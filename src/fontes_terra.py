"""Leitura dos DEMs terrestres (NASADEM via Earthdata; ArcticDEM/REMA via STAC PGC).

Conversão fiel do notebook V1.3.1. Única mudança deliberada: o login Earthdata usa
`earthaccess.login(strategy='netrc')` (regra do projeto: o usuário faz o login
interativo uma vez no próprio terminal; o script nunca pede nem lê a senha).
"""
from __future__ import annotations

import math
import re
import shutil
import zipfile
from contextlib import ExitStack
from pathlib import Path

import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.merge import merge
from rasterio.transform import from_origin
from rasterio.warp import reproject, transform_bounds

from . import config as C


def utm_epsg(lat, lon):
    zona = min(60, max(1, math.floor((lon + 180) / 6) + 1))
    return f'EPSG:{(32600 if lat >= 0 else 32700) + zona}'


def escolher_fonte(lat, lon):
    # Para evitar janela cortando limite de NASADEM, use PGC perto das bordas.
    if lat >= 60.0:
        return 'ArcticDEM', 'EPSG:3413'
    if lat <= -56.0:
        return 'REMA', 'EPSG:3031'
    return 'NASADEM', utm_epsg(lat, lon)


def alvo_grid(lat, lon, n=None):
    n = C.N if n is None else n
    fonte, crs_dest = escolher_fonte(lat, lon)
    x, y = Transformer.from_crs('EPSG:4326', crs_dest, always_xy=True).transform(lon, lat)
    meia = C.RES_M * n / 2
    return fonte, crs_dest, x, y, from_origin(x - meia, y + meia, C.RES_M, C.RES_M)


def codigo_tile(lat, lon):
    return f"{'N' if lat >= 0 else 'S'}{abs(lat):02d}" + f"{'E' if lon >= 0 else 'W'}{abs(lon):03d}"


def necessarios(bbox):
    a, b, c, d = bbox
    if a > c:
        raise ValueError('Recorte cruza antimeridiano; ajustar rotina de tiles.')
    return sorted({codigo_tile(i, j) for i in range(math.floor(b), math.floor(d - 1e-10) + 1)
                   for j in range(math.floor(a), math.floor(c - 1e-10) + 1)})


def extrair_zip_nasadem(arquivo):
    C.CACHE_NASADEM.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(arquivo) as z:
        for info in z.infolist():
            nome = Path(info.filename).name.upper()
            if not re.fullmatch(r'[NS]\d{2}[EW]\d{3}\.HGT', nome):
                continue
            destino = C.CACHE_NASADEM / nome
            if not destino.is_file():
                with z.open(info) as fi, destino.open('wb') as fo:
                    shutil.copyfileobj(fi, fo)


def indice_nasadem():
    C.CACHE_NASADEM.mkdir(parents=True, exist_ok=True)
    # Permite reusar os ZIPs que o usuário já baixou (em entrada/ ou no cache).
    for pasta in (C.ENTRADA, C.CACHE_NASADEM):
        for caminho in pasta.glob('NASADEM_HGT_*.zip'):
            extrair_zip_nasadem(caminho)
    idx = {}
    for p in C.CACHE_NASADEM.rglob('*'):
        if p.is_file() and re.fullmatch(r'[NS]\d{2}[EW]\d{3}\.hgt', p.name, re.I):
            idx[p.stem.upper()] = p
    return idx


_AUTENTICADO = False
_PGC_CLIENTE = None


def tiles_nasadem(bbox):
    global _AUTENTICADO
    codigos = necessarios(bbox)
    existentes = indice_nasadem()
    faltam = [c for c in codigos if c not in existentes]
    if faltam and C.BAIXAR_NASADEM:
        import earthaccess
        if not _AUTENTICADO:
            print('   NASA Earthdata: login (netrc) para os tiles ainda não disponíveis.')
            # Nunca interativo aqui: o usuário roda uma vez no terminal
            # earthaccess.login(strategy='interactive', persist=True)
            earthaccess.login(strategy='netrc')
            _AUTENTICADO = True
        granulos = earthaccess.search_data(
            short_name='NASADEM_HGT', version='001', bounding_box=bbox, count=-1)
        if not granulos:
            raise FileNotFoundError(f'Earthdata não encontrou NASADEM para {bbox}')
        baixados = earthaccess.download(granulos, local_path=str(C.CACHE_NASADEM))
        for p in baixados:
            p = Path(p)
            if p.is_file() and p.suffix.lower() == '.zip':
                extrair_zip_nasadem(p)
        existentes = indice_nasadem()
        faltam = [c for c in codigos if c not in existentes]
    if faltam:
        raise FileNotFoundError('Tiles NASADEM em falta: ' + ', '.join(faltam))
    return [existentes[c] for c in codigos]


def ler_nasadem(lat, lon, dst_crs, dst_tf, n=None):
    n = C.N if n is None else n
    # Mosaico só da janela necessária; CRS de origem WGS84 geográfico.
    bbox = transform_bounds(dst_crs, 'EPSG:4326',
                            dst_tf.c, dst_tf.f - n * C.RES_M,
                            dst_tf.c + n * C.RES_M, dst_tf.f, densify_pts=21)
    tiles = tiles_nasadem(bbox)
    destino = np.full((n, n), np.nan, dtype='float64')
    with ExitStack() as pilha:
        fontes = [pilha.enter_context(rasterio.open(str(p))) for p in tiles]
        mosaico, transf = merge(fontes, bounds=bbox, res=(1 / 3600, 1 / 3600),
                                nodata=-32768, method='first')
        reproject(source=mosaico[0], destination=destino,
                  src_transform=transf, src_crs='EPSG:4326', src_nodata=-32768,
                  dst_transform=dst_tf, dst_crs=dst_crs, dst_nodata=np.nan,
                  resampling=Resampling.average)
    return destino, 'NASA NASADEM_HGT V001', ';'.join(p.name for p in tiles), ''


def pgc_client():
    global _PGC_CLIENTE
    if _PGC_CLIENTE is None:
        from pystac_client import Client
        _PGC_CLIENTE = Client.open(C.STAC_PGC)
    return _PGC_CLIENTE


def ler_pgc(lat, lon, dst_crs, dst_tf, fonte, n=None):
    n = C.N if n is None else n
    # Pesquisa STAC apenas os mosaicos 32m que cruzam a AOI.
    collection = C.PGC_ARCTIC if fonte == 'ArcticDEM' else C.PGC_REMA
    bbox = transform_bounds(dst_crs, 'EPSG:4326',
                            dst_tf.c, dst_tf.f - n * C.RES_M,
                            dst_tf.c + n * C.RES_M, dst_tf.f, densify_pts=21)
    itens = list(pgc_client().search(collections=[collection], bbox=bbox).items())
    itens = sorted(itens, key=lambda item: item.id)
    if not itens:
        raise FileNotFoundError(f'PGC não retornou mosaicos {collection} para {lat}, {lon}')
    destino = np.full((n, n), np.nan, dtype='float64')
    usados = []
    # GeoTIFFs cloud-optimized: GDAL consulta somente blocos do recorte via HTTP range.
    with rasterio.Env(
        GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',
        CPL_VSIL_CURL_ALLOWED_EXTENSIONS='.tif',
        GDAL_HTTP_MAX_RETRY='3', GDAL_HTTP_RETRY_DELAY='1',
        GDAL_HTTP_TIMEOUT='35',
    ):
        for item in itens:
            if 'dem' not in item.assets:
                continue
            href = item.assets['dem'].href
            if not href.startswith('https://'):
                continue
            temporario = np.full((n, n), np.nan, dtype='float64')
            # Um mosaico COG pode ter vários GB, mas não é baixado inteiro.
            with rasterio.open(href) as src:
                reproject(source=rasterio.band(src, 1), destination=temporario,
                          src_transform=src.transform, src_crs=src.crs,
                          src_nodata=src.nodata, dst_transform=dst_tf,
                          dst_crs=dst_crs, dst_nodata=np.nan,
                          resampling=Resampling.average)
            validos = np.isfinite(temporario) & (temporario > -9000)
            inserir = np.isnan(destino) & validos
            destino[inserir] = temporario[inserir]
            if inserir.any():
                usados.append(item.id)
            if np.isfinite(destino).all():
                break
    return destino, f'PGC {collection}', ';'.join(usados), C.STAC_PGC


def dem_terra(lat, lon, n=None):
    fonte, crs, cx, cy, tf = alvo_grid(lat, lon, n)
    if fonte == 'NASADEM':
        arr, dataset, arquivos, url = ler_nasadem(lat, lon, crs, tf, n)
    else:
        arr, dataset, arquivos, url = ler_pgc(lat, lon, crs, tf, fonte, n)
    return arr, tf, crs, {
        'source_dataset': dataset, 'source_files': arquivos,
        'source_catalog_url': url, 'source_native_resolution_m': 32 if fonte != 'NASADEM' else 30,
        'center_x_m': cx, 'center_y_m': cy, 'center_lat': lat, 'center_lon': lon,
        'crs_analysis': crs,
    }

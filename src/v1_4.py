"""Protocolo V1.4 — rugosidade sem tendência + grade de recortes 9 km + alvos configuráveis.

Uso:
    python -m src.v1_4                       # tudo: 43 locais + entrada/alvos.csv
    python -m src.v1_4 --sites earth_teide mars_gale   # só alguns (teste)
    python -m src.v1_4 --sem-terra | --sem-alvos

Decisões (documentadas também no dicionário/relatório):
- Grade: janela de 27×27 km (3×3 recortes de 225×225 px a 40 m) lida com MARGEM de 24 px em volta
  (janela de trabalho 723×723). Os campos (declividade, rugosidades) são calculados na janela inteira e
  agregados por recorte; a exclusão de borda é só a margem externa, que fica fora de todos os recortes.
  24 px cobre o alcance dos filtros (gaussiano σ=5 truncado em 4σ = 20 px + janela 5×5 = 2 px + gradiente 1 px).
  A grade de 40 m é a mesma do V1.3.1 (centro no mesmo ponto), então o recorte r2c2 = recorte do V1.3.1.
- Rugosidade nova: DP local 5×5 de gauss(dem,1) − gauss(dem,5). Legada (V1.3.1): DP local 5×5 de gauss(dem,1).
- NoData: vizinho mais próximo só para filtros; exclusão de 7 px (declividade/rugosidade legada, como V1.3.1)
  e 23 px (rugosidade nova) em volta de cada lacuna. Recorte com cobertura < 99,9% é descartado.
- Terra: fonte decidida pela janela inteira (se a janela tocar 60°N → ArcticDEM; −56° → REMA).
- Marte (STAC, método 1 aprovado): DTM CTX único por alvo; reprojeção para azimutal equidistante local
  centrada no alvo (o CRS nativo eqc lat_ts=0 distorce a escala em x); escolhe-se o DTM que comporta mais
  recortes 9 km totalmente válidos (com margem) e usam-se até 9, os mais próximos do ponto.
"""
from __future__ import annotations

import argparse
import math
import shutil
import time
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from pyproj import CRS, Transformer
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.warp import reproject, transform_bounds
from scipy.ndimage import distance_transform_cdt, distance_transform_edt, gaussian_filter, uniform_filter

from . import config as C
from .esquema import (COMPLETA_COLS, TIPO_MAP, ZEUS_COLS, escrever_dicionario, secao_estatisticas, validar)
from .fontes_terra import escolher_fonte, ler_nasadem, ler_pgc, utm_epsg
from .util import ler_csv, salvar_tif

PROTOCOLO = 'v1_4'
N_TILE = 225
GRADE = 3
MARGEM = 24
N_JANELA = GRADE * N_TILE + 2 * MARGEM          # 723
SIGMA_REG = 5.0
RAIO_LOCAL = 7
RAIO_REG = 23
OUT = C.OUTPUTS / PROTOCOLO
STAC_USGS = 'https://stac.astrogeology.usgs.gov/api/'
R_MARTE = 3396190.0
MAX_TILES_MARTE = 9
TOP_DTMS = 6                            # DTMs (pré-selecionados pelo footprint) lidos para decidir pelos dados


# ----------------------------------------------------------------------------- campos e agregação
def campos(dem: np.ndarray) -> dict:
    dem = np.asarray(dem, dtype='float64')
    validos = np.isfinite(dem)
    if not validos.any():
        raise ValueError('janela sem elevações válidas')
    if (~validos).any():
        idx = distance_transform_edt(~validos, return_distances=False, return_indices=True)
        dem_f = dem[tuple(idx)]
        dist = distance_transform_cdt(validos, metric='chessboard')   # distância até a lacuna mais próxima
        excl_local, excl_reg = dist <= RAIO_LOCAL, dist <= RAIO_REG
    else:
        dem_f = dem
        excl_local = excl_reg = np.zeros(dem.shape, bool)
    z1 = gaussian_filter(dem_f, sigma=C.SIGMA_PX, mode='reflect')
    z_reg = gaussian_filter(dem_f, sigma=SIGMA_REG, mode='reflect')
    gy, gx = np.gradient(z1, C.RES_M, C.RES_M)
    decliv = np.degrees(np.arctan(np.hypot(gx, gy)))

    def dp_local(a):
        m = uniform_filter(a, size=C.RUGOSIDADE_JANELA, mode='reflect')
        m2 = uniform_filter(a * a, size=C.RUGOSIDADE_JANELA, mode='reflect')
        return np.sqrt(np.maximum(m2 - m * m, 0))

    ctr = z1 - z1.mean()
    return {'dem': dem, 'validos': validos, 'decliv': decliv, 'rug_leg': dp_local(ctr),
            'rug': dp_local(z1 - z_reg), 'excl_local': excl_local, 'excl_reg': excl_reg}


def features_recorte(F: dict, r0: int, c0: int, margem_ok: bool = True):
    """Retorna (features, motivo_descarte)."""
    sl = (slice(r0, r0 + N_TILE), slice(c0, c0 + N_TILE))
    v = F['validos'][sl]
    if v.shape != (N_TILE, N_TILE):
        return None, 'recorte fora da janela'
    cob = 100.0 * v.mean()
    nod = int((~v).sum())
    if cob < C.MIN_VALID_PCT - 1e-7:
        return None, f'cobertura {cob:.3f}% < {C.MIN_VALID_PCT}% ({nod} px sem dado)'
    m_l = ~F['excl_local'][sl]
    m_r = ~F['excl_reg'][sl]
    if not m_l.any() or not m_r.any():
        return None, 'sem pixels confiáveis após exclusão em volta de NoData'
    decl = F['decliv'][sl][m_l]
    rl = F['rug_leg'][sl][m_l]
    r = F['rug'][sl][m_r]
    elev = F['dem'][sl][v]
    p05, p95 = np.percentile(elev, [5, 95])
    return {
        'valid_coverage_pct': float(cob), 'nodata_pixels': nod,
        'median_slope_deg': float(np.median(decl)), 'p90_slope_deg': float(np.percentile(decl, 90)),
        'median_roughness_m': float(np.median(r)), 'p90_roughness_m': float(np.percentile(r, 90)),
        'robust_relief_p95_p5_m': float(p95 - p05),
        'mean_slope_deg': float(decl.mean()), 'roughness_m': float(r.mean()),
        'relative_relief_m': float(elev.max() - elev.min()),
        'roughness_legacy_mean_m': float(rl.mean()), 'roughness_legacy_median_m': float(np.median(rl)),
        'roughness_legacy_p90_m': float(np.percentile(rl, 90)),
        '_cob_metricas_local_pct': float(100 * m_l.mean()), '_cob_metricas_reg_pct': float(100 * m_r.mean()),
    }, ''


def latlon_centro(crs, tf, r0, c0):
    c = CRS.from_user_input(crs if isinstance(crs, str) else crs.to_wkt())
    x, y = tf * (c0 + N_TILE / 2, r0 + N_TILE / 2)
    lon, lat = Transformer.from_crs(c, c.geodetic_crs, always_xy=True).transform(x, y)
    return float(lat), ((float(lon) + 180) % 360) - 180


def grade_3x3():
    return [(f'r{i + 1}c{j + 1}', MARGEM + i * N_TILE, MARGEM + j * N_TILE)
            for i in range(GRADE) for j in range(GRADE)]


# ----------------------------------------------------------------------------- leitores
def janela_terra(lat, lon, n=N_JANELA):
    fonte, crs = escolher_fonte(lat, lon)

    def grid(crs_):
        x, y = Transformer.from_crs('EPSG:4326', crs_, always_xy=True).transform(lon, lat)
        tf_ = from_origin(x - n * C.RES_M / 2, y + n * C.RES_M / 2, C.RES_M, C.RES_M)
        bb = transform_bounds(crs_, 'EPSG:4326', tf_.c, tf_.f - n * C.RES_M, tf_.c + n * C.RES_M, tf_.f,
                              densify_pts=21)
        return tf_, bb

    tf, bbox = grid(crs)
    nota = ''
    if fonte == 'NASADEM' and bbox[3] >= 60.0:
        fonte, crs, nota = 'ArcticDEM', 'EPSG:3413', 'janela toca 60°N: ArcticDEM'
        tf, bbox = grid(crs)
    elif fonte == 'NASADEM' and bbox[1] <= -56.0:
        fonte, crs, nota = 'REMA', 'EPSG:3031', 'janela toca 56°S: REMA'
        tf, bbox = grid(crs)
    if fonte == 'NASADEM' and (bbox[0] > bbox[2] or bbox[2] - bbox[0] > 180):
        raise ValueError('janela cruza o antimeridiano (não suportado)')
    if fonte == 'NASADEM':
        arr, ds, arqs, _ = ler_nasadem(lat, lon, crs, tf, n)
        res = 30.0
    else:
        arr, ds, arqs, _ = ler_pgc(lat, lon, crs, tf, fonte, n)
        res = 32.0
    return arr, tf, crs, {'source_dataset': ds, 'native_res_m': res, 'source_files': arqs, 'nota': nota}


def janela_raster(href, cx, cy, n=N_JANELA):
    """Janela n×n (40 m) centrada em (cx, cy) no CRS do próprio raster (média dos pixels nativos)."""
    env = dict(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR', GDAL_HTTP_MAX_RETRY='3', GDAL_HTTP_RETRY_DELAY='1')
    with rasterio.Env(**env), rasterio.open(href) as src:
        tf = from_origin(cx - n * C.RES_M / 2, cy + n * C.RES_M / 2, C.RES_M, C.RES_M)
        dst = np.full((n, n), np.nan, 'float64')
        reproject(rasterio.band(src, 1), dst, src_transform=src.transform, src_crs=src.crs,
                  src_nodata=src.nodata, dst_transform=tf, dst_crs=src.crs, dst_nodata=np.nan,
                  resampling=Resampling.average)
        return dst, tf, src.crs, abs(src.res[0])


def xy_no_crs(href, lat, lon):
    with rasterio.open(href) as src:
        c = CRS.from_wkt(src.crs.to_wkt())
    return Transformer.from_crs(c.geodetic_crs, c, always_xy=True).transform(lon, lat)


def centro_geotiff(href):
    with rasterio.open(href) as src:
        b = src.bounds
    return (b.left + b.right) / 2, (b.bottom + b.top) / 2


def marte_stac(lat, lon, colecao):
    """Método 1: DTM único, até 9 recortes 100% válidos (com margem) mais próximos do ponto."""
    import shapely
    from pystac_client import Client
    from shapely.geometry import box, shape

    aeqd = CRS.from_proj4(f'+proj=aeqd +lat_0={lat} +lon_0={lon} +R={R_MARTE} +units=m +no_defs')
    geo = CRS.from_proj4(f'+proj=longlat +R={R_MARTE} +no_defs')
    to_aeqd = Transformer.from_crs(geo, aeqd, always_xy=True).transform
    d = 0.01
    itens = list(Client.open(STAC_USGS).search(collections=[colecao], bbox=[lon - d, lat - d, lon + d, lat + d],
                                               max_items=100).items())
    if not itens:
        raise FileNotFoundError(f'nenhum DTM em {colecao} contém ({lat}, {lon})')
    passo = N_TILE * C.RES_M            # 9000 m
    meio = passo / 2 + MARGEM * C.RES_M
    K = 4                               # região de busca: recortes -4..4 em volta do ponto (81 km)
    cand = [(i, j) for i in range(-K, K + 1) for j in range(-K, K + 1)]

    # 1) pré-seleção barata pelo footprint STAC (que pode não refletir os NoData reais)
    ranking = []
    for it in itens:
        poly = shapely.transform(shape(it.geometry),
                                 lambda xy: np.column_stack(to_aeqd(xy[:, 0], xy[:, 1]))).buffer(-2 * C.RES_M)
        n_ok = sum(poly.contains(box(j * passo - meio, -i * passo - meio, j * passo + meio, -i * passo + meio))
                   for i, j in cand)
        ranking.append((n_ok, poly.area, it))
    ranking.sort(key=lambda t: (t[0], t[1]), reverse=True)

    # 2) decisão pelos dados reais: lê os TOP_DTMS melhores e conta recortes 100% válidos (com margem)
    lado = (2 * K + 1) * N_TILE + 2 * MARGEM
    tf_reg = from_origin(-K * passo - meio, K * passo + meio, C.RES_M, C.RES_M)
    dst_crs = rasterio.crs.CRS.from_wkt(aeqd.to_wkt())
    env = dict(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR', GDAL_HTTP_MAX_RETRY='3', GDAL_HTTP_RETRY_DELAY='1')
    melhor, tentativas = None, []
    for _n, _a, it in ranking[:TOP_DTMS]:
        chave_asset = 'dem' if 'dem' in it.assets else 'dtm'
        try:
            dst = np.full((lado, lado), np.nan, 'float64')
            with rasterio.Env(**env), rasterio.open(it.assets[chave_asset].href) as src:
                reproject(rasterio.band(src, 1), dst, src_transform=src.transform, src_crs=src.crs,
                          src_nodata=src.nodata, dst_transform=tf_reg, dst_crs=dst_crs,
                          dst_nodata=np.nan, resampling=Resampling.average)
                res = abs(src.res[0])
        except Exception as e:  # noqa: BLE001 — asset quebrado: registra e tenta o próximo
            tentativas.append(f'{it.id}: {type(e).__name__}: {str(e)[:60]}')
            continue
        v = np.isfinite(dst)
        bloco = N_TILE + 2 * MARGEM
        ok = [(i, j) for i, j in cand
              if v[(i + K) * N_TILE:(i + K) * N_TILE + bloco, (j + K) * N_TILE:(j + K) * N_TILE + bloco].mean()
              >= C.MIN_VALID_PCT / 100 - 1e-9]
        ok = sorted(ok, key=lambda t: math.hypot(*t))[:MAX_TILES_MARTE]
        tentativas.append(f'{it.id}: {len(ok)} recortes válidos')
        chave = (len(ok), -sum(math.hypot(*t) for t in ok))
        if ok and (melhor is None or chave > melhor[0]):
            melhor = (chave, it, chave_asset, ok, dst, res)
    if melhor is None:
        raise ValueError(f'nenhum DTM comporta um recorte de 9 km válido. Tentativas: {"; ".join(tentativas)}')
    _, it, chave_asset, tiles, dst, res = melhor

    # 3) recorta a região ao retângulo dos recortes escolhidos (+ margem) e renumera a grade a partir de r1c1
    imin, imax = min(t[0] for t in tiles), max(t[0] for t in tiles)
    jmin, jmax = min(t[1] for t in tiles), max(t[1] for t in tiles)
    r0, c0 = (imin + K) * N_TILE, (jmin + K) * N_TILE
    dem = dst[r0:(imax + K + 1) * N_TILE + 2 * MARGEM, c0:(jmax + K + 1) * N_TILE + 2 * MARGEM]
    tf = from_origin(jmin * passo - meio, -imin * passo + meio, C.RES_M, C.RES_M)
    grade = [(f'r{i - imin + 1}c{j - jmin + 1}', MARGEM + (i - imin) * N_TILE, MARGEM + (j - jmin) * N_TILE)
             for i, j in tiles]
    meta = {'native_res_m': round(res, 2), 'source_files': f'{it.id} [{chave_asset}]',
            'nota': f'{len(itens)} DTMs no ponto; testados pelos dados: {" | ".join(tentativas)}'}
    return dem, tf, aeqd.to_wkt(), grade, meta


# ----------------------------------------------------------------------------- execução
def processar_janela(dem, tf, crs, grade, base, linhas, status, dir_dem):
    F = campos(dem)
    if dir_dem is not None:
        salvar_tif(dir_dem / f'{base["site_id"]}.tif', dem, tf,
                   crs if not isinstance(crs, str) or crs.startswith('EPSG') else rasterio.crs.CRS.from_wkt(crs))
    for nome, r0, c0 in grade:
        tile_id = f'{base["site_id"]}_{nome}'
        feat, motivo = features_recorte(F, r0, c0)
        if feat is None:
            status.append({'tile_id': tile_id, 'site_id': base['site_id'], 'status': 'DESCARTADO',
                           'detail': motivo, 'protocol': PROTOCOLO})
            continue
        lat, lon = latlon_centro(crs, tf, r0, c0)
        extra = {k: feat.pop(k) for k in list(feat) if k.startswith('_')}
        linhas.append({'tile_id': tile_id, **base, 'lat': lat, 'lon': lon, 'protocol': PROTOCOLO, **feat})
        aviso = f'{feat["nodata_pixels"]} px NoData' if feat['nodata_pixels'] else ''
        status.append({'tile_id': tile_id, 'site_id': base['site_id'], 'status': 'OK',
                       'detail': '; '.join(x for x in [aviso,
                                                       f'cobertura métricas {extra["_cob_metricas_local_pct"]:.2f}%/'
                                                       f'{extra["_cob_metricas_reg_pct"]:.2f}%'] if x),
                       'protocol': PROTOCOLO})


def rodar(sites=None, terra=True, alvos=True, salvar_dem=True):
    OUT.mkdir(parents=True, exist_ok=True)
    dir_dem = OUT / 'dem_janelas' if salvar_dem else None
    if dir_dem:
        dir_dem.mkdir(exist_ok=True)
    linhas, status, erros = [], [], []

    def erro(site_id, e):
        erros.append({'site_id': site_id, 'erro': f'{type(e).__name__}: {e}'})
        status.append({'tile_id': '', 'site_id': site_id, 'status': 'ERRO',
                       'detail': f'{type(e).__name__}: {e}', 'protocol': PROTOCOLO})
        print('   ERRO', type(e).__name__, str(e)[:200], flush=True)

    if terra:
        cat = ler_csv(C.CSV_LOCAIS)
        for k, (_, r) in enumerate(cat.iterrows(), 1):
            if sites and r.region_id not in sites:
                continue
            t0 = time.time()
            print(f'[{k:02d}/{len(cat)}] {r.local}', flush=True)
            try:
                dem, tf, crs, meta = janela_terra(float(r.lat), float(r.lon))
                base = {'site_id': r.region_id, 'site_name': r.local, 'body': 'EARTH', 'tipo': TIPO_MAP[r.tipo],
                        'source_dataset': meta['source_dataset'], 'native_res_m': meta['native_res_m']}
                status.append({'tile_id': '', 'site_id': r.region_id, 'status': 'INFO',
                               'detail': '; '.join(x for x in [meta['source_files'], meta['nota']] if x),
                               'protocol': PROTOCOLO})
                processar_janela(dem, tf, crs, grade_3x3(), base, linhas, status, dir_dem)
                print(f'   ok ({time.time() - t0:.0f}s) {meta["nota"]}', flush=True)
            except Exception as e:  # noqa: BLE001 — registrado no status
                erro(r.region_id, e)
            pd.DataFrame(linhas).to_csv(OUT / 'checkpoint_linhas.csv', index=False)

    if alvos:
        cfg = pd.read_csv(C.ALVOS_CSV)
        for _, a in cfg.iterrows():
            if sites and a.id not in sites:
                continue
            t0 = time.time()
            print(f'[ALVO] {a.nome} ({a.corpo})', flush=True)
            try:
                base = {'site_id': a.id, 'site_name': a.nome, 'body': a.corpo, 'tipo': 'alvo',
                        'source_dataset': a.fonte}
                cam = str(a.caminho_geotiff)
                if a.metodo == 'stac_dtm_unico':
                    dem, tf, crs, grade, meta = marte_stac(float(a.lat_centro), float(a.lon_centro),
                                                           cam.split(':', 1)[1])
                    base['native_res_m'] = meta['native_res_m']
                    status.append({'tile_id': '', 'site_id': a.id, 'status': 'INFO',
                                   'detail': f'{meta["source_files"]}; {meta["nota"]}', 'protocol': PROTOCOLO})
                else:
                    href = cam if cam.startswith('http') else str(C.BASE / cam)
                    if a.metodo == 'janela_centro_geotiff':
                        cx, cy = centro_geotiff(href)
                    else:
                        cx, cy = xy_no_crs(href, float(a.lat_centro), float(a.lon_centro))
                    dem, tf, crs, res = janela_raster(href, cx, cy)
                    base['native_res_m'] = round(res, 2)
                    grade = grade_3x3()
                processar_janela(dem, tf, crs, grade, base, linhas, status, dir_dem)
                print(f'   ok ({time.time() - t0:.0f}s)', flush=True)
            except Exception as e:  # noqa: BLE001
                erro(a.id, e)
    return linhas, status, erros


def exportar(linhas, status, erros, copiar_entrega=True):
    completa = pd.DataFrame(linhas)[COMPLETA_COLS]
    zeus = completa[ZEUS_COLS].copy()
    falhas = validar(completa, zeus)
    completa.to_csv(OUT / 'tabela_completa.csv', index=False)
    zeus.to_csv(OUT / 'zeus_input.csv', index=False)
    st = pd.DataFrame(status)
    st.to_csv(OUT / 'processing_status.csv', index=False)
    cl, zl = pd.read_csv(OUT / 'tabela_completa.csv'), pd.read_csv(OUT / 'zeus_input.csv')
    falhas += [f'(após releitura) {x}' for x in validar(cl, zl)]
    notas = [
        '**Rugosidade sem tendência**: `median_roughness_m`, `p90_roughness_m` e `roughness_m` usam o DP local 5×5 '
        'de gauss(σ=1 px) − gauss(σ=5 px ≈ 200 m). A versão antiga (com tendência) está em `roughness_legacy_*`.',
        'Grade: cada local terrestre e alvo lunar/Jezero tem uma janela de 27×27 km fatiada em 3×3 recortes de '
        '9 km (`r1c1` = canto noroeste da grade no CRS de análise; `r2c2` = centro, idêntico ao recorte do V1.3.1). '
        'A janela é lida com margem de 24 px para que os filtros tenham contexto; essa margem é a única borda excluída.',
        'Marte (exceto Jezero): DTM CTX único da USGS (STAC), reprojetado para azimutal equidistante local; até 9 '
        'recortes de 9 km totalmente válidos, os mais próximos do ponto do alvo. `r1c1` = recorte mais ao noroeste '
        'entre os escolhidos; a grade pode não ser 3×3 completa.',
        'Lua: mosaico LOLA 20 m (PGDA, Barker et al. 2023), lido por janela (COG). Os centros das regiões vêm dos '
        'DEMs de 5 m do PGDA com o mesmo nome (correspondência por nome, não oficial).',
        'Lat/lon: centro de cada recorte pela transformação do raster; Terra em WGS84, Lua/Marte no CRS geodésico '
        'esférico do próprio corpo; longitude leste-positiva em -180..180.',
        'Valores `v1_4` não são comparáveis numericamente com `v1_3_1` para a rugosidade (definição mudou).',
        '**Piso de ruído do NASADEM**: em superfícies quase planas o NASADEM mostra ~0,5–0,9° de declividade e '
        '~0,5–0,8 m de rugosidade só por ruído (Salar de Uyuni: 0,6° / 0,5 m; gelo REMA/ArcticDEM: 0,008 m). '
        'Recortes terrestres planos com `source_dataset` NASADEM parecem mais inclinados/rugosos do que são. '
        'Não corrigido (decisão do projeto); ver `outputs/v1_4/investigacao_lua/diagnostico.md`.',
        'Rugosidade lunar baixa (~1 m) foi checada contra DEMs LOLA 5 m e DTMs estéreo Kaguya: é consistente, '
        'não é artefato. Nobile Rim 2 tem resolução efetiva pior (~30 m).',
    ]
    escrever_dicionario(OUT / 'dicionario_colunas.md', PROTOCOLO, notas)
    relatorio(cl, zl, st, erros, falhas)
    if copiar_entrega and not falhas:
        ent = C.BASE / 'entrega_zeus'
        for nome in ('zeus_input.csv', 'tabela_completa.csv', 'dicionario_colunas.md'):
            shutil.copy2(OUT / nome, ent / nome)
    return falhas


def comparacao_v131(cl: pd.DataFrame) -> list[str]:
    ref = C.OUTPUTS / 'v1_3_1' / 'tabela_completa.csv'
    if not ref.is_file():
        return ['(tabela v1_3_1 não encontrada)']
    a = pd.read_csv(ref).set_index('site_id')
    b = cl[cl.tile_id.str.endswith('_r2c2')].set_index('site_id')
    comum = [s for s in b.index if s in a.index and b.loc[s, 'body'] == 'EARTH']
    pares = [('median_slope_deg', 'median_slope_deg'), ('p90_slope_deg', 'p90_slope_deg'),
             ('roughness_legacy_median_m', 'median_roughness_m'), ('robust_relief_p95_p5_m', 'robust_relief_p95_p5_m')]
    linhas = []
    for nb, na in pares:
        rel = (b.loc[comum, nb] - a.loc[comum, na]).abs() / a.loc[comum, na].abs().clip(lower=1e-9)
        linhas.append({'coluna_v1_4': nb, 'coluna_v1_3_1': na, 'n': len(comum),
                       'mediana_dif_rel': rel.median(), 'max_dif_rel': rel.max(), 'site_max': rel.idxmax()})
    return ['Recorte central `r2c2` da V1.4 × recorte único da V1.3.1 (mesma grade de 40 m e mesmo DEM na Terra). '
            'Diferenças esperadas só por contexto de filtro nas bordas do recorte (V1.3.1 usava reflexão + 3 px de '
            'borda) e por eventual mudança de fonte.', '', pd.DataFrame(linhas).to_markdown(index=False, floatfmt='.2e'), '']


def relatorio(cl, zl, st, erros, falhas):
    r = [f'# Relatório de qualidade — protocolo `{PROTOCOLO}`', '', '## Validações obrigatórias', '']
    r += ['- ' + ('**OK** — colunas no esquema, `zeus_input` numérico sem NaN, mesma contagem e ordem, body/tipo '
                  'válidos, `tile_id` único, lat/lon dentro dos limites.' if not falhas
                  else '**FALHAS:**\n' + '\n'.join(f'  - {x}' for x in falhas))]
    r += [f'- Linhas: `tabela_completa.csv` = {len(cl)}, `zeus_input.csv` = {len(zl)}.', '']
    desc = st[st.status == 'DESCARTADO']
    r += ['## Recortes descartados', '', f'{len(desc)} recortes.', '']
    if len(desc):
        r += [desc[['tile_id', 'detail']].to_markdown(index=False), '']
    r += ['## Locais/alvos com erro', '', 'Nenhum.' if not erros else pd.DataFrame(erros).to_markdown(index=False), '']
    info = st[(st.status == 'INFO') & st.site_id.str.startswith('mars_')]
    if len(info):
        r += ['## DTMs escolhidos (Marte, STAC)', '', info[['site_id', 'detail']].to_markdown(index=False), '']
    r += ['## Recortes por local (alvos)', '',
          cl[cl.body != 'EARTH'].groupby(['body', 'site_id']).size().rename('recortes').reset_index()
          .to_markdown(index=False), '']
    r += secao_estatisticas(cl)
    feats_c = ['median_slope_deg', 'median_roughness_m', 'roughness_legacy_median_m']
    r += ['## Efeito da remoção de tendência', '',
          'Correlação de Pearson entre declividade mediana e rugosidade (nova × legada), todas as linhas:', '',
          cl[feats_c].corr().round(3).to_markdown(), '']
    r += ['## Comparação com o V1.3.1', ''] + comparacao_v131(cl)
    (OUT / 'relatorio_qualidade.md').write_text('\n'.join(r) + '\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sites', nargs='*')
    ap.add_argument('--sem-terra', action='store_true')
    ap.add_argument('--sem-alvos', action='store_true')
    ap.add_argument('--nao-copiar', action='store_true', help='não copiar para entrega_zeus/')
    a = ap.parse_args()
    linhas, status, erros = rodar(a.sites, not a.sem_terra, not a.sem_alvos)
    if not linhas:
        raise SystemExit('nenhuma linha gerada')
    falhas = exportar(linhas, status, erros, copiar_entrega=not (a.nao_copiar or a.sites))
    n = pd.DataFrame(linhas).body.value_counts().to_dict()
    print('Linhas por corpo:', n, '| erros:', len(erros), '| validações:', 'OK' if not falhas else falhas)


if __name__ == '__main__':
    main()

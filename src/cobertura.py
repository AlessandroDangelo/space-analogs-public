"""Protocolo v1_5 = v1_4 (terreno) + cobertura superficial por recorte.

Uso:  python -m src.cobertura        -> outputs/v1_5/ (e cópia das tabelas em entrega_zeus/)

Como funciona
- Terra: ESA WorldCover 2021 v200 (10 m, 11 classes; COG público na AWS, sem login). Para cada local, a janela
  DEM salva pela V1.4 (`outputs/v1_4/dem_janelas/{site}.tif`) dá o CRS e a grade de análise; os pixels
  WorldCover são reprojetados (vizinho mais próximo) para uma grade de 10 m alinhada a ela (4×4 subpixels por
  pixel de 40 m) e contados por recorte. As frações somam 1 nos pixels com dado.
- Antártida: o WorldCover não cobre a Antártida. Usa-se o mapa de afloramentos rochosos do AADC (Toth & Terauds
  2023, 100 m): fração de rocha → `frac_solo_exposto`; o resto → `frac_neve_gelo` (`cover_source =
  aadc_afloramentos`). Sem esse arquivo, os domos recebem gelo = 1 atribuído e McMurdo fica fora.
- Lua e Marte: superfície sem vegetação, construções ou água em estado líquido → solo exposto = 1, demais 0
  (`cover_source = atribuido_corpo_sem_vegetacao`). Gelo em crateras permanentemente sombreadas não é cobertura
  visível e não entra.
"""
from __future__ import annotations

import math
import shutil

import numpy as np
import pandas as pd
import rasterio
from affine import Affine
from rasterio.enums import Resampling
from rasterio.warp import reproject, transform_bounds

from . import config as C
from .esquema import (COBERTURA_ZEUS, COMPLETA_COLS_V15, DICIONARIO_COBERTURA, VEGETACAO, WORLDCOVER_CLASSES,
                      ZEUS_COLS_V15, escrever_dicionario, secao_estatisticas, validar)
from .v1_4 import MARGEM, N_TILE

PROTOCOLO = 'v1_5'
BASE_ORIGEM = C.OUTPUTS / 'v1_4'
OUT = C.OUTPUTS / PROTOCOLO
WC_URL = 'https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_{}_Map.tif'
SUB = 4                                   # 40 m / 10 m
MANTO_DE_GELO = {'earth_dome_c', 'earth_vostok', 'earth_dome_argus'}   # só se o mapa AADC não existir
# Antártida: Toth & Terauds (2023), Ice-free Antarctica — union of rock outcrop layers (AADC, CC BY 4.0).
# Extraído de entrada/AAS_4568_ice-free_rock_outcrop_union.zip para cache/antartida/.
AADC = C.BASE / 'cache' / 'antartida' / 'rock_union1.tif'
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR', GDAL_HTTP_MAX_RETRY='3', GDAL_HTTP_RETRY_DELAY='1',
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS='.tif')


def tiles_worldcover(bbox):
    """Nomes dos tiles 3°×3° do WorldCover que cruzam o bbox (lon_min, lat_min, lon_max, lat_max)."""
    lon0, lat0, lon1, lat1 = bbox
    nomes = []
    for la in range(math.floor(lat0 / 3) * 3, math.floor(lat1 / 3) * 3 + 1, 3):
        for lo in range(math.floor(lon0 / 3) * 3, math.floor(lon1 / 3) * 3 + 1, 3):
            nomes.append(f"{'N' if la >= 0 else 'S'}{abs(la):02d}{'E' if lo >= 0 else 'W'}{abs(lo):03d}")
    return nomes


def classes_10m(site_id):
    """Raster de classes WorldCover (uint8, 0 = sem dado) na grade de 10 m alinhada à janela V1.4."""
    with rasterio.open(BASE_ORIGEM / 'dem_janelas' / f'{site_id}.tif') as d:
        crs, tf, h, w = d.crs, d.transform, d.height, d.width
    tf10 = tf * Affine.scale(1 / SUB)
    dst = np.zeros((h * SUB, w * SUB), 'uint8')
    bbox = transform_bounds(crs, 'EPSG:4326', tf.c, tf.f + h * tf.e, tf.c + w * tf.a, tf.f, densify_pts=21)
    usados = []
    for nome in tiles_worldcover(bbox):
        tmp = np.zeros_like(dst)
        try:
            with rasterio.Env(**ENV), rasterio.open(WC_URL.format(nome)) as src:
                reproject(rasterio.band(src, 1), tmp, src_transform=src.transform, src_crs=src.crs, src_nodata=0,
                          dst_transform=tf10, dst_crs=crs, dst_nodata=0, resampling=Resampling.nearest)
        except rasterio.errors.RasterioIOError:
            continue                                   # tile inexistente (oceano aberto ou Antártida)
        novo = (dst == 0) & (tmp != 0)
        dst[novo] = tmp[novo]
        if novo.any():
            usados.append(nome)
    return dst, usados


def offsets(tile_id):
    rc = tile_id.rsplit('_', 1)[1]                    # 'r2c3'
    r, c = int(rc[1:rc.index('c')]), int(rc[rc.index('c') + 1:])
    return MARGEM + (r - 1) * N_TILE, MARGEM + (c - 1) * N_TILE


def fracoes(cls_tile):
    validos = cls_tile[cls_tile > 0]
    out = {col: float((validos == cod).mean()) if validos.size else np.nan for cod, col in WORLDCOVER_CLASSES.items()}
    out['frac_vegetacao'] = float(sum(out[c] for c in VEGETACAO)) if validos.size else np.nan
    return out, (validos.size / cls_tile.size if cls_tile.size else 0.0)


def atribuido(solo, gelo, fonte):
    out = {col: 0.0 for col in WORLDCOVER_CLASSES.values()}
    out['frac_solo_exposto'], out['frac_neve_gelo'], out['frac_vegetacao'] = solo, gelo, 0.0
    out['cover_source'] = fonte
    return out


_CACHE_ROCHA = {}


def rocha_aadc_10m(site_id):
    """Máscara de rocha exposta (True) na grade de 10 m da janela, a partir do mapa AADC (100 m, EPSG:3031).
    Qualquer valor > 0 = afloramento (o produto é a UNIÃO de duas camadas; o significado de 1/2/3 não é
    documentado). 0 = gelo/neve ou mar (o produto não separa os dois)."""
    if site_id in _CACHE_ROCHA:
        return _CACHE_ROCHA[site_id]
    with rasterio.open(BASE_ORIGEM / 'dem_janelas' / f'{site_id}.tif') as d:
        crs, tf, h, w = d.crs, d.transform, d.height, d.width
    dst = np.zeros((h * SUB, w * SUB), 'uint8')
    with rasterio.open(AADC) as src:
        reproject(rasterio.band(src, 1), dst, src_transform=src.transform, src_crs=src.crs, src_nodata=None,
                  dst_transform=tf * Affine.scale(1 / SUB), dst_crs=crs, resampling=Resampling.nearest)
    _CACHE_ROCHA[site_id] = dst > 0
    return _CACHE_ROCHA[site_id]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tab = pd.read_csv(BASE_ORIGEM / 'tabela_completa.csv')
    status_v14 = pd.read_csv(BASE_ORIGEM / 'processing_status.csv')
    cobertura, status = {}, []
    for site_id, g in tab.groupby('site_id', sort=False):
        body = g.body.iloc[0]
        if body != 'EARTH':
            for t in g.tile_id:
                cobertura[t] = atribuido(1.0, 0.0, 'atribuido_corpo_sem_vegetacao')
            continue
        print(site_id, flush=True)
        cls, usados = classes_10m(site_id)
        for t in g.tile_id:
            r0, c0 = offsets(t)
            bloco = cls[r0 * SUB:(r0 + N_TILE) * SUB, c0 * SUB:(c0 + N_TILE) * SUB]
            fr, cob = fracoes(bloco)
            if cob >= 0.999:
                cobertura[t] = {**fr, 'cover_source': 'worldcover'}
                status.append({'tile_id': t, 'site_id': site_id, 'status': 'OK',
                               'detail': f'WorldCover {";".join(usados)}; {100 * cob:.2f}% com dado',
                               'protocol': PROTOCOLO})
            elif cob == 0 and g.lat.mean() < -60 and AADC.is_file():
                rocha = rocha_aadc_10m(site_id)[r0 * SUB:(r0 + N_TILE) * SUB, c0 * SUB:(c0 + N_TILE) * SUB]
                f = float(rocha.mean())
                cobertura[t] = atribuido(f, 1.0 - f, 'aadc_afloramentos')
                status.append({'tile_id': t, 'site_id': site_id, 'status': 'OK',
                               'detail': f'Antártida: mapa de afloramentos AADC; rocha exposta {100 * f:.1f}%',
                               'protocol': PROTOCOLO})
            elif site_id in MANTO_DE_GELO and cob == 0:
                cobertura[t] = atribuido(0.0, 1.0, 'atribuido_manto_de_gelo')
                status.append({'tile_id': t, 'site_id': site_id, 'status': 'OK',
                               'detail': 'sem WorldCover (Antártida); neve/gelo = 1 atribuído (interior do manto)',
                               'protocol': PROTOCOLO})
            else:
                status.append({'tile_id': t, 'site_id': site_id, 'status': 'PENDENTE',
                               'detail': f'cobertura WorldCover {100 * cob:.2f}% (< 99,9%); recorte fora da v1_5',
                               'protocol': PROTOCOLO})

    linhas = []
    for _, r in tab.iterrows():
        if r.tile_id not in cobertura:
            continue
        linhas.append({**r.to_dict(), **cobertura[r.tile_id], 'protocol': PROTOCOLO})
    completa = pd.DataFrame(linhas)[COMPLETA_COLS_V15]
    zeus = completa[ZEUS_COLS_V15].copy()
    falhas = validar(completa, zeus, COMPLETA_COLS_V15, ZEUS_COLS_V15)
    completa.to_csv(OUT / 'tabela_completa.csv', index=False)
    zeus.to_csv(OUT / 'zeus_input.csv', index=False)
    cl, zl = pd.read_csv(OUT / 'tabela_completa.csv'), pd.read_csv(OUT / 'zeus_input.csv')
    falhas += [f'(após releitura) {x}' for x in validar(cl, zl, COMPLETA_COLS_V15, ZEUS_COLS_V15)]
    st = pd.concat([status_v14.assign(etapa='terreno_v1_4'), pd.DataFrame(status).assign(etapa='cobertura')])
    st.to_csv(OUT / 'processing_status.csv', index=False)

    notas = [
        'v1_5 = colunas de terreno idênticas à v1_4 + cobertura superficial. Os valores de terreno não mudaram.',
        'Cobertura (Terra): ESA WorldCover 2021 v200, 10 m, reprojetado por vizinho mais próximo para uma grade de '
        '10 m alinhada à grade de análise; frações sobre os pixels com dado (exige ≥ 99,9% com dado).',
        'Lua e Marte: valores atribuídos (solo exposto = 1). Isso é um fato físico, não uma medição; a coluna '
        '`cover_source` diz qual é o caso.',
        'Antártida: fora do WorldCover; cobertura pelo mapa de afloramentos rochosos do AADC (Toth & Terauds '
        '2023, 100 m): rocha → solo exposto, resto → neve/gelo (o produto não separa gelo de mar).',
        'O ZEUS recebe 4 colunas de cobertura (solo exposto, neve/gelo, vegetação, construído); água e as 11 classes '
        'detalhadas ficam só na tabela completa.',
        '**Piso de ruído do NASADEM** (herdado da v1_4): superfícies planas NASADEM parecem mais inclinadas/rugosas '
        'do que são. Ver `outputs/v1_4/investigacao_lua/diagnostico.md`.',
    ]
    escrever_dicionario(OUT / 'dicionario_colunas.md', PROTOCOLO, notas, ZEUS_COLS_V15, DICIONARIO_COBERTURA)

    pend = st[(st.etapa == 'cobertura') & (st.status == 'PENDENTE')]
    rel = [f'# Relatório de qualidade — protocolo `{PROTOCOLO}`', '', '## Validações obrigatórias', '',
           '- ' + ('**OK** — esquema, `zeus_input` numérico sem NaN, mesma contagem e ordem, body/tipo válidos, '
                   '`tile_id` único, lat/lon nos limites.' if not falhas else '**FALHAS:** ' + '; '.join(falhas)),
           f'- Linhas: {len(cl)} (v1_4 tinha {len(tab)}). Por corpo: ' +
           ', '.join(f'{b}={n}' for b, n in cl.body.value_counts().items()) + '.', '',
           '## Recortes fora da v1_5 (cobertura pendente)', '',
           'Nenhum.' if pend.empty else pend[['tile_id', 'detail']].to_markdown(index=False), '',
           '## Origem da cobertura', '', cl.groupby(['body', 'cover_source']).size().rename('recortes')
           .reset_index().to_markdown(index=False), '',
           '## Cobertura média por local (Terra)', '',
           cl[cl.body == 'EARTH'].groupby(['site_name', 'tipo'])[COBERTURA_ZEUS + ['frac_agua']].mean().round(3)
           .reset_index().to_markdown(index=False), '']
    rel += secao_estatisticas(cl)
    (OUT / 'relatorio_qualidade.md').write_text('\n'.join(rel) + '\n', encoding='utf-8')

    if not falhas:
        ent = C.BASE / 'entrega_zeus'
        for nome in ('zeus_input.csv', 'tabela_completa.csv', 'dicionario_colunas.md'):
            shutil.copy2(OUT / nome, ent / nome)
    print('Linhas:', len(cl), cl.body.value_counts().to_dict(), '| pendentes:', len(pend),
          '| validações:', 'OK' if not falhas else falhas)


if __name__ == '__main__':
    main()

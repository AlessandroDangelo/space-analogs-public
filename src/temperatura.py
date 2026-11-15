"""Protocolo v1_6 = v1_5 + temperatura da SUPERFÍCIE por local (repetida nos recortes do local).

Uso:
    python -m src.temperatura terra    # consulta NASA POWER (cache em cache/power/)
    python -m src.temperatura lua      # lê Diviner PRP sul (cache/diviner/)
    python -m src.temperatura marte    # lê o MGCM Legacy da NASA Ames (cache/mars_gcm/)
    python -m src.temperatura montar   # junta tudo em outputs/v1_6/

Features (Kelvin), comuns aos três corpos:
    t_sup_media_K   temperatura média anual da superfície
    t_sup_max_K     temperatura máxima anual da superfície
Fontes e definições exatas por corpo estão em DICIONARIO_TEMPERATURA e em METODOLOGIA.md.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request

import numpy as np
import pandas as pd

from . import config as C

CACHE = C.BASE / 'cache'
INTER = C.OUTPUTS / 'v1_6' / 'temperatura'
POWER_URL = ('https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=TS,TS_MAX,TS_MIN,TS_MAX_AVG,'
             'TS_MIN_AVG&community=RE&longitude={lon}&latitude={lat}&format=JSON')


def terra():
    """NASA POWER, climatologia da temperatura de 'pele' (skin) da superfície, reanálise MERRA-2 (~0,5°×0,625°)."""
    (CACHE / 'power').mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)
    cat = pd.read_csv(C.CSV_LOCAIS, encoding='utf-8-sig')
    from .util import slug
    linhas = []
    for _, r in cat.iterrows():
        site = 'earth_' + slug(r.local)
        bruto = CACHE / 'power' / f'{site}.json'
        if not bruto.is_file():
            with urllib.request.urlopen(POWER_URL.format(lat=r.lat, lon=r.lon), timeout=60) as resp:
                bruto.write_bytes(resp.read())
            time.sleep(0.5)
        p = json.loads(bruto.read_text(encoding='utf-8'))['properties']['parameter']
        ann = {k: p[k]['ANN'] for k in p}
        if any(v is None or v <= -999 for v in ann.values()):
            linhas.append({'site_id': site, 'status': 'ERRO', 'detalhe': f'valores ausentes: {ann}'})
            continue
        linhas.append({'site_id': site, 'status': 'OK',
                       't_sup_media_K': ann['TS'] + 273.15, 't_sup_max_K': ann['TS_MAX'] + 273.15,
                       't_sup_min_K': ann['TS_MIN'] + 273.15,
                       'amplitude_diaria_media_K': ann['TS_MAX_AVG'] - ann['TS_MIN_AVG'],
                       'temp_fonte': 'NASA POWER climatologia (MERRA-2 skin temperature)',
                       'detalhe': f'ponto ({r.lat}, {r.lon})'})
        print('ok', site, flush=True)
    df = pd.DataFrame(linhas)
    df.to_csv(INTER / 'temperatura_terra.csv', index=False)
    print(df.status.value_counts().to_dict())


def lua():
    """Diviner PRP (LRO-L-DLRE-5-PRP-V2.0): malha de 2,88 milhões de triângulos (~0,5 km) até 80°S, com
    temperatura média anual e máxima anual da superfície (ajuste de modelo térmico ao 1º ano de observações,
    Paige et al. 2010). Cada triângulo é atribuído ao recorte que contém o seu centroide; valor do recorte =
    média dos triângulos. Por recorte (não por local), porque a resolução permite."""
    import rasterio
    from pyproj import CRS, Transformer

    from .v1_4 import MARGEM, N_TILE
    INTER.mkdir(parents=True, exist_ok=True)
    tab = C.BASE / 'cache' / 'diviner' / 'dlre_prp_south.tab'
    df = pd.read_csv(tab, skiprows=1, header=None, usecols=[9, 10, 12, 13], names=['lon', 'lat', 'tavg', 'tmax'],
                     skipinitialspace=True)
    df = df[(df.tavg > 0) & (df.tmax > 0)]
    print(f'{len(df)} triângulos válidos; lat {df.lat.min():.2f}..{df.lat.max():.2f}', flush=True)
    t14 = pd.read_csv(C.OUTPUTS / 'v1_5' / 'tabela_completa.csv')
    linhas = []
    for site, g in t14[t14.body == 'MOON'].groupby('site_id', sort=False):
        with rasterio.open(C.OUTPUTS / 'v1_4' / 'dem_janelas' / f'{site}.tif') as d:
            crs, tf = CRS.from_wkt(d.crs.to_wkt()), d.transform
        to_xy = Transformer.from_crs(crs.geodetic_crs, crs, always_xy=True)
        # pré-filtro barato por latitude (janela de 27 km ≈ 0,9° de latitude)
        lat_c = g.lat.mean()
        sub = df[(df.lat > lat_c - 1.5) & (df.lat < lat_c + 1.5)]
        x, y = to_xy.transform(sub.lon.to_numpy(), sub.lat.to_numpy())
        col, row = ~tf * (x, y)
        for t in g.tile_id:
            rc = t.rsplit('_', 1)[1]
            r, c = int(rc[1:rc.index('c')]), int(rc[rc.index('c') + 1:])
            r0, c0 = MARGEM + (r - 1) * N_TILE, MARGEM + (c - 1) * N_TILE
            m = (row >= r0) & (row < r0 + N_TILE) & (col >= c0) & (col < c0 + N_TILE)
            n = int(m.sum())
            if n < 50:
                linhas.append({'tile_id': t, 'site_id': site, 'status': 'ERRO', 'detalhe': f'{n} triângulos'})
                continue
            linhas.append({'tile_id': t, 'site_id': site, 'status': 'OK',
                           't_sup_media_K': float(sub.tavg.to_numpy()[m].mean()),
                           't_sup_max_K': float(sub.tmax.to_numpy()[m].mean()),
                           'temp_fonte': 'LRO Diviner PRP (média e máxima anuais, modelo ajustado)',
                           'detalhe': f'{n} triângulos'})
        print('ok', site, flush=True)
    out = pd.DataFrame(linhas)
    out.to_csv(INTER / 'temperatura_lua.csv', index=False)
    print(out.groupby('site_id')[['t_sup_media_K', 't_sup_max_K']].mean().round(1).to_string())


MARTE_ARQUIVOS = ['LegacyGCM_Ls000_Ls004.nc', 'LegacyGCM_Ls088_Ls092.nc', 'LegacyGCM_Ls179_Ls184.nc',
                  'LegacyGCM_Ls266_Ls272.nc']


def _bilinear(campo, lats, lons, lat, lon):
    """Interpolação bilinear em grade regular lat×lon (lon periódica). campo[..., nlat, nlon]."""
    dlat, dlon = lats[1] - lats[0], lons[1] - lons[0]
    fi = (lat - lats[0]) / dlat
    fj = ((lon - lons[0]) % 360.0) / dlon
    i0, j0 = int(np.floor(fi)), int(np.floor(fj))
    wi, wj = fi - i0, fj - j0
    i1, j0m, j1 = min(i0 + 1, len(lats) - 1), j0 % len(lons), (j0 + 1) % len(lons)
    return ((1 - wi) * (1 - wj) * campo[..., i0, j0m] + (1 - wi) * wj * campo[..., i0, j1]
            + wi * (1 - wj) * campo[..., i1, j0m] + wi * wj * campo[..., i1, j1])


def marte():
    """NASA Ames Legacy MGCM (simulação ACTIVECLDS, Haberle et al. 2019): `tsurf`, grade 5°×6°, 16 horários por
    sol. Usamos 4 trechos de 10 sóis em torno de Ls 0°, 90°, 180° e 270°. Por local (a grade é grossa):
    média anual ≈ média das 4 estações; máxima anual = maior valor nas 4 estações."""
    from scipy.io import netcdf_file
    INTER.mkdir(parents=True, exist_ok=True)
    alvos = pd.read_csv(C.ALVOS_CSV)
    alvos = alvos[alvos.corpo == 'MARS'].copy()
    t15 = pd.read_csv(C.OUTPUTS / 'v1_5' / 'tabela_completa.csv')
    centro = t15[t15.body == 'MARS'].groupby('site_id')[['lat', 'lon']].mean()
    faltam = [a for a in MARTE_ARQUIVOS if not (CACHE / 'mars_gcm' / a).is_file()]
    if faltam:
        raise SystemExit(f'Faltam arquivos do MGCM: {faltam}')
    por_estacao = {s: [] for s in alvos.id}
    for arq in MARTE_ARQUIVOS:
        f = netcdf_file(CACHE / 'mars_gcm' / arq, 'r', mmap=False)
        lats, lons = f.variables['latitude'].data.astype(float), f.variables['longitude'].data.astype(float)
        ts = f.variables['tsurf'].data.astype(float)            # (sol, horário, lat, lon)
        for s in alvos.id:
            lat, lon = centro.loc[s, 'lat'], centro.loc[s, 'lon']
            serie = _bilinear(ts, lats, lons, lat, lon)          # (sol, horário)
            por_estacao[s].append({'arquivo': arq, 'media': serie.mean(), 'max': serie.max(), 'min': serie.min(),
                                   'amplitude': (serie.max(axis=1) - serie.min(axis=1)).mean()})
        f.close()
    linhas = []
    for s, est in por_estacao.items():
        e = pd.DataFrame(est)
        linhas.append({'site_id': s, 'status': 'OK', 't_sup_media_K': e.media.mean(), 't_sup_max_K': e['max'].max(),
                       't_sup_min_K': e['min'].min(), 'amplitude_diaria_media_K': e.amplitude.mean(),
                       'temp_fonte': 'NASA Ames Legacy MGCM (tsurf, 4 estações)',
                       'detalhe': f'ponto ({centro.loc[s, "lat"]:.3f}, {centro.loc[s, "lon"]:.3f}); ' +
                                  '; '.join(f'{r.arquivo[10:20]}: média {r.media:.1f} K' for r in e.itertuples())})
    out = pd.DataFrame(linhas)
    out.to_csv(INTER / 'temperatura_marte.csv', index=False)
    print(out[['site_id', 't_sup_media_K', 't_sup_max_K', 't_sup_min_K', 'amplitude_diaria_media_K']].round(1)
          .to_string(index=False))


def montar():
    """Junta as temperaturas à v1_5 e grava outputs/v1_6/ (tabelas, status, dicionário, relatório)."""
    import shutil

    from .esquema import (COMPLETA_COLS_V16, DICIONARIO_COBERTURA, DICIONARIO_TEMPERATURA, TEMP_ZEUS,
                          ZEUS_COLS_V16, escrever_dicionario, secao_estatisticas, validar)
    out = C.OUTPUTS / 'v1_6'
    t15 = pd.read_csv(C.OUTPUTS / 'v1_5' / 'tabela_completa.csv')
    terra_t = pd.read_csv(INTER / 'temperatura_terra.csv').assign(temp_escala='local')
    marte_t = pd.read_csv(INTER / 'temperatura_marte.csv').assign(temp_escala='local')
    lua_t = pd.read_csv(INTER / 'temperatura_lua.csv').assign(temp_escala='recorte')
    cols = ['t_sup_media_K', 't_sup_max_K', 'temp_fonte', 'temp_escala']
    por_site = pd.concat([terra_t, marte_t])
    por_site = por_site[por_site.status == 'OK'].set_index('site_id')[cols]
    por_tile = lua_t[lua_t.status == 'OK'].set_index('tile_id')[cols]
    linhas, status = [], []
    for _, r in t15.iterrows():
        if r.tile_id in por_tile.index:
            extra = por_tile.loc[r.tile_id]
        elif r.site_id in por_site.index:
            extra = por_site.loc[r.site_id]
        else:
            status.append({'tile_id': r.tile_id, 'site_id': r.site_id, 'status': 'PENDENTE',
                           'detail': 'sem temperatura; recorte fora da v1_6', 'protocol': 'v1_6'})
            continue
        linhas.append({**r.to_dict(), **extra.to_dict(), 'protocol': 'v1_6'})
    completa = pd.DataFrame(linhas)[COMPLETA_COLS_V16]
    zeus = completa[ZEUS_COLS_V16].copy()
    falhas = validar(completa, zeus, COMPLETA_COLS_V16, ZEUS_COLS_V16)
    out.mkdir(parents=True, exist_ok=True)
    completa.to_csv(out / 'tabela_completa.csv', index=False)
    zeus.to_csv(out / 'zeus_input.csv', index=False)
    cl, zl = pd.read_csv(out / 'tabela_completa.csv'), pd.read_csv(out / 'zeus_input.csv')
    falhas += [f'(após releitura) {x}' for x in validar(cl, zl, COMPLETA_COLS_V16, ZEUS_COLS_V16)]
    st15 = pd.read_csv(C.OUTPUTS / 'v1_5' / 'processing_status.csv')
    st = pd.concat([st15, pd.DataFrame(status).assign(etapa='temperatura')]) if status else st15
    st.to_csv(out / 'processing_status.csv', index=False)

    notas = [
        'v1_6 = v1_5 (relevo + cobertura, valores inalterados) + temperatura da SUPERFÍCIE em K.',
        'As três fontes são de natureza diferente: reanálise (Terra, MERRA-2 via NASA POWER), modelo térmico '
        'ajustado a observações (Lua, Diviner) e modelo climático global (Marte, NASA Ames). É o melhor disponível '
        'sem login nem downloads gigantes; os valores são comparáveis em ordem de grandeza, não com precisão de '
        'poucos kelvin.',
        'Mínima anual e amplitude diária existem para Terra e Marte (em outputs/v1_6/temperatura/), mas não para a '
        'Lua (o Diviner PRP não traz mínima); por isso ficam fora da tabela, que só tem colunas completas.',
        'Escala: na Lua, valor por recorte; na Terra e em Marte, um valor por local (repetido nos recortes).',
        'Marte: só 4 trechos de 10 sóis (Ls 0, 90, 180, 270); a máxima anual pode estar levemente subestimada.',
        'Herdado: piso de ruído do NASADEM; McMurdo fora (sem cobertura); Lua/Marte com cobertura atribuída.',
    ]
    escrever_dicionario(out / 'dicionario_colunas.md', 'v1_6', notas, ZEUS_COLS_V16,
                        DICIONARIO_COBERTURA + DICIONARIO_TEMPERATURA)
    rel = ['# Relatório de qualidade — protocolo `v1_6`', '', '## Validações obrigatórias', '',
           '- ' + ('**OK** — esquema, `zeus_input` numérico sem NaN, mesma contagem e ordem, body/tipo válidos, '
                   '`tile_id` único, lat/lon nos limites.' if not falhas else '**FALHAS:** ' + '; '.join(falhas)),
           f'- Linhas: {len(cl)} (v1_5: {len(t15)}). Por corpo: ' +
           ', '.join(f'{b}={n}' for b, n in cl.body.value_counts().items()) + '.', '',
           '## Temperatura por local (média dos recortes)', '',
           cl.groupby(['body', 'site_name'])[TEMP_ZEUS].mean().round(1).reset_index()
           .sort_values(['body', 't_sup_media_K']).to_markdown(index=False), '',
           '## Faixas por corpo', '', cl.groupby('body')[TEMP_ZEUS].describe().round(1).to_markdown(), '']
    rel += secao_estatisticas(cl)
    (out / 'relatorio_qualidade.md').write_text('\n'.join(rel) + '\n', encoding='utf-8')
    if not falhas:
        ent = C.BASE / 'entrega_zeus'
        for nome in ('zeus_input.csv', 'tabela_completa.csv', 'dicionario_colunas.md'):
            shutil.copy2(out / nome, ent / nome)
    print('Linhas:', len(cl), cl.body.value_counts().to_dict(), '| pendentes:', len(status),
          '| validações:', 'OK' if not falhas else falhas)


if __name__ == '__main__':
    {'terra': terra, 'lua': lua, 'marte': marte, 'montar': montar}[sys.argv[1]]()

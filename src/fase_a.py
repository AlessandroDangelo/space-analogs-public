"""Fase A — entrega provisória no esquema estável, a partir do terrain_features_v1_3_1.csv.

Uso:
    python -m src.fase_a            # gera outputs/v1_3_1/ e copia as tabelas para entrega_zeus/
    python -m src.fase_a --sem-recalculo   # pula o recálculo de checagem (planetas + PGC)

Lat/lon dos alvos: centro do recorte (= centro do GeoTIFF, como no notebook), convertido
do CRS projetado para `crs.geodetic_crs` do próprio corpo (não WGS84 da Terra).
"""
from __future__ import annotations

import argparse
import io
import shutil
import zipfile

import numpy as np
import pandas as pd
import rasterio
from pyproj import CRS, Transformer

from . import config as C
from .esquema import (COMPLETA_COLS, TIPO_MAP, ZEUS_COLS, escrever_dicionario, secao_estatisticas,
                      validar)
from .features import calcular_features
from .fontes_terra import dem_terra
from .planetas import dem_planeta, procurar_planeta

PROTOCOLO = 'v1_3_1'
ZIP_ENTREGA = C.ENTRADA / 'space_analogs_clustering_pronto_v1_3_1.zip'
PASTA_ZIP = '03_referencia_e_auditoria/'
OUT_A = C.OUTPUTS / PROTOCOLO
ENTREGA = C.BASE / 'entrega_zeus'


def norm_lon(lon):
    return ((float(lon) + 180.0) % 360.0) - 180.0


def latlon_planeta(arquivo, x, y):
    """Converte (x, y) projetado para lat/lon no CRS geodésico do próprio corpo."""
    with rasterio.open(str(arquivo)) as src:
        crs = CRS.from_wkt(src.crs.to_wkt())
    geo = crs.geodetic_crs
    lon, lat = Transformer.from_crs(crs, geo, always_xy=True).transform(x, y)
    return float(lat), norm_lon(lon), geo.name, geo.ellipsoid.semi_major_metre


def ler_zip(nome):
    with zipfile.ZipFile(ZIP_ENTREGA) as z:
        return pd.read_csv(io.BytesIO(z.read(PASTA_ZIP + nome)))


def montar(orig: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    notas = []
    linhas = []
    padroes = {ident: pattern for ident, _n, _b, pattern, _s in C.PLANETA_CFG}
    for _, r in orig.iterrows():
        if r.body == 'EARTH':
            lat, lon = float(r.center_lat), norm_lon(r.center_lon)
        else:
            arq = procurar_planeta(padroes[r.region_id])
            lat, lon, geo, raio = latlon_planeta(arq, r.center_x_m, r.center_y_m)
            notas.append(f'`{r.region_id}` ({r.region_name}): lat/lon convertidas de x={r.center_x_m:.1f} m, '
                         f'y={r.center_y_m:.1f} m para o CRS geodésico `{geo}` (esfera de raio {raio:.0f} m); '
                         f'lat={lat:.5f}, lon={lon:.5f}.')
        linhas.append({
            'tile_id': f'{r.region_id}_r2c2',
            'site_id': r.region_id,
            'site_name': r.region_name,
            'body': r.body,
            'tipo': TIPO_MAP[r.tipo],
            'lat': lat, 'lon': lon,
            'source_dataset': r.source_dataset,
            'native_res_m': float(r.source_native_resolution_m),
            'valid_coverage_pct': float(r.valid_coverage_pct),
            'nodata_pixels': int(r.nodata_pixels),
            'protocol': PROTOCOLO,
            **{c: float(r[c]) for c in ZEUS_COLS},
            'mean_slope_deg': float(r.mean_slope_deg),
            'roughness_m': float(r.roughness_m),
            'relative_relief_m': float(r.relative_relief_m),
            # Em v1_3_1 a rugosidade "atual" é a própria versão legada (com tendência).
            'roughness_legacy_mean_m': float(r.roughness_m),
            'roughness_legacy_median_m': float(r.median_roughness_m),
            'roughness_legacy_p90_m': float(r.p90_roughness_m),
        })
    return pd.DataFrame(linhas, columns=COMPLETA_COLS), notas


def checar_reproducao(completa_lida: pd.DataFrame, orig: pd.DataFrame) -> tuple[list[str], bool]:
    """1) CSV gravado == CSV original (round-trip); compara as 8 features + cobertura."""
    mapa = {'mean_slope_deg': 'mean_slope_deg', 'roughness_m': 'roughness_m',
            'relative_relief_m': 'relative_relief_m', 'median_slope_deg': 'median_slope_deg',
            'p90_slope_deg': 'p90_slope_deg', 'median_roughness_m': 'median_roughness_m',
            'p90_roughness_m': 'p90_roughness_m', 'robust_relief_p95_p5_m': 'robust_relief_p95_p5_m',
            'roughness_legacy_mean_m': 'roughness_m', 'roughness_legacy_median_m': 'median_roughness_m',
            'roughness_legacy_p90_m': 'p90_roughness_m', 'valid_coverage_pct': 'valid_coverage_pct',
            'nodata_pixels': 'nodata_pixels', 'native_res_m': 'source_native_resolution_m'}
    o = orig.set_index('region_id')
    c = completa_lida.set_index('site_id')
    ok = list(c.index) == list(o.index)
    piores = []
    for novo, velho in mapa.items():
        d = np.abs(c[novo].to_numpy(float) - o.loc[c.index, velho].to_numpy(float))
        rel = d / np.maximum(np.abs(o.loc[c.index, velho].to_numpy(float)), 1e-12)
        piores.append((novo, velho, float(d.max()), float(rel.max())))
        ok &= bool((rel <= 1e-12).all() | (d <= 1e-12).all())
    tab = pd.DataFrame(piores, columns=['coluna_nova', 'coluna_original', 'max_abs_diff', 'max_rel_diff'])
    txt = ['### 1. Tabela gravada × `terrain_features_v1_3_1.csv` original (45 linhas)', '',
           f'Mesma ordem e mesmos IDs: **{list(c.index) == list(o.index)}**. '
           f'Resultado: **{"REPRODUZ" if ok else "DIVERGE"}** (tolerância relativa 1e-12).', '',
           tab.to_markdown(index=False), '']
    return txt, ok


def checar_recalculo(orig: pd.DataFrame) -> tuple[list[str], bool, list[str]]:
    """2) Recalcula a partir dos DEMs brutos tudo o que não exige login (planetas + PGC)."""
    o = orig.set_index('region_id')
    feats = C.FEATURES
    linhas, erros = [], []
    alvos = [(i, 'planeta', p) for i, _n, _b, p, _s in C.PLANETA_CFG]
    pgc = [(i, 'pgc', None) for i in o.index[o.source_dataset.str.startswith('PGC')]]
    for ident, tipo, pattern in alvos + pgc:
        try:
            if tipo == 'planeta':
                dem, *_ = dem_planeta(procurar_planeta(pattern))
            else:
                dem, *_ = dem_terra(float(o.loc[ident, 'center_lat']), float(o.loc[ident, 'center_lon']))
            f = calcular_features(dem)
            rel = max(abs(f[c] - o.loc[ident, c]) / max(abs(o.loc[ident, c]), 1e-12) for c in feats)
            linhas.append((ident, o.loc[ident, 'source_dataset'], rel, rel <= 1e-6))
        except Exception as e:  # registra, não esconde
            erros.append(f'{ident}: {type(e).__name__}: {e}')
            linhas.append((ident, o.loc[ident, 'source_dataset'], np.nan, False))
    tab = pd.DataFrame(linhas, columns=['site_id', 'source_dataset', 'max_rel_diff_8_features', 'ok'])
    ok = bool(tab.ok.all())
    n_nasa = int((o.body == 'EARTH').sum() - len(pgc))
    txt = ['### 2. Recálculo a partir dos DEMs brutos com `src/` (sem login)', '',
           f'Resultado: **{"REPRODUZ" if ok else "DIVERGE/FALHOU"}** em {int(tab.ok.sum())}/{len(tab)} recortes '
           '(tolerância relativa 1e-6). '
           f'**Não verificados: {n_nasa} locais NASADEM** (exigem login Earthdata).', '',
           tab.to_markdown(index=False), '']
    return txt, ok, erros


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sem-recalculo', action='store_true')
    a = ap.parse_args()
    OUT_A.mkdir(parents=True, exist_ok=True)

    orig = ler_zip('terrain_features_v1_3_1.csv')
    status_orig = ler_zip('processing_status.csv')
    completa, notas_ll = montar(orig)
    zeus = completa[ZEUS_COLS].copy()

    falhas = validar(completa, zeus)
    completa.to_csv(OUT_A / 'tabela_completa.csv', index=False)
    zeus.to_csv(OUT_A / 'zeus_input.csv', index=False)
    completa_lida = pd.read_csv(OUT_A / 'tabela_completa.csv')
    zeus_lida = pd.read_csv(OUT_A / 'zeus_input.csv')
    falhas += [f'(após releitura) {x}' for x in validar(completa_lida, zeus_lida)]

    # Status por recorte (Fase A: nenhum recálculo de features, só herança do status original).
    st = status_orig.rename(columns={'region_id': 'site_id', 'name': 'site_name'})
    st['tile_id'] = st.site_id + '_r2c2'
    st['protocol'] = PROTOCOLO
    st = st[['tile_id', 'site_id', 'site_name', 'source', 'status', 'detail', 'protocol']]
    st.to_csv(OUT_A / 'processing_status.csv', index=False)

    notas = [
        'Fase A (provisória): os valores vêm do `terrain_features_v1_3_1.csv` original, sem recálculo.',
        '**A rugosidade ainda é a versão antiga (com tendência)**: `median_roughness_m`, `p90_roughness_m` e '
        '`roughness_m` são iguais às colunas `roughness_legacy_*`. Na V1.4 elas passam a ser sem tendência.',
        '**Lua e Marte têm só 1 linha cada.** Esta entrega é um teste de pipeline, não serve para achar análogos.',
        'Cada local é um único recorte central de 9×9 km (`tile_id` termina em `_r2c2`, que coincide com o recorte '
        'central da futura grade 3×3 da V1.4 quando o centro do local não muda).',
        'Convenção de longitude: graus, positiva para leste, normalizada em -180..180. '
        'Terra: WGS84 (coordenadas do `terra_por_local.csv`, que são o centro exato do recorte). '
        'Lua/Marte: planetocêntrica no CRS geodésico do GeoTIFF (esferas Mars 2000 e lunar).',
    ] + notas_ll
    escrever_dicionario(OUT_A / 'dicionario_colunas.md', PROTOCOLO, notas)

    rel = [f'# Relatório de qualidade — protocolo `{PROTOCOLO}` (Fase A, provisória)', '',
           '> **Avisos:** rugosidade ainda com tendência (versão antiga); Lua e Marte com 1 linha cada; '
           'teste de pipeline.', '',
           '## Validações obrigatórias', '']
    rel += ['- ' + ('**OK** — todas as validações passaram (colunas, numérico sem NaN, mesma contagem e ordem, '
                    'body/tipo válidos, tile_id único, lat/lon dentro dos limites).' if not falhas
                    else '**FALHAS:**\n' + '\n'.join(f'  - {x}' for x in falhas))]
    rel += [f'- Linhas: `tabela_completa.csv` = {len(completa_lida)}, `zeus_input.csv` = {len(zeus_lida)}.', '']
    rel += ['## Recortes descartados', '',
            'Nenhum. Os 45 recortes do V1.3.1 têm cobertura ≥ 99,9%. Recortes com NoData (aceitos):', '',
            completa_lida.loc[completa_lida.nodata_pixels > 0,
                              ['tile_id', 'valid_coverage_pct', 'nodata_pixels']].to_markdown(index=False), '']
    erros_st = st[st.status != 'OK']
    rel += ['## Locais com erro (processing_status original)', '',
            'Nenhum.' if erros_st.empty else erros_st.to_markdown(index=False), '']
    rel += secao_estatisticas(completa_lida)
    rel += ['## Verificação de reprodução do V1.3.1', '']
    txt, ok1 = checar_reproducao(completa_lida, orig)
    rel += txt
    if not a.sem_recalculo:
        txt, ok2, erros = checar_recalculo(orig)
        rel += txt
        if erros:
            rel += ['Erros no recálculo:', ''] + [f'- {e}' for e in erros] + ['']
    else:
        rel += ['### 2. Recálculo a partir dos DEMs brutos', '', '**Não executado** (`--sem-recalculo`).', '']
    (OUT_A / 'relatorio_qualidade.md').write_text('\n'.join(rel) + '\n', encoding='utf-8')

    ENTREGA.mkdir(exist_ok=True)
    for nome in ('zeus_input.csv', 'tabela_completa.csv', 'dicionario_colunas.md'):
        shutil.copy2(OUT_A / nome, ENTREGA / nome)

    print('\n'.join(notas_ll))
    print('Validações:', 'OK' if not falhas else falhas)
    print('Saídas em', OUT_A, '| cópias em', ENTREGA)
    return 0 if not falhas else 1


if __name__ == '__main__':
    raise SystemExit(main())

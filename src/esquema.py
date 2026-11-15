"""Esquema estável das tabelas de entrega (iguais entre V1.3.1 e V1.4) e validações."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ZEUS_COLS = [
    'median_slope_deg', 'p90_slope_deg', 'median_roughness_m',
    'p90_roughness_m', 'robust_relief_p95_p5_m',
]
ID_COLS = [
    'tile_id', 'site_id', 'site_name', 'body', 'tipo', 'lat', 'lon',
    'source_dataset', 'native_res_m', 'valid_coverage_pct', 'nodata_pixels', 'protocol',
]
EXTRA_COLS = [
    'mean_slope_deg', 'roughness_m', 'relative_relief_m',
    'roughness_legacy_mean_m', 'roughness_legacy_median_m', 'roughness_legacy_p90_m',
]
COMPLETA_COLS = ID_COLS + ZEUS_COLS + EXTRA_COLS

# --- v1_5: cobertura superficial (ESA WorldCover 2021 na Terra; atribuída na Lua/Marte) ---
WORLDCOVER_CLASSES = {  # código WorldCover -> coluna
    10: 'frac_arvore', 20: 'frac_arbusto', 30: 'frac_campo', 40: 'frac_agricultura', 50: 'frac_construido',
    60: 'frac_solo_exposto', 70: 'frac_neve_gelo', 80: 'frac_agua', 90: 'frac_area_umida', 95: 'frac_mangue',
    100: 'frac_musgo_liquen',
}
VEGETACAO = ['frac_arvore', 'frac_arbusto', 'frac_campo', 'frac_agricultura', 'frac_area_umida', 'frac_mangue',
             'frac_musgo_liquen']
COBERTURA_ZEUS = ['frac_solo_exposto', 'frac_neve_gelo', 'frac_vegetacao', 'frac_construido']
COBERTURA_COLS = COBERTURA_ZEUS + list(WORLDCOVER_CLASSES.values()) + ['cover_source']
COBERTURA_COLS = list(dict.fromkeys(COBERTURA_COLS))       # sem duplicatas, ordem estável
ZEUS_COLS_V15 = ZEUS_COLS + COBERTURA_ZEUS
COMPLETA_COLS_V15 = ID_COLS + ZEUS_COLS + COBERTURA_ZEUS + EXTRA_COLS + \
    [c for c in COBERTURA_COLS if c not in COBERTURA_ZEUS]

# --- v1_6: temperatura da superfície (K) ---
TEMP_ZEUS = ['t_sup_media_K', 't_sup_max_K']
ZEUS_COLS_V16 = ZEUS_COLS_V15 + TEMP_ZEUS
COMPLETA_COLS_V16 = ID_COLS + ZEUS_COLS_V16 + EXTRA_COLS + \
    [c for c in COBERTURA_COLS if c not in COBERTURA_ZEUS] + ['temp_fonte', 'temp_escala']
DICIONARIO_TEMPERATURA = [
    ('t_sup_media_K', 'Temperatura média anual da SUPERFÍCIE (não do ar). Terra: NASA POWER, climatologia da '
     'temperatura de pele (TS) da reanálise MERRA-2 (~0,5°×0,625°), no ponto do local. Lua: Diviner PRP '
     '(LRO), média anual de modelo térmico ajustado às observações, média dos triângulos (~0,5 km) dentro do '
     'recorte. Marte: modelo climático Legacy da NASA Ames (tsurf, 5°×6°), média de 4 trechos de 10 sóis em '
     'Ls 0/90/180/270, interpolada no ponto do local.', 'K', 'NASA POWER / LRO Diviner / NASA Ames MGCM'),
    ('t_sup_max_K', 'Temperatura máxima anual da superfície. Terra: TS_MAX (máximo horário da climatologia). '
     'Lua: máxima anual do Diviner PRP. Marte: maior valor nas 4 estações amostradas (subestima levemente o '
     'extremo anual).', 'K', 'idem'),
    ('temp_fonte', 'Produto de origem da temperatura.', '—', 'gerado'),
    ('temp_escala', '`recorte` (valor próprio de cada recorte: Lua) ou `local` (um valor por local, repetido nos '
     'recortes: Terra e Marte, porque a fonte é regional).', '—', 'gerado'),
]

# --- v1_7: geologia (classe litológica harmonizada, one-hot) ---
LITO_ZEUS = ['lito_vulcanica', 'lito_cristalina', 'lito_sedimentar', 'lito_evaporitica', 'lito_gelo',
             'lito_impacto_terras_altas']
ZEUS_COLS_V17 = ZEUS_COLS_V16 + LITO_ZEUS
COMPLETA_COLS_V17 = ID_COLS + ZEUS_COLS_V17 + [c for c in COMPLETA_COLS_V16 if c not in ID_COLS + ZEUS_COLS_V16] + \
    ['lito_classe', 'geo_unidade', 'geo_litologia', 'geo_fonte']
DICIONARIO_GEOLOGIA = [
    ('lito_vulcanica … lito_impacto_terras_altas', 'One-hot da classe litológica harmonizada no centro do '
     'recorte (1 = é a classe; todas 0 = misto/indefinido ou não classificado).', '0/1', 'derivado de lito_classe'),
    ('lito_classe', 'Classe harmonizada: `vulcanica` (basalto, lavas, tufos), `cristalina` (intrusivas e '
     'metamórficas), `sedimentar` (clásticas e carbonáticas), `evaporitica` (evaporitos, salares), `gelo`, '
     '`impacto_terras_altas` (crateras/bacias da Lua; terras altas e unidade de impacto de Marte), '
     '`misto_indefinido`, `nao_classificado`.', '—', 'regras em src/geologia.py'),
    ('geo_unidade', 'Unidade geológica de origem (nome no mapa-fonte).', '—',
     'Macrostrat / USGS Lua 1:5M / USGS Marte SIM 3292'),
    ('geo_litologia', 'Litologia declarada pela fonte (só Terra/Macrostrat).', '—', 'Macrostrat'),
    ('geo_fonte', 'Mapa de origem e escala.', '—', 'gerado'),
]

DICIONARIO_COBERTURA = [
    ('frac_solo_exposto', 'Fração do recorte em solo exposto/vegetação esparsa (WorldCover classe 60). '
     'Lua e Marte: 1 (atribuído).', 'fração 0–1', 'ESA WorldCover 10 m v200 (2021)'),
    ('frac_neve_gelo', 'Fração em neve e gelo permanentes (classe 70). Lua/Marte: 0 (atribuído; gelo em crateras '
     'polares sombreadas não é cobertura visível).', 'fração 0–1', 'ESA WorldCover'),
    ('frac_vegetacao', 'Soma das classes de vegetação (10, 20, 30, 40, 90, 95, 100). Lua/Marte: 0.', 'fração 0–1',
     'ESA WorldCover'),
    ('frac_construido', 'Fração construída/urbana (classe 50). Lua/Marte: 0.', 'fração 0–1', 'ESA WorldCover'),
    ('frac_arvore … frac_musgo_liquen', 'Fração de cada uma das 11 classes WorldCover (10 árvores, 20 arbustos, '
     '30 campo, 40 agricultura, 50 construído, 60 solo exposto, 70 neve/gelo, 80 água, 90 área úmida, '
     '95 mangue, 100 musgo/líquen). Somam 1 nos pixels com dado.', 'fração 0–1', 'ESA WorldCover'),
    ('cover_source', '`worldcover` (medido), `atribuido_corpo_sem_vegetacao` (Lua/Marte) ou '
     '`atribuido_manto_de_gelo` (interior da Antártida, fora da cobertura do WorldCover).', '—', 'gerado'),
]

BODIES = {'EARTH', 'MOON', 'MARS'}
TIPOS = {'candidato', 'controle', 'alvo'}
TIPO_MAP = {'analogo': 'candidato', 'candidato': 'candidato', 'controle': 'controle', 'alvo': 'alvo'}

DICIONARIO = [
    # coluna, definição, unidade, fonte
    ('tile_id', 'Identificador único do recorte 9×9 km: `{site_id}_r{linha}c{coluna}` (linhas/colunas 1..3 na grade 3×3 '
     'de 27 km; o recorte central `r2c2` é o recorte de 9 km centrado no ponto do local).', '—', 'gerado'),
    ('site_id', 'Identificador do local (Terra: `earth_` + nome normalizado; alvos: id do alvo).', '—',
     'terra_por_local.csv / alvos'),
    ('site_name', 'Nome legível do local.', '—', 'terra_por_local.csv / alvos'),
    ('body', 'Corpo celeste: EARTH, MOON ou MARS.', '—', 'gerado'),
    ('tipo', 'candidato (análogo candidato), controle (local comum, p.ex. cidade/floresta, para checar falsos '
     'análogos) ou alvo (local lunar/marciano de referência). `analogo` do CSV original foi mapeado para `candidato`.',
     '—', 'terra_por_local.csv'),
    ('lat', 'Latitude do centro do recorte. Terra: WGS84. Lua/Marte: planetocêntrica no CRS geodésico do próprio '
     'corpo (esfera de referência do GeoTIFF), calculada do centro do recorte.', 'graus', 'calculado'),
    ('lon', 'Longitude do centro do recorte, positiva para leste, normalizada para -180..180. Mesma regra de CRS de `lat`.',
     'graus', 'calculado'),
    ('source_dataset', 'Produto DEM de origem.', '—', 'metadados do processamento'),
    ('native_res_m', 'Resolução nativa do DEM de origem (antes do regradeamento para 40 m).', 'm',
     'metadados do raster'),
    ('valid_coverage_pct', 'Porcentagem de pixels com elevação válida no recorte (mínimo aceito 99,9%).', '%',
     'calculado'),
    ('nodata_pixels', 'Número de pixels sem dado no recorte de 225×225.', 'pixels', 'calculado'),
    ('protocol', 'Versão do protocolo de cálculo (`v1_3_1` ou `v1_4`). Valores de versões diferentes não são '
     'comparáveis numericamente.', '—', 'gerado'),
    ('median_slope_deg', 'Mediana da declividade (np.gradient sobre DEM suavizado com gaussiano σ=1 px, grade 40 m).',
     'graus', 'calculado do DEM'),
    ('p90_slope_deg', 'Percentil 90 da declividade.', 'graus', 'calculado do DEM'),
    ('median_roughness_m', 'Mediana da rugosidade. V1.3.1: DP local 5×5 do DEM suavizado (inclui a rampa/tendência). '
     'V1.4: DP local 5×5 do resíduo gauss(σ=1) − gauss(σ=5) (sem tendência).', 'm', 'calculado do DEM'),
    ('p90_roughness_m', 'Percentil 90 da rugosidade (mesma definição de `median_roughness_m`).', 'm',
     'calculado do DEM'),
    ('robust_relief_p95_p5_m', 'Relevo robusto: percentil 95 − percentil 5 das elevações válidas originais.', 'm',
     'calculado do DEM'),
    ('mean_slope_deg', 'Média da declividade.', 'graus', 'calculado do DEM'),
    ('roughness_m', 'Média da rugosidade (mesma definição de `median_roughness_m` na versão do protocolo).', 'm',
     'calculado do DEM'),
    ('relative_relief_m', 'Relevo relativo: elevação máxima − mínima (sensível a outliers).', 'm',
     'calculado do DEM'),
    ('roughness_legacy_mean_m', 'Média da rugosidade antiga (V1.3.1, com tendência). Em `v1_3_1` é igual a '
     '`roughness_m`.', 'm', 'calculado do DEM'),
    ('roughness_legacy_median_m', 'Mediana da rugosidade antiga (com tendência).', 'm', 'calculado do DEM'),
    ('roughness_legacy_p90_m', 'Percentil 90 da rugosidade antiga (com tendência).', 'm', 'calculado do DEM'),
]


def validar(completa: pd.DataFrame, zeus: pd.DataFrame, cols_completa=None, cols_zeus=None) -> list[str]:
    """Retorna lista de falhas (vazia = tudo certo)."""
    cols_completa = COMPLETA_COLS if cols_completa is None else cols_completa
    cols_zeus = ZEUS_COLS if cols_zeus is None else cols_zeus
    f = []
    if list(completa.columns) != cols_completa:
        f.append(f'colunas da tabela completa fora do esquema: {list(completa.columns)}')
    if list(zeus.columns) != cols_zeus:
        f.append(f'colunas do zeus_input fora do esquema: {list(zeus.columns)}')
    if not all(pd.api.types.is_numeric_dtype(zeus[c]) for c in zeus.columns):
        f.append('zeus_input tem coluna não numérica')
    if zeus.isna().any().any() or not np.isfinite(zeus.to_numpy(dtype=float)).all():
        f.append('zeus_input tem NaN/infinito')
    if len(zeus) != len(completa):
        f.append(f'contagem de linhas difere: zeus={len(zeus)} completa={len(completa)}')
    elif not np.array_equal(zeus.to_numpy(dtype=float), completa[cols_zeus].to_numpy(dtype=float)):
        f.append('zeus_input não corresponde às colunas da tabela completa na mesma ordem')
    if not set(completa.body).issubset(BODIES):
        f.append(f'body inválido: {set(completa.body) - BODIES}')
    if not set(completa.tipo).issubset(TIPOS):
        f.append(f'tipo inválido: {set(completa.tipo) - TIPOS}')
    if completa.tile_id.duplicated().any():
        f.append(f'tile_id duplicado: {completa.tile_id[completa.tile_id.duplicated()].tolist()}')
    if completa[['lat', 'lon']].isna().any().any():
        f.append('lat/lon vazias')
    if not completa.lat.between(-90, 90).all() or not completa.lon.between(-180, 180).all():
        f.append('lat/lon fora de [-90,90]/[-180,180]')
    return f


def escrever_dicionario(path: Path, protocolo: str, notas: list[str], cols_zeus=None, extra=None):
    cols_zeus = ZEUS_COLS if cols_zeus is None else cols_zeus
    linhas = [f'# Dicionário de colunas — protocolo `{protocolo}`', '',
              'Uma linha = um recorte de 9×9 km em grade de 40 m (225×225 px). '
              '`zeus_input.csv` e `tabela_completa.csv` têm as mesmas linhas na mesma ordem.', '',
              '`zeus_input.csv` contém apenas: ' + ', '.join(f'`{c}`' for c in cols_zeus) + '.', '',
              '| coluna | definição | unidade | fonte |', '|---|---|---|---|']
    for c, d, u, s in DICIONARIO + (extra or []):
        linhas.append(f'| `{c}` | {d} | {u} | {s} |')
    if notas:
        linhas += ['', '## Notas desta versão', ''] + [f'- {n}' for n in notas]
    path.write_text('\n'.join(linhas) + '\n', encoding='utf-8')


def secao_estatisticas(completa: pd.DataFrame) -> list[str]:
    out = ['## Linhas por corpo e tipo', '',
           completa.groupby(['body', 'tipo']).size().rename('linhas').reset_index().to_markdown(index=False), '']
    out += ['## Estatísticas das features por corpo', '']
    feats = ZEUS_COLS + ['mean_slope_deg', 'roughness_m', 'relative_relief_m']
    for c in feats:
        st = completa.groupby('body')[c].describe()[['count', 'mean', 'std', 'min', '50%', 'max']]
        out += [f'### `{c}`', '', st.round(4).to_markdown(), '']
    out += ['## Correlação de Pearson entre features (todas as linhas)', '',
            completa[feats].corr().round(3).to_markdown(), '']
    terra = completa[completa.body == 'EARTH']
    out += ['## Correlação de Pearson entre features (só Terra)', '',
            terra[feats].corr().round(3).to_markdown(), '']
    return out

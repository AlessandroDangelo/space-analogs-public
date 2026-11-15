"""Parâmetros do protocolo V1.3.1 (copiados do notebook DadosTerra.ipynb, célula 2).

Mudanças em relação ao notebook (só caminhos, nenhum parâmetro numérico):
- BASE é a raiz do repositório (não /content do Colab);
- entradas são lidas de `entrada/` e o cache NASADEM fica em `cache/nasadem/`;
- saídas vão para `outputs/`.
"""
from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ENTRADA = BASE / 'entrada'
OUTPUTS = BASE / 'outputs'
CSV_LOCAIS = ENTRADA / 'terra_por_local.csv'
OUT = OUTPUTS / 'space_analogs_output_v1_3_1'
CACHE_NASADEM = BASE / 'cache' / 'nasadem'
# Alvos planetários: alvos_v2.csv (centros de Marte conferidos em fontes) substitui alvos.csv, que fica
# intacto em entrada/ (regra: não sobrescrever entradas).
ALVOS_CSV = ENTRADA / ('alvos_v2.csv' if (ENTRADA / 'alvos_v2.csv').is_file() else 'alvos.csv')

RES_M = 40                          # >=32m do DEM polar, evita upsampling nominal
N = 225                             # 225 x 40 = 9.000 metros
SIGMA_PX = 1.0
RUGOSIDADE_JANELA = 5
BORDA_PX = 3
RAIO_EXCLUSAO_NODATA = 7            # raio efetivo dos filtros locais (Gauss 4 + STD 2 + gradiente 1)
MIN_VALID_PCT = 99.9                # aceita no máximo 0,1% de lacunas; registra e exclui seu entorno
SALVAR_RECORTE_TIF = True           # 225x225 / ~200 kB cada, compressão DEFLATE
BAIXAR_NASADEM = True
PROCESSAR_PLANETAS = True

STAC_PGC = 'https://stac.pgc.umn.edu/api/v1/'
PGC_ARCTIC = 'arcticdem-mosaics-v4.1-32m'
PGC_REMA = 'rema-mosaics-v2.0-32m'

FEATURES = [
    'mean_slope_deg', 'roughness_m', 'relative_relief_m',
    'median_slope_deg', 'p90_slope_deg', 'median_roughness_m',
    'p90_roughness_m', 'robust_relief_p95_p5_m'
]
FEATURES_CLUSTER = ['median_slope_deg', 'median_roughness_m', 'robust_relief_p95_p5_m']

# Comparações exploratórias: constantes de tolerância NÃO validadas.
METODOS = {
    'medias_extremos': (['mean_slope_deg', 'roughness_m', 'relative_relief_m'], [2, 2, 150]),
    'medianas_robusto': (FEATURES_CLUSTER, [2, 2, 150]),
    'p90_robusto': (['p90_slope_deg', 'median_roughness_m', 'robust_relief_p95_p5_m'], [5, 2, 150]),
    'sem_rugosidade': (['p90_slope_deg', 'robust_relief_p95_p5_m'], [5, 150]),
}

# Alvos planetários do V1.3.1 (padrão glob procurado em ENTRADA).
PLANETA_CFG = [
    ('mars_001', 'Jezero — recorte central', 'MARS', '*M20_JezeroCrater_CTXDEM_20m*.tif',
     'USGS Mars 2020 CTX DEM 20m'),
    ('moon_001', 'Connecting Ridge — recorte central', 'MOON', '*Site01_final_adj_5mpp_surf*.tif',
     'NASA LOLA Site01 DEM 5m'),
]

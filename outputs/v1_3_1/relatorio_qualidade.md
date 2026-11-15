# Relatório de qualidade — protocolo `v1_3_1` (Fase A, provisória)

> **Avisos:** rugosidade ainda com tendência (versão antiga); Lua e Marte com 1 linha cada; teste de pipeline.

## Validações obrigatórias

- **OK** — todas as validações passaram (colunas, numérico sem NaN, mesma contagem e ordem, body/tipo válidos, tile_id único, lat/lon dentro dos limites).
- Linhas: `tabela_completa.csv` = 45, `zeus_input.csv` = 45.

## Recortes descartados

Nenhum. Os 45 recortes do V1.3.1 têm cobertura ≥ 99,9%. Recortes com NoData (aceitos):

| tile_id                      |   valid_coverage_pct |   nodata_pixels |
|:-----------------------------|---------------------:|----------------:|
| earth_deserto_de_mojave_r2c2 |              99.9862 |               7 |
| earth_rub_al_khali_r2c2      |              99.9506 |              25 |
| earth_saara_tanezrouft_r2c2  |              99.9862 |               7 |

## Locais com erro (processing_status original)

Nenhum.

## Linhas por corpo e tipo

| body   | tipo      |   linhas |
|:-------|:----------|---------:|
| EARTH  | candidato |       38 |
| EARTH  | controle  |        5 |
| MARS   | alvo      |        1 |
| MOON   | alvo      |        1 |

## Estatísticas das features por corpo

### `median_slope_deg`

| body   |   count |    mean |      std |     min |     50% |     max |
|:-------|--------:|--------:|---------:|--------:|--------:|--------:|
| EARTH  |      43 |  7.3214 |   9.6159 |  0.0171 |  3.4369 | 40.6199 |
| MARS   |       1 |  1.1664 | nan      |  1.1664 |  1.1664 |  1.1664 |
| MOON   |       1 | 10.2956 | nan      | 10.2956 | 10.2956 | 10.2956 |

### `p90_slope_deg`

| body   |   count |    mean |      std |     min |     50% |     max |
|:-------|--------:|--------:|---------:|--------:|--------:|--------:|
| EARTH  |      43 | 16.3005 |  15.5446 |  0.0336 | 10.6805 | 55.4045 |
| MARS   |       1 |  3.0589 | nan      |  3.0589 |  3.0589 |  3.0589 |
| MOON   |       1 | 18.7096 | nan      | 18.7096 | 18.7096 | 18.7096 |

### `median_roughness_m`

| body   |   count |    mean |      std |     min |     50% |     max |
|:-------|--------:|--------:|---------:|--------:|--------:|--------:|
| EARTH  |      43 |  7.7517 |  10.9627 |  0.0165 |  3.4488 | 48.6657 |
| MARS   |       1 |  1.1369 | nan      |  1.1369 |  1.1369 |  1.1369 |
| MOON   |       1 | 10.1918 | nan      | 10.1918 | 10.1918 | 10.1918 |

### `p90_roughness_m`

| body   |   count |    mean |      std |     min |     50% |     max |
|:-------|--------:|--------:|---------:|--------:|--------:|--------:|
| EARTH  |      43 | 17.9832 |  20.0349 |  0.0293 | 10.4642 | 80.6734 |
| MARS   |       1 |  2.9321 | nan      |  2.9321 |  2.9321 |  2.9321 |
| MOON   |       1 | 19.1165 | nan      | 19.1165 | 19.1165 | 19.1165 |

### `robust_relief_p95_p5_m`

| body   |   count |     mean |     std |      min |      50% |       max |
|:-------|--------:|---------:|--------:|---------:|---------:|----------:|
| EARTH  |      43 | 504.745  | 691.501 |   1.4493 | 165.399  | 2647.4    |
| MARS   |       1 |  61.4541 | nan     |  61.4541 |  61.4541 |   61.4541 |
| MOON   |       1 | 888.861  | nan     | 888.861  | 888.861  |  888.861  |

### `mean_slope_deg`

| body   |   count |    mean |      std |     min |     50% |     max |
|:-------|--------:|--------:|---------:|--------:|--------:|--------:|
| EARTH  |      43 |  8.4754 |   9.2465 |  0.0245 |  5.3039 | 37.229  |
| MARS   |       1 |  1.5299 | nan      |  1.5299 |  1.5299 |  1.5299 |
| MOON   |       1 | 11.0209 | nan      | 11.0209 | 11.0209 | 11.0209 |

### `roughness_m`

| body   |   count |    mean |      std |     min |     50% |     max |
|:-------|--------:|--------:|---------:|--------:|--------:|--------:|
| EARTH  |      43 |  9.2318 |  11.2545 |  0.023  |  5.2406 | 48.5156 |
| MARS   |       1 |  1.487  | nan      |  1.487  |  1.487  |  1.487  |
| MOON   |       1 | 11.0829 | nan      | 11.0829 | 11.0829 | 11.0829 |

### `relative_relief_m`

| body   |   count |     mean |     std |       min |      50% |      max |
|:-------|--------:|---------:|--------:|----------:|---------:|---------:|
| EARTH  |      43 |  778.039 | 975.232 |    4.3568 |  352.796 | 3487.09  |
| MARS   |       1 |  147.582 | nan     |  147.582  |  147.582 |  147.582 |
| MOON   |       1 | 1201.96  | nan     | 1201.96   | 1201.96  | 1201.96  |

## Correlação de Pearson entre features (todas as linhas)

|                        |   median_slope_deg |   p90_slope_deg |   median_roughness_m |   p90_roughness_m |   robust_relief_p95_p5_m |   mean_slope_deg |   roughness_m |   relative_relief_m |
|:-----------------------|-------------------:|----------------:|---------------------:|------------------:|-------------------------:|-----------------:|--------------:|--------------------:|
| median_slope_deg       |              1     |           0.904 |                0.997 |             0.946 |                    0.943 |            0.981 |         0.988 |               0.94  |
| p90_slope_deg          |              0.904 |           1     |                0.891 |             0.986 |                    0.905 |            0.969 |         0.95  |               0.913 |
| median_roughness_m     |              0.997 |           0.891 |                1     |             0.942 |                    0.933 |            0.972 |         0.987 |               0.926 |
| p90_roughness_m        |              0.946 |           0.986 |                0.942 |             1     |                    0.93  |            0.985 |         0.983 |               0.93  |
| robust_relief_p95_p5_m |              0.943 |           0.905 |                0.933 |             0.93  |                    1     |            0.953 |         0.949 |               0.994 |
| mean_slope_deg         |              0.981 |           0.969 |                0.972 |             0.985 |                    0.953 |            1     |         0.995 |               0.956 |
| roughness_m            |              0.988 |           0.95  |                0.987 |             0.983 |                    0.949 |            0.995 |         1     |               0.947 |
| relative_relief_m      |              0.94  |           0.913 |                0.926 |             0.93  |                    0.994 |            0.956 |         0.947 |               1     |

## Correlação de Pearson entre features (só Terra)

|                        |   median_slope_deg |   p90_slope_deg |   median_roughness_m |   p90_roughness_m |   robust_relief_p95_p5_m |   mean_slope_deg |   roughness_m |   relative_relief_m |
|:-----------------------|-------------------:|----------------:|---------------------:|------------------:|-------------------------:|-----------------:|--------------:|--------------------:|
| median_slope_deg       |              1     |           0.904 |                0.997 |             0.946 |                    0.943 |            0.981 |         0.988 |               0.939 |
| p90_slope_deg          |              0.904 |           1     |                0.89  |             0.986 |                    0.906 |            0.969 |         0.95  |               0.913 |
| median_roughness_m     |              0.997 |           0.89  |                1     |             0.942 |                    0.933 |            0.972 |         0.987 |               0.926 |
| p90_roughness_m        |              0.946 |           0.986 |                0.942 |             1     |                    0.932 |            0.986 |         0.983 |               0.931 |
| robust_relief_p95_p5_m |              0.943 |           0.906 |                0.933 |             0.932 |                    1     |            0.953 |         0.95  |               0.994 |
| mean_slope_deg         |              0.981 |           0.969 |                0.972 |             0.986 |                    0.953 |            1     |         0.995 |               0.956 |
| roughness_m            |              0.988 |           0.95  |                0.987 |             0.983 |                    0.95  |            0.995 |         1     |               0.947 |
| relative_relief_m      |              0.939 |           0.913 |                0.926 |             0.931 |                    0.994 |            0.956 |         0.947 |               1     |

## Verificação de reprodução do V1.3.1

### 1. Tabela gravada × `terrain_features_v1_3_1.csv` original (45 linhas)

Mesma ordem e mesmos IDs: **True**. Resultado: **REPRODUZ** (tolerância relativa 1e-12).

| coluna_nova               | coluna_original            |   max_abs_diff |   max_rel_diff |
|:--------------------------|:---------------------------|---------------:|---------------:|
| mean_slope_deg            | mean_slope_deg             |              0 |              0 |
| roughness_m               | roughness_m                |              0 |              0 |
| relative_relief_m         | relative_relief_m          |              0 |              0 |
| median_slope_deg          | median_slope_deg           |              0 |              0 |
| p90_slope_deg             | p90_slope_deg              |              0 |              0 |
| median_roughness_m        | median_roughness_m         |              0 |              0 |
| p90_roughness_m           | p90_roughness_m            |              0 |              0 |
| robust_relief_p95_p5_m    | robust_relief_p95_p5_m     |              0 |              0 |
| roughness_legacy_mean_m   | roughness_m                |              0 |              0 |
| roughness_legacy_median_m | median_roughness_m         |              0 |              0 |
| roughness_legacy_p90_m    | p90_roughness_m            |              0 |              0 |
| valid_coverage_pct        | valid_coverage_pct         |              0 |              0 |
| nodata_pixels             | nodata_pixels              |              0 |              0 |
| native_res_m              | source_native_resolution_m |              0 |              0 |

### 2. Recálculo a partir dos DEMs brutos com `src/` (sem login)

Resultado: **REPRODUZ** em 12/12 recortes (tolerância relativa 1e-6). **Não verificados: 33 locais NASADEM** (exigem login Earthdata).

| site_id                      | source_dataset                 |   max_rel_diff_8_features | ok   |
|:-----------------------------|:-------------------------------|--------------------------:|:-----|
| mars_001                     | USGS Mars 2020 CTX DEM 20m     |               1.15622e-16 | True |
| moon_001                     | NASA LOLA Site01 DEM 5m        |               6.37263e-13 | True |
| earth_denali                 | PGC arcticdem-mosaics-v4.1-32m |               1.93002e-16 | True |
| earth_dome_argus             | PGC rema-mosaics-v2.0-32m      |               4.34859e-13 | True |
| earth_dome_c                 | PGC rema-mosaics-v2.0-32m      |               2.86105e-15 | True |
| earth_groenlandia_summit     | PGC arcticdem-mosaics-v4.1-32m |               9.75052e-16 | True |
| earth_ilha_devon_haughton    | PGC arcticdem-mosaics-v4.1-32m |               0           | True |
| earth_islandia_askja         | PGC arcticdem-mosaics-v4.1-32m |               1.38771e-16 | True |
| earth_oymyakon               | PGC arcticdem-mosaics-v4.1-32m |               1.64034e-16 | True |
| earth_svalbard_bockfjorden   | PGC arcticdem-mosaics-v4.1-32m |               3.44771e-12 | True |
| earth_vales_secos_de_mcmurdo | PGC rema-mosaics-v2.0-32m      |               1.7727e-16  | True |
| earth_vostok                 | PGC rema-mosaics-v2.0-32m      |               1.87074e-15 | True |


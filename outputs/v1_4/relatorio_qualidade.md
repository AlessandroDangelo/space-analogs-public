# Relatório de qualidade — protocolo `v1_4`

## Validações obrigatórias

- **OK** — colunas no esquema, `zeus_input` numérico sem NaN, mesma contagem e ordem, body/tipo válidos, `tile_id` único, lat/lon dentro dos limites.
- Linhas: `tabela_completa.csv` = 484, `zeus_input.csv` = 484.

## Recortes descartados

2 recortes.

| tile_id           | detail                                      |
|:------------------|:--------------------------------------------|
| earth_denali_r2c1 | cobertura 99.253% < 99.9% (378 px sem dado) |
| earth_denali_r3c1 | cobertura 99.378% < 99.9% (315 px sem dado) |

## Locais/alvos com erro

Nenhum.

## DTMs escolhidos (Marte, STAC)

| site_id          | detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|:-----------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| mars_gale        | P22_009505_1753_XI_04S222W__P22_009571_1756_XI_04S222W [dem]; 100 DTMs no ponto; testados pelos dados: P22_009716_1773_XI_02S223W__G04_019698_1747_XI_05S222W: 9 recortes válidos | P22_009650_1772_XI_02S222W__P22_009716_1773_XI_02S223W: 9 recortes válidos | P22_009650_1772_XI_02S222W__G04_019698_1747_XI_05S222W: 9 recortes válidos | P22_009716_1773_XI_02S223W__J09_048273_1747_XN_05S222W: 6 recortes válidos | P22_009650_1772_XI_02S222W__P02_001752_1753_XI_04S222W: 9 recortes válidos | P22_009505_1753_XI_04S222W__P22_009571_1756_XI_04S222W: 9 recortes válidos                       |
| mars_insight     | N06_064664_1859_XN_05N224W__K21_061684_1823_XN_02N224W [dem]; 100 DTMs no ponto; testados pelos dados: N06_064664_1859_XN_05N224W__N13_067632_1860_XI_06N224W: 9 recortes válidos | N04_063952_1856_XN_05N224W__N03_063385_1867_XI_06N224W: 1 recortes válidos | N06_064664_1859_XN_05N224W__K21_061684_1823_XN_02N224W: 9 recortes válidos | N06_064664_1859_XN_05N224W__N15_068239_1823_XN_02N224W: 9 recortes válidos | N13_067632_1860_XI_06N224W__N07_065218_1824_XN_02N224W: 4 recortes válidos | N13_067632_1860_XI_06N224W__K21_061684_1823_XN_02N224W: 9 recortes válidos                       |
| mars_oxia_planum | B01_009880_1977_XN_17N024W__P22_009735_1977_XN_17N024W [dtm]; 10 DTMs no ponto; testados pelos dados: B01_009880_1977_XN_17N024W__P22_009735_1977_XN_17N024W: 9 recortes válidos | J05_046934_1985_XN_18N025W__N05_064182_1985_XN_18N025W: 9 recortes válidos | N06_064538_1963_XN_16N024W__N06_064828_1963_XN_16N024W: 9 recortes válidos | J11_049215_1984_XN_18N024W__K12_058169_1985_XN_18N024W: 9 recortes válidos | N09_065936_1995_XN_19N025W__N10_066147_1995_XN_19N025W: 9 recortes válidos | K20_061136_1986_XN_18N024W__F21_044178_1988_XN_18N024W: 9 recortes válidos                        |
| mars_meridiani   | F13_040828_1778_XN_02S005W__F13_040973_1778_XN_02S005W [dtm]; 6 DTMs no ponto; testados pelos dados: G02_018912_1779_XN_02S005W__G04_019980_1779_XN_02S005W: 0 recortes válidos | K13_058564_1776_XN_02S005W__K14_058854_1776_XN_02S005W: 0 recortes válidos | D22_035909_1778_XN_02S005W__D21_035408_1772_XN_02S005W: 0 recortes válidos | F13_040828_1778_XN_02S005W__F13_040973_1778_XN_02S005W: 1 recortes válidos | B05_011765_1780_XN_02S005W__B08_012820_1779_XN_02S005W: 0 recortes válidos | G01_018701_1776_XN_02S005W__G02_018846_1791_XN_00S005W: 0 recortes válidos                         |
| mars_gusev       | P07_003900_1653_XI_14S184W__G01_018523_1653_XI_14S184W [dem]; 100 DTMs no ponto; testados pelos dados: P14_006524_1654_XN_14S184W__K05_055458_1653_XN_14S184W: RasterioIOError: HTTP response code: 404 | P14_006524_1654_XN_14S184W__F20_043551_1654_XN_14S184W: 7 recortes válidos | P07_003900_1653_XI_14S184W__G01_018523_1653_XI_14S184W: 8 recortes válidos | P07_003900_1653_XI_14S184W__J01_045318_1653_XN_14S184W: 8 recortes válidos | P14_006524_1654_XN_14S184W__D20_034874_1653_XN_14S184W: 5 recortes válidos | P14_006524_1654_XN_14S184W__G03_019301_1652_XI_14S184W: 6 recortes válidos |

## Recortes por local (alvos)

| body   | site_id                  |   recortes |
|:-------|:-------------------------|-----------:|
| MARS   | mars_gale                |          9 |
| MARS   | mars_gusev               |          8 |
| MARS   | mars_insight             |          9 |
| MARS   | mars_jezero              |          9 |
| MARS   | mars_meridiani           |          1 |
| MARS   | mars_oxia_planum         |          9 |
| MOON   | moon_connecting_ridge    |          9 |
| MOON   | moon_de_gerlache_rim     |          9 |
| MOON   | moon_haworth             |          9 |
| MOON   | moon_malapert_massif     |          9 |
| MOON   | moon_mons_mouton_plateau |          9 |
| MOON   | moon_nobile_rim_2        |          9 |

## Linhas por corpo e tipo

| body   | tipo      |   linhas |
|:-------|:----------|---------:|
| EARTH  | candidato |      340 |
| EARTH  | controle  |       45 |
| MARS   | alvo      |       45 |
| MOON   | alvo      |       54 |

## Estatísticas das features por corpo

### `median_slope_deg`

| body   |   count |    mean |    std |    min |     50% |     max |
|:-------|--------:|--------:|-------:|-------:|--------:|--------:|
| EARTH  |     385 |  6.0663 | 7.4498 | 0      |  3.3953 | 40.6099 |
| MARS   |      45 |  2.8794 | 3.0063 | 0.7791 |  1.6857 | 12.3912 |
| MOON   |      54 | 12.9094 | 4.4649 | 5.2639 | 12.5239 | 23.5319 |

### `p90_slope_deg`

| body   |   count |    mean |     std |    min |     50% |     max |
|:-------|--------:|--------:|--------:|-------:|--------:|--------:|
| EARTH  |     385 | 14.0154 | 13.0354 | 0.0319 |  9.2341 | 55.348  |
| MARS   |      45 |  6.0164 |  5.3343 | 1.4068 |  3.8839 | 18.2801 |
| MOON   |      54 | 19.7932 |  4.9088 | 9.9134 | 19.1837 | 32.8903 |

### `median_roughness_m`

| body   |   count |   mean |    std |    min |    50% |     max |
|:-------|--------:|-------:|-------:|-------:|-------:|--------:|
| EARTH  |     385 | 2.7635 | 2.8418 | 0      | 1.7016 | 13.3166 |
| MARS   |      45 | 1.1194 | 0.5812 | 0.3297 | 1.0322 |  2.8364 |
| MOON   |      54 | 1.1067 | 0.1609 | 0.7169 | 1.0941 |  1.436  |

### `p90_roughness_m`

| body   |   count |   mean |    std |    min |    50% |     max |
|:-------|--------:|-------:|-------:|-------:|-------:|--------:|
| EARTH  |     385 | 7.5863 | 7.1128 | 0.0077 | 5.5297 | 33.6679 |
| MARS   |      45 | 2.5441 | 1.565  | 0.6719 | 2.0788 |  7.6524 |
| MOON   |      54 | 2.6385 | 0.6104 | 1.386  | 2.6412 |  4.3392 |

### `robust_relief_p95_p5_m`

| body   |   count |     mean |     std |      min |       50% |     max |
|:-------|--------:|---------:|--------:|---------:|----------:|--------:|
| EARTH  |     385 |  418.673 | 522.947 |   1.4493 |  181.947  | 2993.47 |
| MARS   |      45 |  282.229 | 440.746 |  22.1579 |   83.4957 | 1728.7  |
| MOON   |      54 | 1548.99  | 660.462 | 439.468  | 1379.47   | 3350.02 |

### `mean_slope_deg`

| body   |   count |    mean |    std |    min |     50% |     max |
|:-------|--------:|--------:|-------:|-------:|--------:|--------:|
| EARTH  |     385 |  7.1685 | 7.3248 | 0.0193 |  4.8439 | 37.0979 |
| MARS   |      45 |  3.3198 | 3.1413 | 0.8277 |  2.0253 | 12.1802 |
| MOON   |      54 | 13.0007 | 4.0553 | 5.6972 | 12.5534 | 23.055  |

### `roughness_m`

| body   |   count |   mean |    std |    min |    50% |     max |
|:-------|--------:|-------:|-------:|-------:|-------:|--------:|
| EARTH  |     385 | 3.646  | 3.4162 | 0.0051 | 2.6219 | 15.4066 |
| MARS   |      45 | 1.3944 | 0.7382 | 0.4141 | 1.2261 |  3.6802 |
| MOON   |      54 | 1.4456 | 0.2643 | 0.8301 | 1.4242 |  2.0666 |

### `relative_relief_m`

| body   |   count |     mean |     std |      min |      50% |     max |
|:-------|--------:|---------:|--------:|---------:|---------:|--------:|
| EARTH  |     385 |  652.172 | 747.726 |   2.738  |  349.435 | 3657.87 |
| MARS   |      45 |  441.086 | 617.284 |  68.8699 |  153.487 | 2167.42 |
| MOON   |      54 | 2148.35  | 789.815 | 673.448  | 2082.82  | 4141.81 |

## Correlação de Pearson entre features (todas as linhas)

|                        |   median_slope_deg |   p90_slope_deg |   median_roughness_m |   p90_roughness_m |   robust_relief_p95_p5_m |   mean_slope_deg |   roughness_m |   relative_relief_m |
|:-----------------------|-------------------:|----------------:|---------------------:|------------------:|-------------------------:|-----------------:|--------------:|--------------------:|
| median_slope_deg       |              1     |           0.87  |                0.787 |             0.7   |                    0.838 |            0.975 |         0.762 |               0.855 |
| p90_slope_deg          |              0.87  |           1     |                0.789 |             0.878 |                    0.746 |            0.953 |         0.858 |               0.787 |
| median_roughness_m     |              0.787 |           0.789 |                1     |             0.906 |                    0.413 |            0.802 |         0.973 |               0.453 |
| p90_roughness_m        |              0.7   |           0.878 |                0.906 |             1     |                    0.415 |            0.791 |         0.978 |               0.466 |
| robust_relief_p95_p5_m |              0.838 |           0.746 |                0.413 |             0.415 |                    1     |            0.842 |         0.43  |               0.983 |
| mean_slope_deg         |              0.975 |           0.953 |                0.802 |             0.791 |                    0.842 |            1     |         0.819 |               0.868 |
| roughness_m            |              0.762 |           0.858 |                0.973 |             0.978 |                    0.43  |            0.819 |         1     |               0.478 |
| relative_relief_m      |              0.855 |           0.787 |                0.453 |             0.466 |                    0.983 |            0.868 |         0.478 |               1     |

## Correlação de Pearson entre features (só Terra)

|                        |   median_slope_deg |   p90_slope_deg |   median_roughness_m |   p90_roughness_m |   robust_relief_p95_p5_m |   mean_slope_deg |   roughness_m |   relative_relief_m |
|:-----------------------|-------------------:|----------------:|---------------------:|------------------:|-------------------------:|-----------------:|--------------:|--------------------:|
| median_slope_deg       |              1     |           0.872 |                0.928 |             0.846 |                    0.865 |            0.972 |         0.909 |               0.873 |
| p90_slope_deg          |              0.872 |           1     |                0.853 |             0.96  |                    0.845 |            0.958 |         0.933 |               0.871 |
| median_roughness_m     |              0.928 |           0.853 |                1     |             0.9   |                    0.716 |            0.923 |         0.971 |               0.734 |
| p90_roughness_m        |              0.846 |           0.96  |                0.9   |             1     |                    0.747 |            0.926 |         0.977 |               0.778 |
| robust_relief_p95_p5_m |              0.865 |           0.845 |                0.716 |             0.747 |                    1     |            0.891 |         0.756 |               0.98  |
| mean_slope_deg         |              0.972 |           0.958 |                0.923 |             0.926 |                    0.891 |            1     |         0.951 |               0.907 |
| roughness_m            |              0.909 |           0.933 |                0.971 |             0.977 |                    0.756 |            0.951 |         1     |               0.782 |
| relative_relief_m      |              0.873 |           0.871 |                0.734 |             0.778 |                    0.98  |            0.907 |         0.782 |               1     |

## Efeito da remoção de tendência

Correlação de Pearson entre declividade mediana e rugosidade (nova × legada), todas as linhas:

|                           |   median_slope_deg |   median_roughness_m |   roughness_legacy_median_m |
|:--------------------------|-------------------:|---------------------:|----------------------------:|
| median_slope_deg          |              1     |                0.787 |                       0.998 |
| median_roughness_m        |              0.787 |                1     |                       0.791 |
| roughness_legacy_median_m |              0.998 |                0.791 |                       1     |

## Comparação com o V1.3.1

Recorte central `r2c2` da V1.4 × recorte único da V1.3.1 (mesma grade de 40 m e mesmo DEM na Terra). Diferenças esperadas só por contexto de filtro nas bordas do recorte (V1.3.1 usava reflexão + 3 px de borda) e por eventual mudança de fonte.

| coluna_v1_4               | coluna_v1_3_1          |   n |   mediana_dif_rel |   max_dif_rel | site_max                 |
|:--------------------------|:-----------------------|----:|------------------:|--------------:|:-------------------------|
| median_slope_deg          | median_slope_deg       |  43 |          4.66e-03 |      4.84e-02 | earth_islandia_askja     |
| p90_slope_deg             | p90_slope_deg          |  43 |          5.08e-03 |      1.66e-01 | earth_oymyakon           |
| roughness_legacy_median_m | median_roughness_m     |  43 |          5.21e-03 |      5.17e-02 | earth_islandia_askja     |
| robust_relief_p95_p5_m    | robust_relief_p95_p5_m |  43 |          6.24e-04 |      4.68e-03 | earth_atacama_chajnantor |


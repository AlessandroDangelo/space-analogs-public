# Relatório de qualidade — protocolo `v1_5`

## Validações obrigatórias

- **OK** — esquema, `zeus_input` numérico sem NaN, mesma contagem e ordem, body/tipo válidos, `tile_id` único, lat/lon nos limites.
- Linhas: 484 (v1_4 tinha 484). Por corpo: EARTH=385, MOON=54, MARS=45.

## Recortes fora da v1_5 (cobertura pendente)

Nenhum.

## Origem da cobertura

| body   | cover_source                  |   recortes |
|:-------|:------------------------------|-----------:|
| EARTH  | aadc_afloramentos             |         36 |
| EARTH  | worldcover                    |        349 |
| MARS   | atribuido_corpo_sem_vegetacao |         45 |
| MOON   | atribuido_corpo_sem_vegetacao |         54 |

## Cobertura média por local (Terra)

| site_name                      | tipo      |   frac_solo_exposto |   frac_neve_gelo |   frac_vegetacao |   frac_construido |   frac_agua |
|:-------------------------------|:----------|--------------------:|-----------------:|-----------------:|------------------:|------------:|
| Aconcagua                      | candidato |               0.827 |            0.151 |            0.022 |             0     |       0.001 |
| Arkaroola                      | candidato |               0.019 |            0     |            0.981 |             0     |       0     |
| Atacama - Chajnantor           | candidato |               0.892 |            0     |            0.108 |             0     |       0     |
| Atacama - Yungay               | candidato |               0.998 |            0     |            0.002 |             0     |       0     |
| Bacia de Qaidam                | candidato |               1     |            0     |            0     |             0     |       0     |
| Danakil - Dallol               | candidato |               0.996 |            0     |            0.001 |             0     |       0.003 |
| Denali                         | candidato |               0.034 |            0.954 |            0.009 |             0     |       0.003 |
| Deserto de Lut                 | candidato |               1     |            0     |            0     |             0     |       0     |
| Deserto de Mojave              | candidato |               0.392 |            0     |            0.607 |             0.001 |       0     |
| Deserto de Simpson             | candidato |               0.35  |            0     |            0.65  |             0     |       0     |
| Dome Argus                     | candidato |               0     |            1     |            0     |             0     |       0     |
| Dome C                         | candidato |               0     |            1     |            0     |             0     |       0     |
| Everest                        | candidato |               0.221 |            0.696 |            0.077 |             0     |       0.006 |
| Gobi                           | candidato |               0.999 |            0     |            0.001 |             0     |       0     |
| Groenlandia - Summit           | candidato |               0     |            1     |            0     |             0     |       0     |
| Ilha Devon - Haughton          | candidato |               0.371 |            0.001 |            0.62  |             0     |       0.007 |
| Islandia - Askja               | candidato |               0.937 |            0.009 |            0.033 |             0     |       0.021 |
| Kilimanjaro                    | candidato |               0.21  |            0.003 |            0.786 |             0     |       0.001 |
| Ladakh                         | candidato |               0.827 |            0.007 |            0.151 |             0.011 |       0.005 |
| Lanzarote                      | candidato |               0.433 |            0     |            0.232 |             0.046 |       0.289 |
| Licancabur                     | candidato |               0.84  |            0     |            0.14  |             0     |       0.019 |
| Londres                        | controle  |               0     |            0     |            0.442 |             0.536 |       0.022 |
| Manaus                         | controle  |               0.008 |            0     |            0.499 |             0.241 |       0.252 |
| Mauna Loa - HI-SEAS            | candidato |               0.757 |            0     |            0.243 |             0     |       0     |
| Namibe                         | candidato |               0.962 |            0     |            0.038 |             0     |       0     |
| Nova York                      | controle  |               0.013 |            0     |            0.205 |             0.575 |       0.208 |
| Ojos del Salado                | candidato |               0.841 |            0.157 |            0.001 |             0     |       0     |
| Oymyakon                       | candidato |               0.003 |            0     |            0.984 |             0     |       0.013 |
| Pilbara                        | candidato |               0.018 |            0     |            0.982 |             0     |       0     |
| Planalto do Tibete - Changtang | candidato |               0.684 |            0     |            0.301 |             0     |       0.015 |
| Rio Tinto                      | candidato |               0.023 |            0     |            0.956 |             0.009 |       0.013 |
| Rub al Khali                   | candidato |               1     |            0     |            0     |             0     |       0     |
| Saara - Tanezrouft             | candidato |               1     |            0     |            0     |             0     |       0     |
| Salar de Uyuni                 | candidato |               1     |            0     |            0     |             0     |       0     |
| Sao Paulo                      | controle  |               0.003 |            0     |            0.191 |             0.8   |       0.006 |
| Singapura                      | controle  |               0.021 |            0     |            0.34  |             0.354 |       0.285 |
| Svalbard - Bockfjorden         | candidato |               0.237 |            0.479 |            0.073 |             0     |       0.211 |
| Teide                          | candidato |               0.186 |            0     |            0.777 |             0.021 |       0.015 |
| Utah - MDRS                    | candidato |               0.95  |            0     |            0.049 |             0.001 |       0     |
| Vale da Morte                  | candidato |               0.95  |            0     |            0.049 |             0.001 |       0     |
| Vales Secos de McMurdo         | candidato |               0.651 |            0.349 |            0     |             0     |       0     |
| Vostok                         | candidato |               0     |            1     |            0     |             0     |       0     |
| Wadi Rum                       | candidato |               0.989 |            0     |            0.009 |             0.002 |       0     |

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


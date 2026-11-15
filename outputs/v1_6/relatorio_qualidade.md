# Relatório de qualidade — protocolo `v1_6`

## Validações obrigatórias

- **OK** — esquema, `zeus_input` numérico sem NaN, mesma contagem e ordem, body/tipo válidos, `tile_id` único, lat/lon nos limites.
- Linhas: 484 (v1_5: 484). Por corpo: EARTH=385, MOON=54, MARS=45.

## Temperatura por local (média dos recortes)

| body   | site_name                               |   t_sup_media_K |   t_sup_max_K |
|:-------|:----------------------------------------|----------------:|--------------:|
| EARTH  | Dome Argus                              |           214.2 |         252.2 |
| EARTH  | Vostok                                  |           217.4 |         257.2 |
| EARTH  | Dome C                                  |           217.7 |         260   |
| EARTH  | Groenlandia - Summit                    |           242   |         273.2 |
| EARTH  | Vales Secos de McMurdo                  |           249.6 |         272   |
| EARTH  | Ilha Devon - Haughton                   |           258.3 |         290.4 |
| EARTH  | Oymyakon                                |           259   |         304.1 |
| EARTH  | Denali                                  |           261.4 |         281.9 |
| EARTH  | Svalbard - Bockfjorden                  |           265   |         276.5 |
| EARTH  | Islandia - Askja                        |           268.8 |         276.2 |
| EARTH  | Planalto do Tibete - Changtang          |           269.7 |         309   |
| EARTH  | Everest                                 |           270.7 |         296.7 |
| EARTH  | Ladakh                                  |           271.5 |         316.1 |
| EARTH  | Ojos del Salado                         |           271.9 |         311.8 |
| EARTH  | Aconcagua                               |           273.2 |         310.1 |
| EARTH  | Atacama - Chajnantor                    |           276.3 |         312.3 |
| EARTH  | Bacia de Qaidam                         |           278.3 |         322   |
| EARTH  | Gobi                                    |           281.1 |         328.6 |
| EARTH  | Salar de Uyuni                          |           281.4 |         312.5 |
| EARTH  | Londres                                 |           283.6 |         308.9 |
| EARTH  | Utah - MDRS                             |           285.3 |         326.2 |
| EARTH  | Nova York                               |           286.1 |         305   |
| EARTH  | Licancabur                              |           287.9 |         320.2 |
| EARTH  | Deserto de Mojave                       |           291.6 |         331   |
| EARTH  | Rio Tinto                               |           291.9 |         328.7 |
| EARTH  | Atacama - Yungay                        |           292.1 |         318.4 |
| EARTH  | Kilimanjaro                             |           292.3 |         314   |
| EARTH  | Vale da Morte                           |           292.7 |         332.4 |
| EARTH  | Wadi Rum                                |           292.9 |         330.6 |
| EARTH  | Mauna Loa - HI-SEAS                     |           293.1 |         308.3 |
| EARTH  | Sao Paulo                               |           293.2 |         318.8 |
| EARTH  | Arkaroola                               |           294.2 |         334.3 |
| EARTH  | Lanzarote                               |           294.4 |         304.6 |
| EARTH  | Teide                                   |           295   |         303.8 |
| EARTH  | Namibe                                  |           295.6 |         326.3 |
| EARTH  | Deserto de Simpson                      |           298.3 |         333.6 |
| EARTH  | Deserto de Lut                          |           299.2 |         337   |
| EARTH  | Singapura                               |           300.5 |         308.8 |
| EARTH  | Danakil - Dallol                        |           300.7 |         324.8 |
| EARTH  | Saara - Tanezrouft                      |           300.8 |         332.9 |
| EARTH  | Manaus                                  |           301   |         313.1 |
| EARTH  | Pilbara                                 |           302.3 |         337.8 |
| EARTH  | Rub al Khali                            |           303.4 |         333.5 |
| MARS   | Gusev (Spirit)                          |           218.6 |         293   |
| MARS   | Oxia Planum (ExoMars Rosalind Franklin) |           222.3 |         279.1 |
| MARS   | Jezero (Perseverance)                   |           223.7 |         285   |
| MARS   | Elysium Planitia (InSight)              |           223.8 |         284.1 |
| MARS   | Gale (Curiosity)                        |           224   |         285.8 |
| MARS   | Meridiani Planum (Opportunity)          |           227.5 |         291.9 |
| MOON   | de Gerlache Rim                         |           106.9 |         240   |
| MOON   | Haworth                                 |           107.5 |         239.8 |
| MOON   | Nobile Rim 2                            |           114.6 |         226.2 |
| MOON   | Mons Mouton Plateau                     |           117.7 |         250.4 |
| MOON   | Connecting Ridge                        |           117.9 |         249.3 |
| MOON   | Malapert Massif                         |           140.1 |         272.3 |

## Faixas por corpo

| body   |   ('t_sup_media_K', 'count') |   ('t_sup_media_K', 'mean') |   ('t_sup_media_K', 'std') |   ('t_sup_media_K', 'min') |   ('t_sup_media_K', '25%') |   ('t_sup_media_K', '50%') |   ('t_sup_media_K', '75%') |   ('t_sup_media_K', 'max') |   ('t_sup_max_K', 'count') |   ('t_sup_max_K', 'mean') |   ('t_sup_max_K', 'std') |   ('t_sup_max_K', 'min') |   ('t_sup_max_K', '25%') |   ('t_sup_max_K', '50%') |   ('t_sup_max_K', '75%') |   ('t_sup_max_K', 'max') |
|:-------|-----------------------------:|----------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|--------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|
| EARTH  |                          385 |                       279.1 |                       22.8 |                      214.2 |                      269.7 |                      286.1 |                      294.4 |                      303.4 |                        385 |                     309.3 |                     22.7 |                    252.2 |                    303.8 |                    312.5 |                    328.6 |                    337.8 |
| MARS   |                           45 |                       222.7 |                        2.1 |                      218.6 |                      222.3 |                      223.7 |                      223.8 |                      227.5 |                         45 |                     285.4 |                      4.5 |                    279.1 |                    284.1 |                    285   |                    285.8 |                    293   |
| MOON   |                           54 |                       117.4 |                       26.5 |                       56.6 |                      100.5 |                      117.5 |                      138.6 |                      175.5 |                         54 |                     246.3 |                     33.1 |                    114.5 |                    236.8 |                    248.8 |                    263.8 |                    310   |

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


# Relatório de qualidade — protocolo `v1_7`

## Validações obrigatórias

- **OK** — esquema, `zeus_input` numérico sem NaN, mesma contagem e ordem, body/tipo válidos, `tile_id` único, lat/lon nos limites.
- Linhas: 480 (v1_6: 484). Por corpo: EARTH=381, MOON=54, MARS=45.

## Classes por corpo (recortes)

| lito_classe          |   EARTH |   MARS |   MOON |
|:---------------------|--------:|-------:|-------:|
| cristalina           |      53 |      0 |      0 |
| evaporitica          |      19 |      0 |      0 |
| gelo                 |      39 |      0 |      0 |
| impacto_terras_altas |       0 |     21 |     54 |
| sedimentar           |     162 |     16 |      0 |
| vulcanica            |     108 |      8 |      0 |

## Classe predominante por local

| body   | site_name                               | classe               |   fracao | unidade                                                      |
|:-------|:----------------------------------------|:---------------------|---------:|:-------------------------------------------------------------|
| EARTH  | Aconcagua                               | vulcanica            |     0.67 | Cretaceous Volcano-sedimentary                               |
| EARTH  | Arkaroola                               | sedimentar           |     0.89 | Neoproterozoic sedimentary rocks                             |
| EARTH  | Atacama - Chajnantor                    | vulcanica            |     1    | Quaternary Andesitic and related                             |
| EARTH  | Atacama - Yungay                        | cristalina           |     0.89 | Cretaceous Granitic                                          |
| EARTH  | Bacia de Qaidam                         | sedimentar           |     1    | Cenozoic sedimentary rocks                                   |
| EARTH  | Danakil - Dallol                        | vulcanica            |     0.56 | volcanic                                                     |
| EARTH  | Denali                                  | gelo                 |     0.43 | ice                                                          |
| EARTH  | Deserto de Lut                          | sedimentar           |     1    | Cenozoic sedimentary rocks                                   |
| EARTH  | Deserto de Mojave                       | evaporitica          |     0.33 | Alluvium, lake, playa, and terrace deposits                  |
| EARTH  | Deserto de Simpson                      | sedimentar           |     1    | Cenozoic regolith                                            |
| EARTH  | Dome Argus                              | gelo                 |     1    | Phanerozoic ice                                              |
| EARTH  | Dome C                                  | gelo                 |     1    | Phanerozoic ice                                              |
| EARTH  | Everest                                 | cristalina           |     1    | Precambrian-Phanerozoic crystalline metamorphic rocks        |
| EARTH  | Gobi                                    | vulcanica            |     1    | Paleozoic sedimentary and volcanic rocks                     |
| EARTH  | Groenlandia - Summit                    | gelo                 |     1    | ice                                                          |
| EARTH  | Ilha Devon - Haughton                   | sedimentar           |     0.56 | Ordovician-Silurian sedimentary                              |
| EARTH  | Islandia - Askja                        | vulcanica            |     1    | Basalt, Holocene                                             |
| EARTH  | Kilimanjaro                             | vulcanica            |     1    | volcanic                                                     |
| EARTH  | Ladakh                                  | sedimentar           |     0.56 | Mesozoic-Cenozoic sedimentary rocks                          |
| EARTH  | Lanzarote                               | vulcanica            |     0.89 | mafic volcanic rocks                                         |
| EARTH  | Licancabur                              | vulcanica            |     1    | Quaternary Andesitic and related                             |
| EARTH  | Londres                                 | sedimentar           |     1    | Clastic sediment, Quaternary                                 |
| EARTH  | Manaus                                  | sedimentar           |     1    | Alter do Chão Formação                                       |
| EARTH  | Mauna Loa - HI-SEAS                     | vulcanica            |     1    | Lava flows                                                   |
| EARTH  | Namibe                                  | sedimentar           |     1    | sedimentary                                                  |
| EARTH  | Nova York                               | sedimentar           |     0.67 | Passaic Formation                                            |
| EARTH  | Ojos del Salado                         | vulcanica            |     1    | Neogene Andesitic and related                                |
| EARTH  | Oymyakon                                | sedimentar           |     1    | Sedimentary; Clastic: shallow marine                         |
| EARTH  | Pilbara                                 | vulcanica            |     0.78 | Archean mafic volcanics                                      |
| EARTH  | Planalto do Tibete - Changtang          | sedimentar           |     1    | Mesozoic sedimentary rocks                                   |
| EARTH  | Rio Tinto                               | cristalina           |     0.56 | volcanics and volcaniclastic rocks                           |
| EARTH  | Rub al Khali                            | sedimentar           |     1    | Cenozoic sedimentary rocks                                   |
| EARTH  | Saara - Tanezrouft                      | sedimentar           |     1    | sedimentary                                                  |
| EARTH  | Salar de Uyuni                          | evaporitica          |     1    | Quaternary Evaporitic                                        |
| EARTH  | Sao Paulo                               | sedimentar           |     0.78 | Resende Formação                                             |
| EARTH  | Singapura                               | sedimentar           |     1    | Mesozoic sedimentary rocks                                   |
| EARTH  | Svalbard - Bockfjorden                  | cristalina           |     0.44 | Supracrustal; Sedimentary and/or volcanic: undivided         |
| EARTH  | Teide                                   | vulcanica            |     1    | mafic volcanic rocks                                         |
| EARTH  | Utah - MDRS                             | sedimentar           |     0.89 | Tununk Shale Member, Ferron Sandstone Member, Blue Gate Shal |
| EARTH  | Vale da Morte                           | sedimentar           |     0.44 | Alluvium, lake, playa, and terrace deposits                  |
| EARTH  | Vales Secos de McMurdo                  | cristalina           |     0.89 | Paleozoic intrusive rocks                                    |
| EARTH  | Vostok                                  | gelo                 |     1    | Phanerozoic ice                                              |
| EARTH  | Wadi Rum                                | sedimentar           |     1    | Jordan                                                       |
| MARS   | Elysium Planitia (InSight)              | sedimentar           |     1    | eHt (Early Hesperian transition unit)                        |
| MARS   | Gale (Curiosity)                        | sedimentar           |     0.67 | Htu (Hesperian transition undivided unit)                    |
| MARS   | Gusev (Spirit)                          | vulcanica            |     1    | eHv (Early Hesperian volcanic unit)                          |
| MARS   | Jezero (Perseverance)                   | impacto_terras_altas |     1    | HNt (Hesperian and Noachian transition unit)                 |
| MARS   | Meridiani Planum (Opportunity)          | sedimentar           |     1    | HNhu (Hesperian and Noachian highland undivided unit)        |
| MARS   | Oxia Planum (ExoMars Rosalind Franklin) | impacto_terras_altas |     1    | lNh (Late Noachian highland unit)                            |
| MOON   | Connecting Ridge                        | impacto_terras_altas |     1    | pNb (Basin Undivided Unit)                                   |
| MOON   | Haworth                                 | impacto_terras_altas |     1    | pNb (Basin Undivided Unit)                                   |
| MOON   | Malapert Massif                         | impacto_terras_altas |     1    | pNbm (Basin Massif Unit)                                     |
| MOON   | Mons Mouton Plateau                     | impacto_terras_altas |     1    | pNb (Basin Undivided Unit)                                   |
| MOON   | Nobile Rim 2                            | impacto_terras_altas |     1    | pNc (Crater Unit)                                            |
| MOON   | de Gerlache Rim                         | impacto_terras_altas |     1    | Nc (Crater Unit)                                             |

## Linhas por corpo e tipo

| body   | tipo      |   linhas |
|:-------|:----------|---------:|
| EARTH  | candidato |      340 |
| EARTH  | controle  |       41 |
| MARS   | alvo      |       45 |
| MOON   | alvo      |       54 |

## Estatísticas das features por corpo

### `median_slope_deg`

| body   |   count |    mean |    std |    min |     50% |     max |
|:-------|--------:|--------:|-------:|-------:|--------:|--------:|
| EARTH  |     381 |  6.1224 | 7.4683 | 0      |  3.436  | 40.6099 |
| MARS   |      45 |  2.8794 | 3.0063 | 0.7791 |  1.6857 | 12.3912 |
| MOON   |      54 | 12.9094 | 4.4649 | 5.2639 | 12.5239 | 23.5319 |

### `p90_slope_deg`

| body   |   count |    mean |     std |    min |     50% |     max |
|:-------|--------:|--------:|--------:|-------:|--------:|--------:|
| EARTH  |     381 | 14.1234 | 13.0605 | 0.0319 |  9.3905 | 55.348  |
| MARS   |      45 |  6.0164 |  5.3343 | 1.4068 |  3.8839 | 18.2801 |
| MOON   |      54 | 19.7932 |  4.9088 | 9.9134 | 19.1837 | 32.8903 |

### `median_roughness_m`

| body   |   count |   mean |    std |    min |    50% |     max |
|:-------|--------:|-------:|-------:|-------:|-------:|--------:|
| EARTH  |     381 | 2.7856 | 2.8478 | 0      | 1.7081 | 13.3166 |
| MARS   |      45 | 1.1194 | 0.5812 | 0.3297 | 1.0322 |  2.8364 |
| MOON   |      54 | 1.1067 | 0.1609 | 0.7169 | 1.0941 |  1.436  |

### `p90_roughness_m`

| body   |   count |   mean |    std |    min |    50% |     max |
|:-------|--------:|-------:|-------:|-------:|-------:|--------:|
| EARTH  |     381 | 7.6367 | 7.1327 | 0.0077 | 5.6093 | 33.6679 |
| MARS   |      45 | 2.5441 | 1.565  | 0.6719 | 2.0788 |  7.6524 |
| MOON   |      54 | 2.6385 | 0.6104 | 1.386  | 2.6412 |  4.3392 |

### `robust_relief_p95_p5_m`

| body   |   count |     mean |     std |      min |       50% |     max |
|:-------|--------:|---------:|--------:|---------:|----------:|--------:|
| EARTH  |     381 |  422.843 | 524.094 |   1.4493 |  186.796  | 2993.47 |
| MARS   |      45 |  282.229 | 440.746 |  22.1579 |   83.4957 | 1728.7  |
| MOON   |      54 | 1548.99  | 660.462 | 439.468  | 1379.47   | 3350.02 |

### `mean_slope_deg`

| body   |   count |    mean |    std |    min |     50% |     max |
|:-------|--------:|--------:|-------:|-------:|--------:|--------:|
| EARTH  |     381 |  7.2291 | 7.3389 | 0.0193 |  4.8945 | 37.0979 |
| MARS   |      45 |  3.3198 | 3.1413 | 0.8277 |  2.0253 | 12.1802 |
| MOON   |      54 | 13.0007 | 4.0553 | 5.6972 | 12.5534 | 23.055  |

### `roughness_m`

| body   |   count |   mean |    std |    min |    50% |     max |
|:-------|--------:|-------:|-------:|-------:|-------:|--------:|
| EARTH  |     381 | 3.6723 | 3.4242 | 0.0051 | 2.6665 | 15.4066 |
| MARS   |      45 | 1.3944 | 0.7382 | 0.4141 | 1.2261 |  3.6802 |
| MOON   |      54 | 1.4456 | 0.2643 | 0.8301 | 1.4242 |  2.0666 |

### `relative_relief_m`

| body   |   count |     mean |     std |      min |      50% |     max |
|:-------|--------:|---------:|--------:|---------:|---------:|--------:|
| EARTH  |     381 |  657.974 | 749.484 |   2.738  |  350.149 | 3657.87 |
| MARS   |      45 |  441.086 | 617.284 |  68.8699 |  153.487 | 2167.42 |
| MOON   |      54 | 2148.35  | 789.815 | 673.448  | 2082.82  | 4141.81 |

## Correlação de Pearson entre features (todas as linhas)

|                        |   median_slope_deg |   p90_slope_deg |   median_roughness_m |   p90_roughness_m |   robust_relief_p95_p5_m |   mean_slope_deg |   roughness_m |   relative_relief_m |
|:-----------------------|-------------------:|----------------:|---------------------:|------------------:|-------------------------:|-----------------:|--------------:|--------------------:|
| median_slope_deg       |              1     |           0.869 |                0.786 |             0.699 |                    0.838 |            0.975 |         0.761 |               0.855 |
| p90_slope_deg          |              0.869 |           1     |                0.788 |             0.878 |                    0.745 |            0.952 |         0.858 |               0.786 |
| median_roughness_m     |              0.786 |           0.788 |                1     |             0.906 |                    0.41  |            0.801 |         0.973 |               0.451 |
| p90_roughness_m        |              0.699 |           0.878 |                0.906 |             1     |                    0.413 |            0.791 |         0.978 |               0.464 |
| robust_relief_p95_p5_m |              0.838 |           0.745 |                0.41  |             0.413 |                    1     |            0.841 |         0.428 |               0.982 |
| mean_slope_deg         |              0.975 |           0.952 |                0.801 |             0.791 |                    0.841 |            1     |         0.819 |               0.867 |
| roughness_m            |              0.761 |           0.858 |                0.973 |             0.978 |                    0.428 |            0.819 |         1     |               0.476 |
| relative_relief_m      |              0.855 |           0.786 |                0.451 |             0.464 |                    0.982 |            0.867 |         0.476 |               1     |

## Correlação de Pearson entre features (só Terra)

|                        |   median_slope_deg |   p90_slope_deg |   median_roughness_m |   p90_roughness_m |   robust_relief_p95_p5_m |   mean_slope_deg |   roughness_m |   relative_relief_m |
|:-----------------------|-------------------:|----------------:|---------------------:|------------------:|-------------------------:|-----------------:|--------------:|--------------------:|
| median_slope_deg       |              1     |           0.871 |                0.928 |             0.845 |                    0.864 |            0.972 |         0.909 |               0.872 |
| p90_slope_deg          |              0.871 |           1     |                0.852 |             0.959 |                    0.844 |            0.958 |         0.932 |               0.87  |
| median_roughness_m     |              0.928 |           0.852 |                1     |             0.899 |                    0.715 |            0.923 |         0.971 |               0.733 |
| p90_roughness_m        |              0.845 |           0.959 |                0.899 |             1     |                    0.746 |            0.925 |         0.976 |               0.777 |
| robust_relief_p95_p5_m |              0.864 |           0.844 |                0.715 |             0.746 |                    1     |            0.89  |         0.755 |               0.98  |
| mean_slope_deg         |              0.972 |           0.958 |                0.923 |             0.925 |                    0.89  |            1     |         0.951 |               0.907 |
| roughness_m            |              0.909 |           0.932 |                0.971 |             0.976 |                    0.755 |            0.951 |         1     |               0.781 |
| relative_relief_m      |              0.872 |           0.87  |                0.733 |             0.777 |                    0.98  |            0.907 |         0.781 |               1     |


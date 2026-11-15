# Similaridade Terra × Lua/Marte — protocolo `v1_7`

Grupos (peso igual): **terreno** (median_slope_deg, p90_slope_deg, median_roughness_m, p90_roughness_m, robust_relief_p95_p5_m); **cobertura** (frac_solo_exposto, frac_neve_gelo, frac_vegetacao, frac_construido); **temperatura** (t_sup_media_K, t_sup_max_K); **geologia** (lito_vulcanica, lito_cristalina, lito_sedimentar, lito_evaporitica, lito_gelo, lito_impacto_terras_altas).

Distância total = √(média dos quadrados das distâncias dos grupos); d50 = 1.296; score = 100/(1 + d/d50). `dist_<grupo>`: quanto cada grupo afasta o local do alvo (0 = igual).

## MOON: 10 locais da Terra mais parecidos (todos os alvos do corpo juntos)

|   posicao | site_name                      | tipo      |   score |   dist_features |   dist_terreno |   dist_cobertura |   dist_temperatura |   dist_geologia |   dist_zeus |
|----------:|:-------------------------------|:----------|--------:|----------------:|---------------:|-----------------:|-------------------:|----------------:|------------:|
|         1 | Vales Secos de McMurdo         | candidato |  52.703 |           1.163 |          0.605 |            0.439 |              1.949 |               1 |      17.185 |
|         2 | Islandia - Askja               | candidato |  51.44  |           1.223 |          0.726 |            0.023 |              2.144 |               1 |      24.742 |
|         3 | Ilha Devon - Haughton          | candidato |  49.684 |           1.312 |          1.028 |            0.332 |              2.192 |               1 |      18.227 |
|         4 | Svalbard - Bockfjorden         | candidato |  49.266 |           1.334 |          1.046 |            0.7   |              2.116 |               1 |      17.234 |
|         5 | Planalto do Tibete - Changtang | candidato |  48.265 |           1.389 |          0.563 |            0.333 |              2.484 |               1 |      27.543 |
|         6 | Ojos del Salado                | candidato |  47.793 |           1.415 |          0.727 |            0.255 |              2.53  |               1 |      24.775 |
|         7 | Mauna Loa - HI-SEAS            | candidato |  47.568 |           1.428 |          0.374 |            0     |              2.636 |               1 |      24.442 |
|         8 | Atacama - Chajnantor           | candidato |  47.507 |           1.432 |          0.71  |            0.002 |              2.568 |               1 |      24.749 |
|         9 | Lanzarote                      | candidato |  47.045 |           1.458 |          0.855 |            0.199 |              2.605 |               1 |      24.567 |
|        10 | Ladakh                         | candidato |  46.862 |           1.469 |          0.839 |            0.4   |              2.567 |               1 |      17.209 |

Controles (cidades/floresta) neste ranking: posições 32, 34, 36, 40, 43 de 43.

## MARS: 10 locais da Terra mais parecidos (todos os alvos do corpo juntos)

|   posicao | site_name                      | tipo      |   score |   dist_features |   dist_terreno |   dist_cobertura |   dist_temperatura |   dist_geologia |   dist_zeus |
|----------:|:-------------------------------|:----------|--------:|----------------:|---------------:|-----------------:|-------------------:|----------------:|------------:|
|         1 | Islandia - Askja               | candidato |  69.534 |           0.568 |          0.317 |            0.044 |              0.471 |               1 |      18.977 |
|         2 | Ilha Devon - Haughton          | candidato |  67.419 |           0.626 |          0.765 |            0.332 |              0.361 |               1 |      14.144 |
|         3 | Planalto do Tibete - Changtang | candidato |  67.17  |           0.633 |          0.536 |            0.127 |              0.662 |               1 |      19.082 |
|         4 | Bacia de Qaidam                | candidato |  65.65  |           0.678 |          0.237 |            0     |              0.906 |               1 |      18.946 |
|         5 | Atacama - Chajnantor           | candidato |  65.446 |           0.684 |          0.524 |            0     |              0.748 |               1 |      18.884 |
|         6 | Mauna Loa - HI-SEAS            | candidato |  65.175 |           0.692 |          0.521 |            0.234 |              0.796 |               1 |      18.251 |
|         7 | Atacama - Yungay               | candidato |  65.065 |           0.696 |          0.638 |            0.001 |              0.922 |               1 |      17.063 |
|         8 | Lanzarote                      | candidato |  64.814 |           0.703 |          0.666 |            0.199 |              0.762 |               0 |       2.01  |
|         9 | Utah - MDRS                    | candidato |  64.565 |           0.711 |          0.477 |            0.082 |              1.005 |               1 |      15.727 |
|        10 | Danakil - Dallol               | candidato |  63.382 |           0.749 |          0.459 |            0.001 |              1.06  |               1 |       0.901 |

Controles (cidades/floresta) neste ranking: posições 26, 28, 31, 32, 42 de 43.

## Top 3 por alvo

- **Haworth** (MOON): Vales Secos de McMurdo (52), Islandia - Askja (51), Ilha Devon - Haughton (49)
- **Malapert Massif** (MOON): Vales Secos de McMurdo (58), Islandia - Askja (57), Planalto do Tibete - Changtang (56)
- **Mons Mouton Plateau** (MOON): Vales Secos de McMurdo (54), Islandia - Askja (53), Ilha Devon - Haughton (51)
- **Nobile Rim 2** (MOON): Vales Secos de McMurdo (54), Islandia - Askja (53), Ilha Devon - Haughton (52)
- **de Gerlache Rim** (MOON): Vales Secos de McMurdo (51), Islandia - Askja (50), Ilha Devon - Haughton (49)
- **Connecting Ridge** (MOON): Vales Secos de McMurdo (52), Islandia - Askja (51), Ilha Devon - Haughton (49)
- **Jezero (Perseverance)** (MARS): Islandia - Askja (69), Ilha Devon - Haughton (68), Planalto do Tibete - Changtang (67)
- **Gale (Curiosity)** (MARS): Vales Secos de McMurdo (75), Planalto do Tibete - Changtang (74), Ilha Devon - Haughton (70)
- **Elysium Planitia (InSight)** (MARS): Bacia de Qaidam (73), Planalto do Tibete - Changtang (71), Islandia - Askja (70)
- **Oxia Planum (ExoMars Rosalind Franklin)** (MARS): Islandia - Askja (70), Ilha Devon - Haughton (66), Planalto do Tibete - Changtang (66)
- **Meridiani Planum (Opportunity)** (MARS): Ilha Devon - Haughton (82), Planalto do Tibete - Changtang (80), Bacia de Qaidam (76)
- **Gusev (Spirit)** (MARS): Islandia - Askja (76), Atacama - Chajnantor (76), Lanzarote (73)

## Limitações

- Similaridade usa relevo, cobertura, temperatura da superfície e geologia (classe harmonizada).
- Peso igual por grupo (relevo, cobertura, temperatura, geologia). O ZEUS (clusters, dist_zeus) continua recebendo todas as colunas sem peso: é um modelo pré-treinado.
- Geologia só diferencia alvos com classe existente na Terra (em Marte, só Gusev, vulcânico).
- Piso de ruído do NASADEM: locais planos da Terra parecem mais inclinados/rugosos do que são.
- O score é uma escala relativa a este conjunto de locais; muda se os locais mudarem.

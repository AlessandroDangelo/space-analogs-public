# Similaridade Terra × Lua/Marte — protocolo `v1_6`

Features: `median_slope_deg`, `p90_slope_deg`, `median_roughness_m`, `p90_roughness_m`, `robust_relief_p95_p5_m`, `frac_solo_exposto`, `frac_neve_gelo`, `frac_vegetacao`, `frac_construido`, `t_sup_media_K`, `t_sup_max_K`. Distância em desvios-padrão (RMS); d50 = 1.259. Score = 100/(1 + d/d50).

## MOON: 10 locais da Terra mais parecidos (todos os alvos do corpo juntos)

|   posicao | site_name                      | tipo      |   score |   dist_features |   dist_zeus |   cocluster_k4 |
|----------:|:-------------------------------|:----------|--------:|----------------:|------------:|---------------:|
|         1 | Islandia - Askja               | candidato |  55.853 |           0.995 |      12.78  |              0 |
|         2 | Mauna Loa - HI-SEAS            | candidato |  52.432 |           1.142 |       8.694 |              0 |
|         3 | Ilha Devon - Haughton          | candidato |  52.403 |           1.143 |      12.905 |              0 |
|         4 | Planalto do Tibete - Changtang | candidato |  52.4   |           1.143 |      12.776 |              0 |
|         5 | Ojos del Salado                | candidato |  51.542 |           1.183 |      12.495 |              0 |
|         6 | Atacama - Chajnantor           | candidato |  51.259 |           1.197 |      12.706 |              0 |
|         7 | Svalbard - Bockfjorden         | candidato |  50.868 |           1.216 |      13.85  |              0 |
|         8 | Licancabur                     | candidato |  50.814 |           1.218 |      13.042 |              0 |
|         9 | Lanzarote                      | candidato |  50.659 |           1.226 |      12.966 |              0 |
|        10 | Atacama - Yungay               | candidato |  50.308 |           1.243 |      12.887 |              0 |

Controles (cidades/floresta) neste ranking: posições 30, 33, 34, 37, 38 de 42.

## MARS: 10 locais da Terra mais parecidos (todos os alvos do corpo juntos)

|   posicao | site_name                      | tipo      |   score |   dist_features |   dist_zeus |   cocluster_k4 |
|----------:|:-------------------------------|:----------|--------:|----------------:|------------:|---------------:|
|         1 | Islandia - Askja               | candidato |  82.159 |           0.273 |       0.343 |          0.933 |
|         2 | Bacia de Qaidam                | candidato |  74.787 |           0.424 |       0.169 |          0.933 |
|         3 | Planalto do Tibete - Changtang | candidato |  72.109 |           0.487 |       1.36  |          0.933 |
|         4 | Mauna Loa - HI-SEAS            | candidato |  71.913 |           0.492 |       1.011 |          0.933 |
|         5 | Atacama - Chajnantor           | candidato |  71.452 |           0.503 |       1.079 |          0.933 |
|         6 | Gobi                           | candidato |  70.834 |           0.518 |       0.275 |          0.933 |
|         7 | Danakil - Dallol               | candidato |  70.818 |           0.519 |       0.298 |          0.933 |
|         8 | Vale da Morte                  | candidato |  69.755 |           0.546 |       0.342 |          0.933 |
|         9 | Deserto de Lut                 | candidato |  69.429 |           0.554 |       0.259 |          0.933 |
|        10 | Utah - MDRS                    | candidato |  69.387 |           0.555 |       0.879 |          0.933 |

Controles (cidades/floresta) neste ranking: posições 24, 26, 29, 31, 41 de 42.

## Top 3 por alvo

- **Haworth** (MOON): Islandia - Askja (55), Ilha Devon - Haughton (52), Planalto do Tibete - Changtang (51)
- **Malapert Massif** (MOON): Mauna Loa - HI-SEAS (60), Planalto do Tibete - Changtang (60), Ojos del Salado (59)
- **Mons Mouton Plateau** (MOON): Islandia - Askja (56), Planalto do Tibete - Changtang (54), Mauna Loa - HI-SEAS (54)
- **Nobile Rim 2** (MOON): Islandia - Askja (56), Planalto do Tibete - Changtang (55), Mauna Loa - HI-SEAS (54)
- **de Gerlache Rim** (MOON): Islandia - Askja (54), Planalto do Tibete - Changtang (52), Ilha Devon - Haughton (51)
- **Connecting Ridge** (MOON): Islandia - Askja (55), Ilha Devon - Haughton (52), Ojos del Salado (52)
- **Jezero (Perseverance)** (MARS): Islandia - Askja (84), Planalto do Tibete - Changtang (76), Bacia de Qaidam (76)
- **Gale (Curiosity)** (MARS): Islandia - Askja (77), Mauna Loa - HI-SEAS (75), Planalto do Tibete - Changtang (74)
- **Elysium Planitia (InSight)** (MARS): Islandia - Askja (82), Bacia de Qaidam (75), Gobi (74)
- **Oxia Planum (ExoMars Rosalind Franklin)** (MARS): Islandia - Askja (84), Bacia de Qaidam (74), Mauna Loa - HI-SEAS (73)
- **Meridiani Planum (Opportunity)** (MARS): Atacama - Chajnantor (82), Islandia - Askja (79), Ilha Devon - Haughton (79)
- **Gusev (Spirit)** (MARS): Bacia de Qaidam (77), Atacama - Chajnantor (74), Islandia - Askja (74)

## Limitações

- Similaridade só de relevo e cobertura superficial; clima e geologia ainda não entram.
- Piso de ruído do NASADEM: locais planos da Terra parecem mais inclinados/rugosos do que são.
- O score é uma escala relativa a este conjunto de locais; muda se os locais mudarem.

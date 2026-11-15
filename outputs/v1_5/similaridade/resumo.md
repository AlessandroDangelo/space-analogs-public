# Similaridade Terra × Lua/Marte — protocolo `v1_5`

Features: `median_slope_deg`, `p90_slope_deg`, `median_roughness_m`, `p90_roughness_m`, `robust_relief_p95_p5_m`, `frac_solo_exposto`, `frac_neve_gelo`, `frac_vegetacao`, `frac_construido`. Distância em desvios-padrão (RMS); d50 = 0.901. Score = 100/(1 + d/d50).

## MOON: 10 locais da Terra mais parecidos (todos os alvos do corpo juntos)

|   posicao | site_name                      | tipo      |   score |   dist_features |   dist_zeus |   cocluster_k4 |
|----------:|:-------------------------------|:----------|--------:|----------------:|------------:|---------------:|
|         1 | Mauna Loa - HI-SEAS            | candidato |  76.379 |           0.279 |       0.196 |              1 |
|         2 | Licancabur                     | candidato |  68.488 |           0.415 |       5.828 |              1 |
|         3 | Atacama - Yungay               | candidato |  65.677 |           0.471 |       7.891 |              1 |
|         4 | Planalto do Tibete - Changtang | candidato |  65.585 |           0.473 |       8.109 |              1 |
|         5 | Atacama - Chajnantor           | candidato |  63.135 |           0.526 |       7.908 |              1 |
|         6 | Islandia - Askja               | candidato |  62.573 |           0.539 |       8.126 |              1 |
|         7 | Ojos del Salado                | candidato |  61.204 |           0.571 |       7.726 |              1 |
|         8 | Vale da Morte                  | candidato |  59.921 |           0.603 |       7.967 |              1 |
|         9 | Lanzarote                      | candidato |  58.146 |           0.649 |       8.674 |              1 |
|        10 | Ladakh                         | candidato |  57.053 |           0.678 |       7.976 |              1 |

Controles (cidades/floresta) neste ranking: posições 30, 34, 35, 37, 38 de 42.

## MARS: 10 locais da Terra mais parecidos (todos os alvos do corpo juntos)

|   posicao | site_name            | tipo      |   score |   dist_features |   dist_zeus |   cocluster_k4 |
|----------:|:---------------------|:----------|--------:|----------------:|------------:|---------------:|
|         1 | Bacia de Qaidam      | candidato |  84.888 |           0.16  |       0.156 |              1 |
|         2 | Deserto de Lut       | candidato |  81.354 |           0.207 |       0.258 |              1 |
|         3 | Islandia - Askja     | candidato |  81.231 |           0.208 |       0.302 |              1 |
|         4 | Vale da Morte        | candidato |  81.063 |           0.21  |       0.273 |              1 |
|         5 | Gobi                 | candidato |  76.405 |           0.278 |       0.476 |              1 |
|         6 | Danakil - Dallol     | candidato |  75.248 |           0.296 |       0.299 |              1 |
|         7 | Utah - MDRS          | candidato |  71.495 |           0.359 |       1.277 |              1 |
|         8 | Mauna Loa - HI-SEAS  | candidato |  69.559 |           0.394 |       0.771 |              1 |
|         9 | Atacama - Chajnantor | candidato |  68.101 |           0.422 |       1.585 |              1 |
|        10 | Saara - Tanezrouft   | candidato |  67.572 |           0.432 |       0.391 |              1 |

Controles (cidades/floresta) neste ranking: posições 23, 26, 29, 32, 40 de 42.

## Top 3 por alvo

- **Haworth** (MOON): Mauna Loa - HI-SEAS (82), Licancabur (71), Atacama - Yungay (68)
- **Malapert Massif** (MOON): Mauna Loa - HI-SEAS (70), Licancabur (66), Planalto do Tibete - Changtang (64)
- **Mons Mouton Plateau** (MOON): Mauna Loa - HI-SEAS (78), Licancabur (70), Atacama - Yungay (68)
- **Nobile Rim 2** (MOON): Mauna Loa - HI-SEAS (79), Licancabur (68), Planalto do Tibete - Changtang (67)
- **de Gerlache Rim** (MOON): Mauna Loa - HI-SEAS (77), Licancabur (69), Atacama - Yungay (66)
- **Connecting Ridge** (MOON): Mauna Loa - HI-SEAS (72), Licancabur (66), Planalto do Tibete - Changtang (64)
- **Jezero (Perseverance)** (MARS): Bacia de Qaidam (88), Islandia - Askja (85), Deserto de Lut (83)
- **Gale (Curiosity)** (MARS): Mauna Loa - HI-SEAS (76), Vale da Morte (75), Islandia - Askja (72)
- **Elysium Planitia (InSight)** (MARS): Gobi (96), Deserto de Lut (96), Vale da Morte (84)
- **Oxia Planum (ExoMars Rosalind Franklin)** (MARS): Bacia de Qaidam (88), Islandia - Askja (85), Deserto de Lut (83)
- **Meridiani Planum (Opportunity)** (MARS): Atacama - Chajnantor (88), Utah - MDRS (88), Atacama - Yungay (85)
- **Gusev (Spirit)** (MARS): Bacia de Qaidam (85), Rub al Khali (84), Utah - MDRS (79)

## Limitações

- Similaridade só de relevo e cobertura superficial; clima e geologia ainda não entram.
- Piso de ruído do NASADEM: locais planos da Terra parecem mais inclinados/rugosos do que são.
- O score é uma escala relativa a este conjunto de locais; muda se os locais mudarem.

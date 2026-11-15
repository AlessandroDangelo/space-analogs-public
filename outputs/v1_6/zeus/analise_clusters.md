# Análise dos clusters ZEUS

475 recortes: EARTH=376, MOON=54, MARS=45 | protocolo: v1_6

## Qualidade por k

`silhueta_embedding`: separação dos clusters no espaço do ZEUS (-1 a 1, maior = melhor). `ari_medio_entre_sementes`: 1 = o K-Means dá o mesmo resultado com sementes diferentes.

|   k |   silhueta_embedding |   ari_medio_entre_sementes |   inercia | tamanhos                      |
|----:|---------------------:|---------------------------:|----------:|:------------------------------|
|   2 |             0.525925 |                          1 | 42301.7   | 156 319                       |
|   3 |             0.620707 |                          1 | 20714.2   | 120 319 36                    |
|   4 |             0.667767 |                          1 | 13109.4   | 121 57 261 36                 |
|   5 |             0.764561 |                          1 |  7082.96  | 120 57 220 36 42              |
|   6 |             0.833113 |                          1 |  2426.38  | 96 57 220 36 24 42            |
|   7 |             0.797241 |                          1 |  1145.52  | 57 130 95 36 24 42 91         |
|   8 |             0.828321 |                          1 |   697.721 | 95 57 127 36 24 42 76 18      |
|   9 |             0.829325 |                          1 |   446.212 | 88 74 36 57 42 24 127 17 10   |
|  10 |             0.838972 |                          1 |   355.899 | 24 74 36 88 55 42 121 17 10 8 |

## Checagem de sanidade: recortes do mesmo local

ARI entre cluster e `site_id`. Com k pequeno e muitos locais o ARI é naturalmente baixo; a coluna de locais "inteiros" é a leitura mais direta.

|   k |   ARI_vs_site_id | locais_com_todos_recortes_no_mesmo_cluster   |
|----:|-----------------:|:---------------------------------------------|
|   2 |            0.021 | 41/54                                        |
|   3 |            0.025 | 41/54                                        |
|   4 |            0.043 | 40/54                                        |
|   5 |            0.063 | 40/54                                        |
|   6 |            0.069 | 39/54                                        |
|   7 |            0.114 | 34/54                                        |
|   8 |            0.12  | 33/54                                        |
|   9 |            0.125 | 33/54                                        |
|  10 |            0.131 | 33/54                                        |

## k = 2

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     156 |      0 |      0 |
|         1 |     220 |     45 |     54 |

- **Cluster 1** — alvos: MOON (54), MARS (45); Terra (220 recortes): Aconcagua ×7, Atacama - Chajnantor ×7, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Deserto de Lut ×9, Deserto de Mojave ×3, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×9, Kilimanjaro, Ladakh ×9, Lanzarote ×6, Licancabur ×7, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×4, Mauna Loa - HI-SEAS ×6, Namibe ×9, Nova York [CONTROLE] ×9, Ojos del Salado ×8, Planalto do Tibete - Changtang ×6, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×9, Singapura [CONTROLE] ×8, Svalbard - Bockfjorden ×3, Utah - MDRS ×9, Vale da Morte ×9, Wadi Rum ×9

## k = 3

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     120 |      0 |      0 |
|         1 |     220 |     45 |     54 |
|         2 |      36 |      0 |      0 |

- **Cluster 1** — alvos: MOON (54), MARS (45); Terra (220 recortes): Aconcagua ×7, Atacama - Chajnantor ×7, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Deserto de Lut ×9, Deserto de Mojave ×3, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×9, Kilimanjaro, Ladakh ×9, Lanzarote ×6, Licancabur ×7, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×4, Mauna Loa - HI-SEAS ×6, Namibe ×9, Nova York [CONTROLE] ×9, Ojos del Salado ×8, Planalto do Tibete - Changtang ×6, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×9, Singapura [CONTROLE] ×8, Svalbard - Bockfjorden ×3, Utah - MDRS ×9, Vale da Morte ×9, Wadi Rum ×9

## k = 4

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     121 |      0 |      0 |
|         1 |       0 |      3 |     54 |
|         2 |     219 |     42 |      0 |
|         3 |      36 |      0 |      0 |

- **Cluster 1** — alvos: MOON (54), MARS (3); Terra (0 recortes): nenhum
- **Cluster 2** — alvos: MARS (42); Terra (219 recortes): Aconcagua ×7, Atacama - Chajnantor ×7, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Deserto de Lut ×9, Deserto de Mojave ×3, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×9, Kilimanjaro, Ladakh ×9, Lanzarote ×6, Licancabur ×7, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×4, Mauna Loa - HI-SEAS ×6, Namibe ×9, Nova York [CONTROLE] ×9, Ojos del Salado ×7, Planalto do Tibete - Changtang ×6, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×9, Singapura [CONTROLE] ×8, Svalbard - Bockfjorden ×3, Utah - MDRS ×9, Vale da Morte ×9, Wadi Rum ×9

## k = 5

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     120 |      0 |      0 |
|         1 |       0 |      3 |     54 |
|         2 |     178 |     42 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |      42 |      0 |      0 |

- **Cluster 1** — alvos: MOON (54), MARS (3); Terra (0 recortes): nenhum
- **Cluster 2** — alvos: MARS (42); Terra (178 recortes): Aconcagua ×7, Atacama - Chajnantor ×7, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Deserto de Lut ×9, Deserto de Mojave ×3, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×9, Kilimanjaro, Ladakh ×9, Lanzarote ×4, Licancabur ×7, Mauna Loa - HI-SEAS ×6, Namibe ×9, Ojos del Salado ×8, Planalto do Tibete - Changtang ×6, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Svalbard - Bockfjorden ×2, Utah - MDRS ×9, Vale da Morte ×9, Wadi Rum ×9

## k = 6

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      96 |      0 |      0 |
|         1 |       0 |      3 |     54 |
|         2 |     178 |     42 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |      24 |      0 |      0 |
|         5 |      42 |      0 |      0 |

- **Cluster 1** — alvos: MOON (54), MARS (3); Terra (0 recortes): nenhum
- **Cluster 2** — alvos: MARS (42); Terra (178 recortes): Aconcagua ×7, Atacama - Chajnantor ×7, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Deserto de Lut ×9, Deserto de Mojave ×3, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×9, Kilimanjaro, Ladakh ×9, Lanzarote ×4, Licancabur ×7, Mauna Loa - HI-SEAS ×6, Namibe ×9, Ojos del Salado ×8, Planalto do Tibete - Changtang ×6, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Svalbard - Bockfjorden ×2, Utah - MDRS ×9, Vale da Morte ×9, Wadi Rum ×9

## k = 7

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |       0 |      3 |     54 |
|         1 |      90 |     40 |      0 |
|         2 |      95 |      0 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |      24 |      0 |      0 |
|         5 |      42 |      0 |      0 |
|         6 |      89 |      2 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (3); Terra (0 recortes): nenhum
- **Cluster 1** — alvos: MARS (40); Terra (90 recortes): Atacama - Chajnantor, Atacama - Yungay ×2, Bacia de Qaidam ×9, Danakil - Dallol ×8, Deserto de Lut ×9, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×4, Lanzarote, Licancabur, Mauna Loa - HI-SEAS ×5, Planalto do Tibete - Changtang, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Utah - MDRS ×8, Vale da Morte ×4
- **Cluster 6** — alvos: MARS (2); Terra (89 recortes): Aconcagua ×7, Atacama - Chajnantor ×6, Atacama - Yungay ×7, Danakil - Dallol, Deserto de Mojave ×3, Islandia - Askja ×5, Kilimanjaro, Ladakh ×9, Lanzarote ×3, Licancabur ×7, Mauna Loa - HI-SEAS, Namibe ×9, Ojos del Salado ×8, Planalto do Tibete - Changtang ×5, Svalbard - Bockfjorden ×2, Utah - MDRS, Vale da Morte ×5, Wadi Rum ×9

## k = 8

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      95 |      0 |      0 |
|         1 |       0 |      3 |     54 |
|         2 |      86 |     41 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |      24 |      0 |      0 |
|         5 |      42 |      0 |      0 |
|         6 |      75 |      1 |      0 |
|         7 |      18 |      0 |      0 |

- **Cluster 1** — alvos: MOON (54), MARS (3); Terra (0 recortes): nenhum
- **Cluster 2** — alvos: MARS (41); Terra (86 recortes): Atacama - Chajnantor, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol ×7, Deserto de Lut ×9, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×4, Lanzarote, Mauna Loa - HI-SEAS ×5, Planalto do Tibete - Changtang, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Utah - MDRS ×7, Vale da Morte ×4
- **Cluster 6** — alvos: MARS (1); Terra (75 recortes): Atacama - Chajnantor ×6, Atacama - Yungay ×8, Danakil - Dallol ×2, Deserto de Mojave ×3, Islandia - Askja ×5, Ladakh ×4, Lanzarote ×3, Licancabur ×7, Mauna Loa - HI-SEAS, Namibe ×9, Ojos del Salado ×5, Planalto do Tibete - Changtang ×5, Svalbard - Bockfjorden ×2, Utah - MDRS ×2, Vale da Morte ×4, Wadi Rum ×9

## k = 9

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      88 |      0 |      0 |
|         1 |      73 |      1 |      0 |
|         2 |      36 |      0 |      0 |
|         3 |       0 |      3 |     54 |
|         4 |      42 |      0 |      0 |
|         5 |      24 |      0 |      0 |
|         6 |      86 |     41 |      0 |
|         7 |      17 |      0 |      0 |
|         8 |      10 |      0 |      0 |

- **Cluster 1** — alvos: MARS (1); Terra (73 recortes): Atacama - Chajnantor ×6, Atacama - Yungay ×8, Danakil - Dallol ×2, Deserto de Mojave ×2, Islandia - Askja ×5, Ladakh ×4, Lanzarote ×3, Licancabur ×7, Mauna Loa - HI-SEAS, Namibe ×9, Ojos del Salado ×5, Planalto do Tibete - Changtang ×4, Svalbard - Bockfjorden ×2, Utah - MDRS ×2, Vale da Morte ×4, Wadi Rum ×9
- **Cluster 3** — alvos: MOON (54), MARS (3); Terra (0 recortes): nenhum
- **Cluster 6** — alvos: MARS (41); Terra (86 recortes): Atacama - Chajnantor, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol ×7, Deserto de Lut ×9, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×4, Lanzarote, Mauna Loa - HI-SEAS ×5, Planalto do Tibete - Changtang, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Utah - MDRS ×7, Vale da Morte ×4

## k = 10

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      24 |      0 |      0 |
|         1 |      73 |      1 |      0 |
|         2 |      36 |      0 |      0 |
|         3 |      88 |      0 |      0 |
|         4 |       0 |      1 |     54 |
|         5 |      42 |      0 |      0 |
|         6 |      82 |     39 |      0 |
|         7 |      17 |      0 |      0 |
|         8 |      10 |      0 |      0 |
|         9 |       4 |      4 |      0 |

- **Cluster 1** — alvos: MARS (1); Terra (73 recortes): Atacama - Chajnantor ×6, Atacama - Yungay ×8, Danakil - Dallol ×2, Deserto de Mojave ×2, Islandia - Askja ×5, Ladakh ×4, Lanzarote ×3, Licancabur ×7, Mauna Loa - HI-SEAS, Namibe ×9, Ojos del Salado ×5, Planalto do Tibete - Changtang ×4, Svalbard - Bockfjorden ×2, Utah - MDRS ×2, Vale da Morte ×4, Wadi Rum ×9
- **Cluster 4** — alvos: MOON (54), MARS (1); Terra (0 recortes): nenhum
- **Cluster 6** — alvos: MARS (39); Terra (82 recortes): Atacama - Chajnantor, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol ×7, Deserto de Lut ×9, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×4, Lanzarote, Mauna Loa - HI-SEAS, Planalto do Tibete - Changtang, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Utah - MDRS ×7, Vale da Morte ×4
- **Cluster 9** — alvos: MARS (4); Terra (4 recortes): Mauna Loa - HI-SEAS ×4

---
Locais marcados [CONTROLE] (cidades/florestas) caindo junto com Lua/Marte indicam que o cluster é grosseiro demais para aquele k.

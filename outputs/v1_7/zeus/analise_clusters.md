# Análise dos clusters ZEUS

480 recortes: EARTH=381, MOON=54, MARS=45 | protocolo: v1_7

## Qualidade por k

`silhueta_embedding`: separação dos clusters no espaço do ZEUS (-1 a 1, maior = melhor). `ari_medio_entre_sementes`: 1 = o K-Means dá o mesmo resultado com sementes diferentes.

|   k |   silhueta_embedding |   ari_medio_entre_sementes |   inercia | tamanhos                      |
|----:|---------------------:|---------------------------:|----------:|:------------------------------|
|   2 |             0.51254  |                          1 | 52285.9   | 264 216                       |
|   3 |             0.695994 |                          1 | 26198.9   | 217 147 116                   |
|   4 |             0.795523 |                          1 | 12024     | 182 146 116 36                |
|   5 |             0.90796  |                          1 |  1400.3   | 180 75 116 36 73              |
|   6 |             0.881656 |                          1 |   798.496 | 106 75 116 36 73 74           |
|   7 |             0.886189 |                          1 |   261.649 | 105 75 116 36 53 74 21        |
|   8 |             0.890246 |                          1 |   168.061 | 105 75 116 36 53 74 12 9      |
|   9 |             0.893664 |                          1 |   127.731 | 75 104 116 36 53 74 10 10 2   |
|  10 |             0.851704 |                          1 |   101.755 | 87 75 36 116 53 70 10 10 21 2 |

## Checagem de sanidade: recortes do mesmo local

ARI entre cluster e `site_id`. Com k pequeno e muitos locais o ARI é naturalmente baixo; a coluna de locais "inteiros" é a leitura mais direta.

|   k |   ARI_vs_site_id | locais_com_todos_recortes_no_mesmo_cluster   |
|----:|-----------------:|:---------------------------------------------|
|   2 |            0.025 | 38/55                                        |
|   3 |            0.045 | 37/55                                        |
|   4 |            0.059 | 37/55                                        |
|   5 |            0.076 | 37/55                                        |
|   6 |            0.112 | 36/55                                        |
|   7 |            0.118 | 36/55                                        |
|   8 |            0.119 | 36/55                                        |
|   9 |            0.119 | 36/55                                        |
|  10 |            0.128 | 35/55                                        |

## k = 2

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     181 |     29 |     54 |
|         1 |     200 |     16 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (29); Terra (181 recortes): Aconcagua ×6, Arkaroola, Atacama - Chajnantor ×9, Atacama - Yungay ×8, Danakil - Dallol ×8, Denali ×5, Deserto de Mojave ×5, Everest ×9, Gobi ×9, Ilha Devon - Haughton ×3, Islandia - Askja ×9, Kilimanjaro ×9, Ladakh ×4, Lanzarote ×8, Licancabur ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE] ×3, Ojos del Salado ×9, Pilbara ×8, Rio Tinto ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×7, Teide ×9, Utah - MDRS, Vale da Morte ×5, Vales Secos de McMurdo ×8
- **Cluster 1** — alvos: MARS (16); Terra (200 recortes): Aconcagua ×3, Arkaroola ×8, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol, Denali ×2, Deserto de Lut ×9, Deserto de Mojave ×4, Deserto de Simpson ×9, Dome Argus ×9, Dome C ×9, Groenlandia - Summit ×9, Ilha Devon - Haughton ×6, Ladakh ×5, Lanzarote, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×9, Namibe ×9, Nova York [CONTROLE] ×6, Oymyakon ×9, Pilbara, Planalto do Tibete - Changtang ×9, Rub al Khali ×9, Saara - Tanezrouft ×9, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×5, Svalbard - Bockfjorden ×2, Utah - MDRS ×8, Vale da Morte ×4, Vales Secos de McMurdo, Vostok ×9, Wadi Rum ×9

## k = 3

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     201 |     16 |      0 |
|         1 |      72 |     21 |     54 |
|         2 |     108 |      8 |      0 |

- **Cluster 0** — alvos: MARS (16); Terra (201 recortes): Aconcagua ×3, Arkaroola ×8, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol, Denali ×2, Deserto de Lut ×9, Deserto de Mojave ×5, Deserto de Simpson ×9, Dome Argus ×9, Dome C ×9, Groenlandia - Summit ×9, Ilha Devon - Haughton ×6, Ladakh ×5, Lanzarote, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×9, Namibe ×9, Nova York [CONTROLE] ×6, Oymyakon ×9, Pilbara, Planalto do Tibete - Changtang ×9, Rub al Khali ×9, Saara - Tanezrouft ×9, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×5, Svalbard - Bockfjorden ×2, Utah - MDRS ×8, Vale da Morte ×4, Vales Secos de McMurdo, Vostok ×9, Wadi Rum ×9
- **Cluster 1** — alvos: MOON (54), MARS (21); Terra (72 recortes): Arkaroola, Atacama - Yungay ×8, Danakil - Dallol ×3, Denali ×5, Deserto de Mojave ×3, Everest ×9, Ilha Devon - Haughton ×3, Ladakh ×4, Nova York [CONTROLE] ×2, Pilbara, Rio Tinto ×5, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×4, Utah - MDRS, Vale da Morte ×4, Vales Secos de McMurdo ×8
- **Cluster 2** — alvos: MARS (8); Terra (108 recortes): Aconcagua ×6, Atacama - Chajnantor ×9, Danakil - Dallol ×5, Deserto de Mojave, Gobi ×9, Islandia - Askja ×9, Kilimanjaro ×9, Lanzarote ×8, Licancabur ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE], Ojos del Salado ×9, Pilbara ×7, Rio Tinto ×4, Svalbard - Bockfjorden ×3, Teide ×9, Vale da Morte

## k = 4

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     166 |     16 |      0 |
|         1 |      71 |     21 |     54 |
|         2 |     108 |      8 |      0 |
|         3 |      36 |      0 |      0 |

- **Cluster 0** — alvos: MARS (16); Terra (166 recortes): Aconcagua ×3, Arkaroola ×8, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol, Denali ×2, Deserto de Lut ×9, Deserto de Mojave ×5, Deserto de Simpson ×9, Ilha Devon - Haughton ×7, Ladakh ×5, Lanzarote, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×9, Namibe ×9, Nova York [CONTROLE] ×6, Oymyakon ×9, Pilbara, Planalto do Tibete - Changtang ×9, Rub al Khali ×9, Saara - Tanezrouft ×9, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×5, Svalbard - Bockfjorden ×2, Utah - MDRS ×8, Vale da Morte ×4, Vales Secos de McMurdo, Wadi Rum ×9
- **Cluster 1** — alvos: MOON (54), MARS (21); Terra (71 recortes): Arkaroola, Atacama - Yungay ×8, Danakil - Dallol ×3, Denali ×5, Deserto de Mojave ×3, Everest ×9, Ilha Devon - Haughton ×2, Ladakh ×4, Nova York [CONTROLE] ×2, Pilbara, Rio Tinto ×5, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×4, Utah - MDRS, Vale da Morte ×4, Vales Secos de McMurdo ×8
- **Cluster 2** — alvos: MARS (8); Terra (108 recortes): Aconcagua ×6, Atacama - Chajnantor ×9, Danakil - Dallol ×5, Deserto de Mojave, Gobi ×9, Islandia - Askja ×9, Kilimanjaro ×9, Lanzarote ×8, Licancabur ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE], Ojos del Salado ×9, Pilbara ×7, Rio Tinto ×4, Svalbard - Bockfjorden ×3, Teide ×9, Vale da Morte

## k = 5

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     164 |     16 |      0 |
|         1 |       0 |     21 |     54 |
|         2 |     108 |      8 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |      73 |      0 |      0 |

- **Cluster 0** — alvos: MARS (16); Terra (164 recortes): Aconcagua ×3, Arkaroola ×8, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol, Denali ×2, Deserto de Lut ×9, Deserto de Mojave ×4, Deserto de Simpson ×9, Ilha Devon - Haughton ×6, Ladakh ×5, Lanzarote, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×9, Namibe ×9, Nova York [CONTROLE] ×6, Oymyakon ×9, Pilbara, Planalto do Tibete - Changtang ×9, Rub al Khali ×9, Saara - Tanezrouft ×9, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×5, Svalbard - Bockfjorden ×2, Utah - MDRS ×8, Vale da Morte ×4, Vales Secos de McMurdo, Wadi Rum ×9
- **Cluster 1** — alvos: MOON (54), MARS (21); Terra (0 recortes): nenhum
- **Cluster 2** — alvos: MARS (8); Terra (108 recortes): Aconcagua ×6, Atacama - Chajnantor ×9, Danakil - Dallol ×5, Deserto de Mojave, Gobi ×9, Islandia - Askja ×9, Kilimanjaro ×9, Lanzarote ×8, Licancabur ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE], Ojos del Salado ×9, Pilbara ×7, Rio Tinto ×4, Svalbard - Bockfjorden ×3, Teide ×9, Vale da Morte

## k = 6

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      90 |     16 |      0 |
|         1 |       0 |     21 |     54 |
|         2 |     108 |      8 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |      73 |      0 |      0 |
|         5 |      74 |      0 |      0 |

- **Cluster 0** — alvos: MARS (16); Terra (90 recortes): Aconcagua ×3, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol, Deserto de Lut ×9, Deserto de Mojave ×2, Ilha Devon - Haughton ×2, Ladakh ×5, Lanzarote, Namibe ×9, Planalto do Tibete - Changtang ×8, Rub al Khali ×9, Saara - Tanezrouft ×9, Utah - MDRS ×8, Vale da Morte ×4, Vales Secos de McMurdo, Wadi Rum ×9
- **Cluster 1** — alvos: MOON (54), MARS (21); Terra (0 recortes): nenhum
- **Cluster 2** — alvos: MARS (8); Terra (108 recortes): Aconcagua ×6, Atacama - Chajnantor ×9, Danakil - Dallol ×5, Deserto de Mojave, Gobi ×9, Islandia - Askja ×9, Kilimanjaro ×9, Lanzarote ×8, Licancabur ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE], Ojos del Salado ×9, Pilbara ×7, Rio Tinto ×4, Svalbard - Bockfjorden ×3, Teide ×9, Vale da Morte

## k = 7

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      89 |     16 |      0 |
|         1 |       0 |     21 |     54 |
|         2 |     108 |      8 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |      53 |      0 |      0 |
|         5 |      74 |      0 |      0 |
|         6 |      21 |      0 |      0 |

- **Cluster 0** — alvos: MARS (16); Terra (89 recortes): Aconcagua ×3, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol, Deserto de Lut ×9, Deserto de Mojave, Ilha Devon - Haughton ×2, Ladakh ×5, Lanzarote, Namibe ×9, Planalto do Tibete - Changtang ×8, Rub al Khali ×9, Saara - Tanezrouft ×9, Utah - MDRS ×8, Vale da Morte ×4, Vales Secos de McMurdo, Wadi Rum ×9
- **Cluster 1** — alvos: MOON (54), MARS (21); Terra (0 recortes): nenhum
- **Cluster 2** — alvos: MARS (8); Terra (108 recortes): Aconcagua ×6, Atacama - Chajnantor ×9, Danakil - Dallol ×5, Deserto de Mojave, Gobi ×9, Islandia - Askja ×9, Kilimanjaro ×9, Lanzarote ×8, Licancabur ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE], Ojos del Salado ×9, Pilbara ×7, Rio Tinto ×4, Svalbard - Bockfjorden ×3, Teide ×9, Vale da Morte

## k = 8

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      89 |     16 |      0 |
|         1 |       0 |     21 |     54 |
|         2 |     108 |      8 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |      53 |      0 |      0 |
|         5 |      74 |      0 |      0 |
|         6 |      12 |      0 |      0 |
|         7 |       9 |      0 |      0 |

- **Cluster 0** — alvos: MARS (16); Terra (89 recortes): Aconcagua ×3, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol, Deserto de Lut ×9, Deserto de Mojave, Ilha Devon - Haughton ×2, Ladakh ×5, Lanzarote, Namibe ×9, Planalto do Tibete - Changtang ×8, Rub al Khali ×9, Saara - Tanezrouft ×9, Utah - MDRS ×8, Vale da Morte ×4, Vales Secos de McMurdo, Wadi Rum ×9
- **Cluster 1** — alvos: MOON (54), MARS (21); Terra (0 recortes): nenhum
- **Cluster 2** — alvos: MARS (8); Terra (108 recortes): Aconcagua ×6, Atacama - Chajnantor ×9, Danakil - Dallol ×5, Deserto de Mojave, Gobi ×9, Islandia - Askja ×9, Kilimanjaro ×9, Lanzarote ×8, Licancabur ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE], Ojos del Salado ×9, Pilbara ×7, Rio Tinto ×4, Svalbard - Bockfjorden ×3, Teide ×9, Vale da Morte

## k = 9

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |       0 |     21 |     54 |
|         1 |      88 |     16 |      0 |
|         2 |     108 |      8 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |      53 |      0 |      0 |
|         5 |      74 |      0 |      0 |
|         6 |      10 |      0 |      0 |
|         7 |      10 |      0 |      0 |
|         8 |       2 |      0 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (21); Terra (0 recortes): nenhum
- **Cluster 1** — alvos: MARS (16); Terra (88 recortes): Aconcagua ×3, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol, Deserto de Lut ×9, Deserto de Mojave, Ilha Devon - Haughton, Ladakh ×5, Lanzarote, Namibe ×9, Planalto do Tibete - Changtang ×8, Rub al Khali ×9, Saara - Tanezrouft ×9, Utah - MDRS ×8, Vale da Morte ×4, Vales Secos de McMurdo, Wadi Rum ×9
- **Cluster 2** — alvos: MARS (8); Terra (108 recortes): Aconcagua ×6, Atacama - Chajnantor ×9, Danakil - Dallol ×5, Deserto de Mojave, Gobi ×9, Islandia - Askja ×9, Kilimanjaro ×9, Lanzarote ×8, Licancabur ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE], Ojos del Salado ×9, Pilbara ×7, Rio Tinto ×4, Svalbard - Bockfjorden ×3, Teide ×9, Vale da Morte

## k = 10

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      76 |     11 |      0 |
|         1 |       0 |     21 |     54 |
|         2 |      36 |      0 |      0 |
|         3 |     108 |      8 |      0 |
|         4 |      53 |      0 |      0 |
|         5 |      70 |      0 |      0 |
|         6 |      10 |      0 |      0 |
|         7 |      10 |      0 |      0 |
|         8 |      16 |      5 |      0 |
|         9 |       2 |      0 |      0 |

- **Cluster 0** — alvos: MARS (11); Terra (76 recortes): Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol, Deserto de Lut ×9, Ilha Devon - Haughton, Ladakh ×2, Namibe ×9, Planalto do Tibete - Changtang ×4, Rub al Khali ×9, Saara - Tanezrouft ×9, Utah - MDRS ×8, Vale da Morte ×4, Vales Secos de McMurdo, Wadi Rum ×9
- **Cluster 1** — alvos: MOON (54), MARS (21); Terra (0 recortes): nenhum
- **Cluster 3** — alvos: MARS (8); Terra (108 recortes): Aconcagua ×6, Atacama - Chajnantor ×9, Danakil - Dallol ×5, Deserto de Mojave, Gobi ×9, Islandia - Askja ×9, Kilimanjaro ×9, Lanzarote ×8, Licancabur ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE], Ojos del Salado ×9, Pilbara ×7, Rio Tinto ×4, Svalbard - Bockfjorden ×3, Teide ×9, Vale da Morte
- **Cluster 8** — alvos: MARS (5); Terra (16 recortes): Aconcagua ×3, Deserto de Mojave ×2, Deserto de Simpson, Ilha Devon - Haughton, Ladakh ×3, Lanzarote, Planalto do Tibete - Changtang ×4, Svalbard - Bockfjorden

---
Locais marcados [CONTROLE] (cidades/florestas) caindo junto com Lua/Marte indicam que o cluster é grosseiro demais para aquele k.

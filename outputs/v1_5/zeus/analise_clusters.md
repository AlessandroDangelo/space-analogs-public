# Análise dos clusters ZEUS

475 recortes: EARTH=376, MOON=54, MARS=45 | protocolo: v1_5

## Qualidade por k

`silhueta_embedding`: separação dos clusters no espaço do ZEUS (-1 a 1, maior = melhor). `ari_medio_entre_sementes`: 1 = o K-Means dá o mesmo resultado com sementes diferentes.

|   k |   silhueta_embedding |   ari_medio_entre_sementes |   inercia | tamanhos                      |
|----:|---------------------:|---------------------------:|----------:|:------------------------------|
|   2 |             0.652014 |                   1        | 36252.8   | 439 36                        |
|   3 |             0.56671  |                   1        | 18892.6   | 299 36 140                    |
|   4 |             0.649594 |                   1        | 11443.5   | 273 124 36 42                 |
|   5 |             0.72506  |                   1        |  6024.54  | 42 197 36 96 104              |
|   6 |             0.810756 |                   1        |  2254.52  | 197 96 42 36 63 41            |
|   7 |             0.777029 |                   1        |  1402.93  | 96 125 36 63 41 26 88         |
|   8 |             0.811159 |                   1        |   882.073 | 96 118 36 63 24 41 79 18      |
|   9 |             0.814768 |                   1        |   629.145 | 63 115 36 89 41 24 13 17 77   |
|  10 |             0.818412 |                   0.993416 |   460.342 | 89 63 36 114 39 24 17 77 13 3 |

## Checagem de sanidade: recortes do mesmo local

ARI entre cluster e `site_id`. Com k pequeno e muitos locais o ARI é naturalmente baixo; a coluna de locais "inteiros" é a leitura mais direta.

|   k |   ARI_vs_site_id | locais_com_todos_recortes_no_mesmo_cluster   |
|----:|-----------------:|:---------------------------------------------|
|   2 |            0.006 | 54/54                                        |
|   3 |            0.029 | 43/54                                        |
|   4 |            0.039 | 41/54                                        |
|   5 |            0.071 | 38/54                                        |
|   6 |            0.08  | 38/54                                        |
|   7 |            0.118 | 35/54                                        |
|   8 |            0.125 | 33/54                                        |
|   9 |            0.131 | 33/54                                        |
|  10 |            0.132 | 33/54                                        |

## k = 2

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     340 |     45 |     54 |
|         1 |      36 |      0 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (45); Terra (340 recortes): Aconcagua ×9, Arkaroola ×9, Atacama - Chajnantor ×9, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Denali ×7, Deserto de Lut ×9, Deserto de Mojave ×9, Deserto de Simpson ×9, Everest ×9, Gobi ×9, Ilha Devon - Haughton ×9, Islandia - Askja ×9, Kilimanjaro ×9, Ladakh ×9, Lanzarote ×9, Licancabur ×9, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×9, Mauna Loa - HI-SEAS ×9, Namibe ×9, Nova York [CONTROLE] ×9, Ojos del Salado ×9, Oymyakon ×9, Pilbara ×9, Planalto do Tibete - Changtang ×9, Rio Tinto ×9, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×9, Singapura [CONTROLE] ×9, Svalbard - Bockfjorden ×9, Teide ×9, Utah - MDRS ×9, Vale da Morte ×9, Wadi Rum ×9

## k = 3

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     200 |     45 |     54 |
|         1 |      36 |      0 |      0 |
|         2 |     140 |      0 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (45); Terra (200 recortes): Atacama - Chajnantor ×7, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Deserto de Lut ×9, Deserto de Mojave, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×9, Ladakh ×4, Lanzarote ×5, Licancabur ×7, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×5, Mauna Loa - HI-SEAS ×5, Namibe ×9, Nova York [CONTROLE] ×9, Ojos del Salado ×5, Planalto do Tibete - Changtang ×4, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×9, Singapura [CONTROLE] ×9, Svalbard - Bockfjorden ×3, Utah - MDRS ×9, Vale da Morte ×9, Wadi Rum ×9

## k = 4

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     174 |     45 |     54 |
|         1 |     124 |      0 |      0 |
|         2 |      36 |      0 |      0 |
|         3 |      42 |      0 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (45); Terra (174 recortes): Aconcagua ×7, Atacama - Chajnantor ×7, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Deserto de Lut ×9, Deserto de Mojave, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×9, Kilimanjaro, Ladakh ×9, Lanzarote ×5, Licancabur ×7, Mauna Loa - HI-SEAS ×5, Namibe ×9, Ojos del Salado ×7, Planalto do Tibete - Changtang ×4, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Singapura [CONTROLE], Svalbard - Bockfjorden ×2, Utah - MDRS ×9, Vale da Morte ×9, Wadi Rum ×9

## k = 5

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      42 |      0 |      0 |
|         1 |     157 |     40 |      0 |
|         2 |      36 |      0 |      0 |
|         3 |      96 |      0 |      0 |
|         4 |      45 |      5 |     54 |

- **Cluster 1** — alvos: MARS (40); Terra (157 recortes): Atacama - Chajnantor ×7, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Deserto de Lut ×9, Deserto de Mojave ×2, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×9, Ladakh ×4, Lanzarote ×5, Licancabur ×8, Mauna Loa - HI-SEAS ×2, Namibe ×9, Ojos del Salado ×5, Planalto do Tibete - Changtang ×4, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Singapura [CONTROLE], Svalbard - Bockfjorden ×2, Utah - MDRS ×9, Vale da Morte ×8, Wadi Rum ×9
- **Cluster 4** — alvos: MOON (54), MARS (5); Terra (45 recortes): Aconcagua ×9, Denali ×7, Everest ×8, Kilimanjaro, Ladakh ×5, Mauna Loa - HI-SEAS ×4, Ojos del Salado ×4, Svalbard - Bockfjorden ×6, Vale da Morte

## k = 6

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     157 |     40 |      0 |
|         1 |      96 |      0 |      0 |
|         2 |      42 |      0 |      0 |
|         3 |      36 |      0 |      0 |
|         4 |       4 |      5 |     54 |
|         5 |      41 |      0 |      0 |

- **Cluster 0** — alvos: MARS (40); Terra (157 recortes): Atacama - Chajnantor ×7, Atacama - Yungay ×9, Bacia de Qaidam ×9, Danakil - Dallol ×9, Deserto de Lut ×9, Deserto de Mojave ×2, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×9, Ladakh ×4, Lanzarote ×5, Licancabur ×8, Mauna Loa - HI-SEAS ×2, Namibe ×9, Ojos del Salado ×5, Planalto do Tibete - Changtang ×4, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Singapura [CONTROLE], Svalbard - Bockfjorden ×2, Utah - MDRS ×9, Vale da Morte ×8, Wadi Rum ×9
- **Cluster 4** — alvos: MOON (54), MARS (5); Terra (4 recortes): Mauna Loa - HI-SEAS ×4

## k = 7

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      96 |      0 |      0 |
|         1 |      86 |     39 |      0 |
|         2 |      36 |      0 |      0 |
|         3 |       4 |      5 |     54 |
|         4 |      41 |      0 |      0 |
|         5 |      26 |      0 |      0 |
|         6 |      87 |      1 |      0 |

- **Cluster 1** — alvos: MARS (39); Terra (86 recortes): Atacama - Chajnantor, Atacama - Yungay, Bacia de Qaidam ×9, Danakil - Dallol ×7, Deserto de Lut ×9, Gobi ×9, Ilha Devon - Haughton, Islandia - Askja ×3, Lanzarote ×2, Manaus [CONTROLE], Mauna Loa - HI-SEAS, Planalto do Tibete - Changtang, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Singapura [CONTROLE], Utah - MDRS ×9, Vale da Morte ×4
- **Cluster 3** — alvos: MOON (54), MARS (5); Terra (4 recortes): Mauna Loa - HI-SEAS ×4
- **Cluster 6** — alvos: MARS (1); Terra (87 recortes): Aconcagua ×7, Atacama - Chajnantor ×6, Atacama - Yungay ×8, Danakil - Dallol ×2, Deserto de Mojave ×2, Islandia - Askja ×6, Kilimanjaro, Ladakh ×9, Lanzarote ×3, Licancabur ×8, Mauna Loa - HI-SEAS, Namibe ×9, Ojos del Salado ×6, Planalto do Tibete - Changtang ×3, Svalbard - Bockfjorden ×2, Vale da Morte ×5, Wadi Rum ×9

## k = 8

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      96 |      0 |      0 |
|         1 |      79 |     39 |      0 |
|         2 |      36 |      0 |      0 |
|         3 |       4 |      5 |     54 |
|         4 |      24 |      0 |      0 |
|         5 |      41 |      0 |      0 |
|         6 |      78 |      1 |      0 |
|         7 |      18 |      0 |      0 |

- **Cluster 1** — alvos: MARS (39); Terra (79 recortes): Atacama - Chajnantor, Bacia de Qaidam ×9, Danakil - Dallol ×7, Deserto de Lut ×8, Gobi ×9, Islandia - Askja ×3, Lanzarote, Manaus [CONTROLE], Mauna Loa - HI-SEAS, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Singapura [CONTROLE], Utah - MDRS ×8, Vale da Morte ×3
- **Cluster 3** — alvos: MOON (54), MARS (5); Terra (4 recortes): Mauna Loa - HI-SEAS ×4
- **Cluster 6** — alvos: MARS (1); Terra (78 recortes): Atacama - Chajnantor ×6, Atacama - Yungay ×9, Danakil - Dallol ×2, Deserto de Lut, Deserto de Mojave ×2, Ilha Devon - Haughton, Islandia - Askja ×6, Ladakh ×4, Lanzarote ×4, Licancabur ×7, Mauna Loa - HI-SEAS, Namibe ×9, Ojos del Salado ×5, Planalto do Tibete - Changtang ×4, Svalbard - Bockfjorden ×2, Utah - MDRS, Vale da Morte ×5, Wadi Rum ×9

## k = 9

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |       4 |      5 |     54 |
|         1 |      76 |     39 |      0 |
|         2 |      36 |      0 |      0 |
|         3 |      89 |      0 |      0 |
|         4 |      41 |      0 |      0 |
|         5 |      24 |      0 |      0 |
|         6 |      13 |      0 |      0 |
|         7 |      17 |      0 |      0 |
|         8 |      76 |      1 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (5); Terra (4 recortes): Mauna Loa - HI-SEAS ×4
- **Cluster 1** — alvos: MARS (39); Terra (76 recortes): Atacama - Chajnantor, Bacia de Qaidam ×9, Danakil - Dallol ×7, Deserto de Lut ×8, Gobi ×9, Islandia - Askja ×3, Lanzarote, Manaus [CONTROLE], Mauna Loa - HI-SEAS, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Utah - MDRS ×6, Vale da Morte ×3
- **Cluster 8** — alvos: MARS (1); Terra (76 recortes): Atacama - Chajnantor ×6, Atacama - Yungay ×9, Danakil - Dallol ×2, Deserto de Lut, Deserto de Mojave, Ilha Devon - Haughton, Islandia - Askja ×6, Ladakh ×4, Lanzarote ×2, Licancabur ×7, Namibe ×9, Ojos del Salado ×5, Planalto do Tibete - Changtang ×4, Svalbard - Bockfjorden ×2, Utah - MDRS ×3, Vale da Morte ×5, Wadi Rum ×9

## k = 10

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      89 |      0 |      0 |
|         1 |       4 |      5 |     54 |
|         2 |      36 |      0 |      0 |
|         3 |      75 |     39 |      0 |
|         4 |      39 |      0 |      0 |
|         5 |      24 |      0 |      0 |
|         6 |      17 |      0 |      0 |
|         7 |      76 |      1 |      0 |
|         8 |      13 |      0 |      0 |
|         9 |       3 |      0 |      0 |

- **Cluster 1** — alvos: MOON (54), MARS (5); Terra (4 recortes): Mauna Loa - HI-SEAS ×4
- **Cluster 3** — alvos: MARS (39); Terra (75 recortes): Atacama - Chajnantor, Bacia de Qaidam ×9, Danakil - Dallol ×7, Deserto de Lut ×8, Gobi ×9, Islandia - Askja ×3, Lanzarote, Mauna Loa - HI-SEAS, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Utah - MDRS ×6, Vale da Morte ×3
- **Cluster 7** — alvos: MARS (1); Terra (76 recortes): Atacama - Chajnantor ×6, Atacama - Yungay ×9, Danakil - Dallol ×2, Deserto de Lut, Deserto de Mojave, Ilha Devon - Haughton, Islandia - Askja ×6, Ladakh ×4, Lanzarote ×2, Licancabur ×7, Namibe ×9, Ojos del Salado ×5, Planalto do Tibete - Changtang ×4, Svalbard - Bockfjorden ×2, Utah - MDRS ×3, Vale da Morte ×5, Wadi Rum ×9

---
Locais marcados [CONTROLE] (cidades/florestas) caindo junto com Lua/Marte indicam que o cluster é grosseiro demais para aquele k.

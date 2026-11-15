# Análise dos clusters ZEUS

484 recortes: EARTH=385, MOON=54, MARS=45 | protocolo: v1_4

## Qualidade por k

`silhueta_embedding`: separação dos clusters no espaço do ZEUS (-1 a 1, maior = melhor). `ari_medio_entre_sementes`: 1 = o K-Means dá o mesmo resultado com sementes diferentes.

|   k |   silhueta_embedding |   ari_medio_entre_sementes |   inercia | tamanhos                      |
|----:|---------------------:|---------------------------:|----------:|:------------------------------|
|   2 |             0.684795 |                   1        | 31748.5   | 311 173                       |
|   3 |             0.835158 |                   1        |  6569.29  | 66 176 242                    |
|   4 |             0.821272 |                   1        |  3895.97  | 148 241 65 30                 |
|   5 |             0.775097 |                   1        |  1869.86  | 28 143 218 65 30              |
|   6 |             0.679279 |                   1        |  1300     | 143 65 65 30 20 161           |
|   7 |             0.672744 |                   1        |  1046.4   | 143 128 65 30 33 67 18        |
|   8 |             0.670122 |                   0.997356 |   858.065 | 65 41 140 30 117 9 20 62      |
|   9 |             0.557549 |                   0.976505 |   704.586 | 61 76 65 42 30 117 20 9 64    |
|  10 |             0.558167 |                   0.996449 |   607.96  | 30 44 65 76 59 23 101 8 64 14 |

## Checagem de sanidade: recortes do mesmo local

ARI entre cluster e `site_id`. Com k pequeno e muitos locais o ARI é naturalmente baixo; a coluna de locais "inteiros" é a leitura mais direta.

|   k |   ARI_vs_site_id | locais_com_todos_recortes_no_mesmo_cluster   |
|----:|-----------------:|:---------------------------------------------|
|   2 |            0.021 | 39/55                                        |
|   3 |            0.039 | 38/55                                        |
|   4 |            0.045 | 37/55                                        |
|   5 |            0.053 | 34/55                                        |
|   6 |            0.07  | 27/55                                        |
|   7 |            0.088 | 27/55                                        |
|   8 |            0.092 | 26/55                                        |
|   9 |            0.11  | 22/55                                        |
|  10 |            0.114 | 21/55                                        |

## k = 2

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     213 |     44 |     54 |
|         1 |     172 |      1 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (44); Terra (213 recortes): Atacama - Chajnantor, Atacama - Yungay ×4, Bacia de Qaidam ×9, Danakil - Dallol ×8, Deserto de Lut ×9, Deserto de Mojave ×2, Deserto de Simpson ×9, Dome Argus ×9, Dome C ×9, Gobi ×9, Groenlandia - Summit ×9, Ilha Devon - Haughton ×6, Islandia - Askja ×5, Kilimanjaro, Lanzarote ×7, Licancabur, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×9, Mauna Loa - HI-SEAS ×9, Nova York [CONTROLE] ×9, Oymyakon ×5, Pilbara, Planalto do Tibete - Changtang ×7, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×9, Svalbard - Bockfjorden, Utah - MDRS ×9, Vale da Morte ×4, Vostok ×9
- **Cluster 1** — alvos: MARS (1); Terra (172 recortes): Aconcagua ×9, Arkaroola ×9, Atacama - Chajnantor ×8, Atacama - Yungay ×5, Danakil - Dallol, Denali ×7, Deserto de Mojave ×7, Everest ×9, Ilha Devon - Haughton ×3, Islandia - Askja ×4, Kilimanjaro ×8, Ladakh ×9, Lanzarote ×2, Licancabur ×8, Namibe ×9, Ojos del Salado ×9, Oymyakon ×4, Pilbara ×8, Planalto do Tibete - Changtang ×2, Rio Tinto ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×8, Teide ×9, Vale da Morte ×5, Vales Secos de McMurdo ×9, Wadi Rum ×9

## k = 3

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |       7 |      5 |     54 |
|         1 |     175 |      1 |      0 |
|         2 |     203 |     39 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (5); Terra (7 recortes): Kilimanjaro, Mauna Loa - HI-SEAS ×6
- **Cluster 1** — alvos: MARS (1); Terra (175 recortes): Aconcagua ×9, Arkaroola ×9, Atacama - Chajnantor ×8, Atacama - Yungay ×6, Danakil - Dallol, Denali ×7, Deserto de Mojave ×7, Everest ×9, Ilha Devon - Haughton ×3, Islandia - Askja ×4, Kilimanjaro ×8, Ladakh ×9, Lanzarote ×2, Licancabur ×8, Namibe ×9, Ojos del Salado ×9, Oymyakon ×5, Pilbara ×8, Planalto do Tibete - Changtang ×3, Rio Tinto ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×8, Teide ×9, Vale da Morte ×5, Vales Secos de McMurdo ×9, Wadi Rum ×9
- **Cluster 2** — alvos: MARS (39); Terra (203 recortes): Atacama - Chajnantor, Atacama - Yungay ×3, Bacia de Qaidam ×9, Danakil - Dallol ×8, Deserto de Lut ×9, Deserto de Mojave ×2, Deserto de Simpson ×9, Dome Argus ×9, Dome C ×9, Gobi ×9, Groenlandia - Summit ×9, Ilha Devon - Haughton ×6, Islandia - Askja ×5, Lanzarote ×7, Licancabur, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×9, Mauna Loa - HI-SEAS ×3, Nova York [CONTROLE] ×9, Oymyakon ×4, Pilbara, Planalto do Tibete - Changtang ×6, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×9, Svalbard - Bockfjorden, Utah - MDRS ×9, Vale da Morte ×4, Vostok ×9

## k = 4

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     147 |      1 |      0 |
|         1 |     202 |     39 |      0 |
|         2 |       6 |      5 |     54 |
|         3 |      30 |      0 |      0 |

- **Cluster 0** — alvos: MARS (1); Terra (147 recortes): Arkaroola ×9, Atacama - Chajnantor ×8, Atacama - Yungay ×7, Danakil - Dallol, Deserto de Mojave ×7, Everest, Ilha Devon - Haughton ×3, Islandia - Askja ×4, Kilimanjaro ×9, Ladakh ×4, Lanzarote ×2, Licancabur ×8, Namibe ×9, Ojos del Salado ×9, Oymyakon ×5, Pilbara ×8, Planalto do Tibete - Changtang ×3, Rio Tinto ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×8, Teide ×9, Vale da Morte ×4, Vales Secos de McMurdo ×9, Wadi Rum ×9
- **Cluster 1** — alvos: MARS (39); Terra (202 recortes): Atacama - Chajnantor, Atacama - Yungay ×2, Bacia de Qaidam ×9, Danakil - Dallol ×8, Deserto de Lut ×9, Deserto de Mojave ×2, Deserto de Simpson ×9, Dome Argus ×9, Dome C ×9, Gobi ×9, Groenlandia - Summit ×9, Ilha Devon - Haughton ×6, Islandia - Askja ×5, Lanzarote ×7, Licancabur, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×9, Mauna Loa - HI-SEAS ×3, Nova York [CONTROLE] ×9, Oymyakon ×4, Pilbara, Planalto do Tibete - Changtang ×6, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×9, Svalbard - Bockfjorden, Utah - MDRS ×9, Vale da Morte ×4, Vostok ×9
- **Cluster 2** — alvos: MOON (54), MARS (5); Terra (6 recortes): Mauna Loa - HI-SEAS ×6

## k = 5

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      28 |      0 |      0 |
|         1 |     142 |      1 |      0 |
|         2 |     179 |     39 |      0 |
|         3 |       6 |      5 |     54 |
|         4 |      30 |      0 |      0 |

- **Cluster 1** — alvos: MARS (1); Terra (142 recortes): Arkaroola ×9, Atacama - Chajnantor ×8, Atacama - Yungay ×5, Danakil - Dallol, Deserto de Mojave ×7, Everest, Ilha Devon - Haughton ×3, Islandia - Askja ×4, Kilimanjaro ×8, Ladakh ×4, Lanzarote ×2, Licancabur ×8, Namibe ×9, Ojos del Salado ×9, Oymyakon ×4, Pilbara ×8, Planalto do Tibete - Changtang ×2, Rio Tinto ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×8, Teide ×9, Vale da Morte ×4, Vales Secos de McMurdo ×9, Wadi Rum ×9
- **Cluster 2** — alvos: MARS (39); Terra (179 recortes): Atacama - Chajnantor, Bacia de Qaidam ×9, Danakil - Dallol ×7, Deserto de Lut ×8, Deserto de Mojave ×2, Deserto de Simpson ×9, Dome Argus ×9, Dome C ×9, Gobi ×9, Groenlandia - Summit ×9, Ilha Devon - Haughton ×6, Islandia - Askja ×2, Lanzarote ×3, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×9, Mauna Loa - HI-SEAS ×2, Nova York [CONTROLE] ×9, Oymyakon ×2, Pilbara, Rub al Khali ×9, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×9, Svalbard - Bockfjorden, Utah - MDRS ×8, Vale da Morte ×3, Vostok ×9
- **Cluster 3** — alvos: MOON (54), MARS (5); Terra (6 recortes): Mauna Loa - HI-SEAS ×6

## k = 6

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     142 |      1 |      0 |
|         1 |      55 |     10 |      0 |
|         2 |       6 |      5 |     54 |
|         3 |      30 |      0 |      0 |
|         4 |      20 |      0 |      0 |
|         5 |     132 |     29 |      0 |

- **Cluster 0** — alvos: MARS (1); Terra (142 recortes): Arkaroola ×9, Atacama - Chajnantor ×8, Atacama - Yungay ×5, Danakil - Dallol, Deserto de Mojave ×7, Everest, Ilha Devon - Haughton ×3, Islandia - Askja ×4, Kilimanjaro ×8, Ladakh ×4, Lanzarote ×2, Licancabur ×8, Namibe ×9, Ojos del Salado ×9, Oymyakon ×4, Pilbara ×8, Planalto do Tibete - Changtang ×2, Rio Tinto ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×8, Teide ×9, Vale da Morte ×4, Vales Secos de McMurdo ×9, Wadi Rum ×9
- **Cluster 1** — alvos: MARS (10); Terra (55 recortes): Atacama - Chajnantor, Atacama - Yungay, Bacia de Qaidam ×2, Deserto de Lut ×2, Deserto de Mojave ×2, Ilha Devon - Haughton ×6, Islandia - Askja ×2, Lanzarote ×3, Londres [CONTROLE], Manaus [CONTROLE] ×4, Mauna Loa - HI-SEAS ×3, Nova York [CONTROLE] ×2, Pilbara, Rub al Khali ×4, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×2, Utah - MDRS ×9, Vale da Morte ×3
- **Cluster 2** — alvos: MOON (54), MARS (5); Terra (6 recortes): Mauna Loa - HI-SEAS ×6
- **Cluster 5** — alvos: MARS (29); Terra (132 recortes): Bacia de Qaidam ×7, Danakil - Dallol ×7, Deserto de Lut ×7, Deserto de Simpson ×9, Dome Argus ×9, Dome C ×9, Gobi ×9, Groenlandia - Summit ×9, Islandia - Askja, Lanzarote ×2, Londres [CONTROLE] ×8, Manaus [CONTROLE] ×5, Nova York [CONTROLE] ×7, Oymyakon ×2, Rub al Khali ×5, Saara - Tanezrouft ×9, Salar de Uyuni ×9, Singapura [CONTROLE] ×7, Svalbard - Bockfjorden, Vale da Morte, Vostok ×9

## k = 7

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |     142 |      1 |      0 |
|         1 |      94 |     34 |      0 |
|         2 |       6 |      5 |     54 |
|         3 |      30 |      0 |      0 |
|         4 |      28 |      5 |      0 |
|         5 |      67 |      0 |      0 |
|         6 |      18 |      0 |      0 |

- **Cluster 0** — alvos: MARS (1); Terra (142 recortes): Arkaroola ×9, Atacama - Chajnantor ×8, Atacama - Yungay ×5, Danakil - Dallol, Deserto de Mojave ×7, Everest, Ilha Devon - Haughton ×3, Islandia - Askja ×4, Kilimanjaro ×8, Ladakh ×4, Lanzarote ×2, Licancabur ×8, Namibe ×9, Ojos del Salado ×9, Oymyakon ×4, Pilbara ×8, Planalto do Tibete - Changtang ×2, Rio Tinto ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×8, Teide ×9, Vale da Morte ×4, Vales Secos de McMurdo ×9, Wadi Rum ×9
- **Cluster 1** — alvos: MARS (34); Terra (94 recortes): Bacia de Qaidam ×8, Danakil - Dallol, Deserto de Lut ×8, Deserto de Mojave ×2, Deserto de Simpson ×9, Gobi ×9, Ilha Devon - Haughton ×2, Islandia - Askja, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×6, Mauna Loa - HI-SEAS, Nova York [CONTROLE] ×8, Oymyakon ×2, Rub al Khali ×9, Saara - Tanezrouft, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×7, Svalbard - Bockfjorden, Utah - MDRS, Vale da Morte ×2
- **Cluster 2** — alvos: MOON (54), MARS (5); Terra (6 recortes): Mauna Loa - HI-SEAS ×6
- **Cluster 4** — alvos: MARS (5); Terra (28 recortes): Atacama - Chajnantor, Atacama - Yungay, Deserto de Lut, Ilha Devon - Haughton ×4, Islandia - Askja ×2, Lanzarote ×4, Manaus [CONTROLE], Mauna Loa - HI-SEAS ×2, Pilbara, Planalto do Tibete - Changtang, Utah - MDRS ×8, Vale da Morte ×2

## k = 8

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |       6 |      5 |     54 |
|         1 |      32 |      9 |      0 |
|         2 |     139 |      1 |      0 |
|         3 |      30 |      0 |      0 |
|         4 |      87 |     30 |      0 |
|         5 |       9 |      0 |      0 |
|         6 |      20 |      0 |      0 |
|         7 |      62 |      0 |      0 |

- **Cluster 0** — alvos: MOON (54), MARS (5); Terra (6 recortes): Mauna Loa - HI-SEAS ×6
- **Cluster 1** — alvos: MARS (9); Terra (32 recortes): Atacama - Chajnantor, Deserto de Lut, Deserto de Mojave, Ilha Devon - Haughton ×6, Islandia - Askja, Lanzarote ×2, Manaus [CONTROLE] ×2, Mauna Loa - HI-SEAS ×2, Nova York [CONTROLE], Pilbara, Rub al Khali, Sao Paulo [CONTROLE] ×2, Singapura [CONTROLE], Utah - MDRS ×8, Vale da Morte ×2
- **Cluster 2** — alvos: MARS (1); Terra (139 recortes): Arkaroola ×9, Atacama - Chajnantor ×8, Atacama - Yungay ×4, Danakil - Dallol, Deserto de Mojave ×7, Everest, Ilha Devon - Haughton ×3, Islandia - Askja ×4, Kilimanjaro ×8, Ladakh ×4, Lanzarote ×2, Licancabur ×7, Namibe ×9, Ojos del Salado ×9, Oymyakon ×3, Pilbara ×8, Planalto do Tibete - Changtang ×2, Rio Tinto ×9, Sao Paulo [CONTROLE] ×2, Svalbard - Bockfjorden ×8, Teide ×9, Vale da Morte ×4, Vales Secos de McMurdo ×9, Wadi Rum ×9
- **Cluster 4** — alvos: MARS (30); Terra (87 recortes): Bacia de Qaidam ×8, Danakil - Dallol ×3, Deserto de Lut ×8, Deserto de Mojave, Deserto de Simpson ×9, Gobi ×9, Islandia - Askja, Lanzarote ×2, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×5, Nova York [CONTROLE] ×8, Oymyakon ×2, Rub al Khali ×8, Saara - Tanezrouft, Sao Paulo [CONTROLE] ×5, Singapura [CONTROLE] ×6, Svalbard - Bockfjorden, Vale da Morte

## k = 9

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      61 |      0 |      0 |
|         1 |      76 |      0 |      0 |
|         2 |       6 |      5 |     54 |
|         3 |      32 |     10 |      0 |
|         4 |      30 |      0 |      0 |
|         5 |      88 |     29 |      0 |
|         6 |      20 |      0 |      0 |
|         7 |       9 |      0 |      0 |
|         8 |      63 |      1 |      0 |

- **Cluster 2** — alvos: MOON (54), MARS (5); Terra (6 recortes): Mauna Loa - HI-SEAS ×6
- **Cluster 3** — alvos: MARS (10); Terra (32 recortes): Atacama - Chajnantor, Deserto de Lut, Deserto de Mojave, Ilha Devon - Haughton ×6, Islandia - Askja, Lanzarote ×2, Manaus [CONTROLE] ×2, Mauna Loa - HI-SEAS ×2, Nova York [CONTROLE], Pilbara, Rub al Khali, Sao Paulo [CONTROLE] ×2, Singapura [CONTROLE], Utah - MDRS ×8, Vale da Morte ×2
- **Cluster 5** — alvos: MARS (29); Terra (88 recortes): Bacia de Qaidam ×8, Danakil - Dallol ×4, Deserto de Lut ×8, Deserto de Mojave, Deserto de Simpson ×9, Gobi ×9, Islandia - Askja, Lanzarote ×2, Londres [CONTROLE] ×9, Manaus [CONTROLE] ×5, Nova York [CONTROLE] ×8, Oymyakon ×2, Rub al Khali ×8, Saara - Tanezrouft, Sao Paulo [CONTROLE] ×5, Singapura [CONTROLE] ×6, Svalbard - Bockfjorden, Vale da Morte
- **Cluster 8** — alvos: MARS (1); Terra (63 recortes): Arkaroola ×4, Atacama - Chajnantor ×3, Atacama - Yungay, Danakil - Dallol, Deserto de Mojave, Everest, Ilha Devon - Haughton, Kilimanjaro ×7, Ladakh ×3, Licancabur ×3, Ojos del Salado ×8, Oymyakon, Planalto do Tibete - Changtang, Svalbard - Bockfjorden ×5, Teide ×9, Vale da Morte ×3, Vales Secos de McMurdo ×5, Wadi Rum ×6

## k = 10

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      30 |      0 |      0 |
|         1 |      37 |      7 |      0 |
|         2 |       6 |      5 |     54 |
|         3 |      76 |      0 |      0 |
|         4 |      59 |      0 |      0 |
|         5 |      20 |      3 |      0 |
|         6 |      72 |     29 |      0 |
|         7 |       8 |      0 |      0 |
|         8 |      63 |      1 |      0 |
|         9 |      14 |      0 |      0 |

- **Cluster 1** — alvos: MARS (7); Terra (37 recortes): Bacia de Qaidam ×2, Deserto de Lut, Deserto de Mojave ×2, Ilha Devon - Haughton ×5, Londres [CONTROLE], Manaus [CONTROLE] ×4, Mauna Loa - HI-SEAS, Nova York [CONTROLE] ×2, Rub al Khali ×5, Sao Paulo [CONTROLE] ×7, Singapura [CONTROLE] ×2, Utah - MDRS ×4, Vale da Morte
- **Cluster 2** — alvos: MOON (54), MARS (5); Terra (6 recortes): Mauna Loa - HI-SEAS ×6
- **Cluster 5** — alvos: MARS (3); Terra (20 recortes): Atacama - Chajnantor, Atacama - Yungay, Deserto de Lut, Ilha Devon - Haughton, Islandia - Askja ×2, Lanzarote ×4, Mauna Loa - HI-SEAS ×2, Pilbara, Utah - MDRS ×5, Vale da Morte ×2
- **Cluster 6** — alvos: MARS (29); Terra (72 recortes): Bacia de Qaidam ×6, Danakil - Dallol ×4, Deserto de Lut ×7, Deserto de Simpson ×9, Gobi ×9, Islandia - Askja, Lanzarote ×2, Londres [CONTROLE] ×8, Manaus [CONTROLE] ×3, Nova York [CONTROLE] ×7, Oymyakon ×2, Rub al Khali ×4, Saara - Tanezrouft ×3, Singapura [CONTROLE] ×5, Svalbard - Bockfjorden, Vale da Morte
- **Cluster 8** — alvos: MARS (1); Terra (63 recortes): Arkaroola ×4, Atacama - Chajnantor ×3, Atacama - Yungay, Danakil - Dallol, Deserto de Mojave, Everest, Ilha Devon - Haughton, Kilimanjaro ×7, Ladakh ×3, Licancabur ×3, Ojos del Salado ×8, Oymyakon, Planalto do Tibete - Changtang, Svalbard - Bockfjorden ×5, Teide ×9, Vale da Morte ×3, Vales Secos de McMurdo ×5, Wadi Rum ×6

---
Locais marcados [CONTROLE] (cidades/florestas) caindo junto com Lua/Marte indicam que o cluster é grosseiro demais para aquele k.

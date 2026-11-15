# Análise dos clusters ZEUS

45 recortes: EARTH=43, MARS=1, MOON=1 | protocolo: v1_3_1

## Qualidade por k

`silhueta_embedding`: separação dos clusters no espaço do ZEUS (-1 a 1, maior = melhor). `ari_medio_entre_sementes`: 1 = o K-Means dá o mesmo resultado com sementes diferentes.

|   k |   silhueta_embedding |   ari_medio_entre_sementes |   inercia | tamanhos             |
|----:|---------------------:|---------------------------:|----------:|:---------------------|
|   2 |             0.674868 |                          1 | 2422.79   | 24 21                |
|   3 |             0.661379 |                          1 | 1084.65   | 17 15 13             |
|   4 |             0.699971 |                          1 |  611.165  | 10 15 6 14           |
|   5 |             0.722257 |                          1 |  291.483  | 6 10 6 14 9          |
|   6 |             0.736481 |                          1 |  185.23   | 10 9 6 14 1 5        |
|   7 |             0.721199 |                          1 |  108.977  | 14 5 6 6 9 1 4       |
|   8 |             0.728493 |                          1 |   82.0246 | 14 9 5 6 1 5 4 1     |
|   9 |             0.711848 |                          1 |   57.1228 | 9 14 5 5 4 4 1 2 1   |
|  10 |             0.695461 |                          1 |   47.7439 | 3 9 4 14 3 5 1 1 2 3 |

## Checagem de sanidade: recortes do mesmo local

Cada local tem só 1 recorte nesta tabela, então a checagem por `site_id` não se aplica (ARI com `site_id` é ~0 por construção). Ela passa a valer com a grade 3×3 da V1.4.

## k = 2

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      23 |      0 |      1 |
|         1 |      20 |      1 |      0 |

- **Cluster 0** — alvos: MOON (1); Terra (23 recortes): Aconcagua, Arkaroola, Atacama - Chajnantor, Atacama - Yungay, Denali, Deserto de Mojave, Everest, Islandia - Askja, Kilimanjaro, Ladakh, Lanzarote, Licancabur, Mauna Loa - HI-SEAS, Namibe, Ojos del Salado, Pilbara, Planalto do Tibete - Changtang, Rio Tinto, Svalbard - Bockfjorden, Teide, Vale da Morte, Vales Secos de McMurdo, Wadi Rum
- **Cluster 1** — alvos: MARS (1); Terra (20 recortes): Bacia de Qaidam, Danakil - Dallol, Deserto de Lut, Deserto de Simpson, Dome Argus, Dome C, Gobi, Groenlandia - Summit, Ilha Devon - Haughton, Londres [CONTROLE], Manaus [CONTROLE], Nova York [CONTROLE], Oymyakon, Rub al Khali, Saara - Tanezrouft, Salar de Uyuni, Sao Paulo [CONTROLE], Singapura [CONTROLE], Utah - MDRS, Vostok

## k = 3

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      16 |      0 |      1 |
|         1 |      14 |      1 |      0 |
|         2 |      13 |      0 |      0 |

- **Cluster 0** — alvos: MOON (1); Terra (16 recortes): Aconcagua, Arkaroola, Denali, Deserto de Mojave, Everest, Kilimanjaro, Ladakh, Licancabur, Namibe, Ojos del Salado, Rio Tinto, Svalbard - Bockfjorden, Teide, Vale da Morte, Vales Secos de McMurdo, Wadi Rum
- **Cluster 1** — alvos: MARS (1); Terra (14 recortes): Bacia de Qaidam, Danakil - Dallol, Deserto de Lut, Deserto de Simpson, Dome Argus, Dome C, Gobi, Groenlandia - Summit, Londres [CONTROLE], Nova York [CONTROLE], Oymyakon, Saara - Tanezrouft, Salar de Uyuni, Vostok

## k = 4

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      10 |      0 |      0 |
|         1 |      14 |      1 |      0 |
|         2 |       6 |      0 |      0 |
|         3 |      13 |      0 |      1 |

- **Cluster 1** — alvos: MARS (1); Terra (14 recortes): Bacia de Qaidam, Danakil - Dallol, Deserto de Lut, Deserto de Simpson, Dome Argus, Dome C, Gobi, Groenlandia - Summit, Londres [CONTROLE], Nova York [CONTROLE], Oymyakon, Saara - Tanezrouft, Salar de Uyuni, Vostok
- **Cluster 3** — alvos: MOON (1); Terra (13 recortes): Aconcagua, Denali, Deserto de Mojave, Everest, Kilimanjaro, Ladakh, Licancabur, Ojos del Salado, Svalbard - Bockfjorden, Teide, Vale da Morte, Vales Secos de McMurdo, Wadi Rum

## k = 5

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |       6 |      0 |      0 |
|         1 |      10 |      0 |      0 |
|         2 |       6 |      0 |      0 |
|         3 |      13 |      0 |      1 |
|         4 |       8 |      1 |      0 |

- **Cluster 3** — alvos: MOON (1); Terra (13 recortes): Aconcagua, Denali, Deserto de Mojave, Everest, Kilimanjaro, Ladakh, Licancabur, Ojos del Salado, Svalbard - Bockfjorden, Teide, Vale da Morte, Vales Secos de McMurdo, Wadi Rum
- **Cluster 4** — alvos: MARS (1); Terra (8 recortes): Bacia de Qaidam, Danakil - Dallol, Deserto de Lut, Deserto de Simpson, Gobi, Londres [CONTROLE], Nova York [CONTROLE], Saara - Tanezrouft

## k = 6

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      10 |      0 |      0 |
|         1 |       8 |      1 |      0 |
|         2 |       6 |      0 |      0 |
|         3 |      13 |      0 |      1 |
|         4 |       1 |      0 |      0 |
|         5 |       5 |      0 |      0 |

- **Cluster 1** — alvos: MARS (1); Terra (8 recortes): Bacia de Qaidam, Danakil - Dallol, Deserto de Lut, Deserto de Simpson, Gobi, Londres [CONTROLE], Nova York [CONTROLE], Saara - Tanezrouft
- **Cluster 3** — alvos: MOON (1); Terra (13 recortes): Aconcagua, Denali, Deserto de Mojave, Everest, Kilimanjaro, Ladakh, Licancabur, Ojos del Salado, Svalbard - Bockfjorden, Teide, Vale da Morte, Vales Secos de McMurdo, Wadi Rum

## k = 7

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      13 |      0 |      1 |
|         1 |       5 |      0 |      0 |
|         2 |       6 |      0 |      0 |
|         3 |       6 |      0 |      0 |
|         4 |       8 |      1 |      0 |
|         5 |       1 |      0 |      0 |
|         6 |       4 |      0 |      0 |

- **Cluster 0** — alvos: MOON (1); Terra (13 recortes): Aconcagua, Denali, Deserto de Mojave, Everest, Kilimanjaro, Ladakh, Licancabur, Ojos del Salado, Svalbard - Bockfjorden, Teide, Vale da Morte, Vales Secos de McMurdo, Wadi Rum
- **Cluster 4** — alvos: MARS (1); Terra (8 recortes): Bacia de Qaidam, Danakil - Dallol, Deserto de Lut, Deserto de Simpson, Gobi, Londres [CONTROLE], Nova York [CONTROLE], Saara - Tanezrouft

## k = 8

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |      13 |      0 |      1 |
|         1 |       8 |      1 |      0 |
|         2 |       5 |      0 |      0 |
|         3 |       6 |      0 |      0 |
|         4 |       1 |      0 |      0 |
|         5 |       5 |      0 |      0 |
|         6 |       4 |      0 |      0 |
|         7 |       1 |      0 |      0 |

- **Cluster 0** — alvos: MOON (1); Terra (13 recortes): Aconcagua, Denali, Deserto de Mojave, Everest, Kilimanjaro, Ladakh, Licancabur, Ojos del Salado, Svalbard - Bockfjorden, Teide, Vale da Morte, Vales Secos de McMurdo, Wadi Rum
- **Cluster 1** — alvos: MARS (1); Terra (8 recortes): Bacia de Qaidam, Danakil - Dallol, Deserto de Lut, Deserto de Simpson, Gobi, Londres [CONTROLE], Nova York [CONTROLE], Saara - Tanezrouft

## k = 9

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |       8 |      1 |      0 |
|         1 |      13 |      0 |      1 |
|         2 |       5 |      0 |      0 |
|         3 |       5 |      0 |      0 |
|         4 |       4 |      0 |      0 |
|         5 |       4 |      0 |      0 |
|         6 |       1 |      0 |      0 |
|         7 |       2 |      0 |      0 |
|         8 |       1 |      0 |      0 |

- **Cluster 0** — alvos: MARS (1); Terra (8 recortes): Bacia de Qaidam, Danakil - Dallol, Deserto de Lut, Deserto de Simpson, Gobi, Londres [CONTROLE], Nova York [CONTROLE], Saara - Tanezrouft
- **Cluster 1** — alvos: MOON (1); Terra (13 recortes): Aconcagua, Denali, Deserto de Mojave, Everest, Kilimanjaro, Ladakh, Licancabur, Ojos del Salado, Svalbard - Bockfjorden, Teide, Vale da Morte, Vales Secos de McMurdo, Wadi Rum

## k = 10

Composição por corpo:

|   cluster |   EARTH |   MARS |   MOON |
|----------:|--------:|-------:|-------:|
|         0 |       3 |      0 |      0 |
|         1 |       8 |      1 |      0 |
|         2 |       4 |      0 |      0 |
|         3 |      13 |      0 |      1 |
|         4 |       3 |      0 |      0 |
|         5 |       5 |      0 |      0 |
|         6 |       1 |      0 |      0 |
|         7 |       1 |      0 |      0 |
|         8 |       2 |      0 |      0 |
|         9 |       3 |      0 |      0 |

- **Cluster 1** — alvos: MARS (1); Terra (8 recortes): Bacia de Qaidam, Danakil - Dallol, Deserto de Lut, Deserto de Simpson, Gobi, Londres [CONTROLE], Nova York [CONTROLE], Saara - Tanezrouft
- **Cluster 3** — alvos: MOON (1); Terra (13 recortes): Aconcagua, Denali, Deserto de Mojave, Everest, Kilimanjaro, Ladakh, Licancabur, Ojos del Salado, Svalbard - Bockfjorden, Teide, Vale da Morte, Vales Secos de McMurdo, Wadi Rum

---
Locais marcados [CONTROLE] (cidades/florestas) caindo junto com Lua/Marte indicam que o cluster é grosseiro demais para aquele k.

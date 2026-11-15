# Proposta de alvos planetários — V1.4 (aguardando aprovação)

Rascunho em `outputs/v1_4/alvos_rascunho.csv`. Nada foi baixado além de cabeçalhos de GeoTIFF
(leitura remota de metadados) e consultas STAC. Só depois da aprovação o arquivo vira `entrada/alvos.csv`.

## Lua — fonte proposta: um único mosaico LOLA de 20 m
- **Arquivo:** `LDEM_80S_20MPP_ADJ.TIF` (PGDA produto 90, Barker et al. 2023), 80°–90°S,
  30400×30400 px, 20 m/px, estereográfica polar sul, Moon 2015 esfera.
  URL: https://pgda.gsfc.nasa.gov/data/LOLA_20mpp/LDEM_80S_20MPP_ADJ.TIF
- **Acesso:** sem login. O arquivo tem 2,7 GB, **mas é COG**: leio só as janelas de 27 km por HTTP
  (alguns MB por alvo), sem baixar o arquivo inteiro.
- **Por que não os DEMs de 5 m por local (PGDA produto 78):** quase todos têm 16–21 km de lado; só Haworth
  (29,8 km) comporta 3×3 recortes de 9 km. Com o mosaico de 20 m todos os alvos têm a grade 3×3 completa,
  com a mesma fonte e o mesmo processamento. A resolução nativa (20 m) é melhor que a grade de análise (40 m).
- **Centros:** a NASA não publica coordenadas das 9 regiões Artemis III (comunicado de out/2024 e resumo
  LPSC 2026 só trazem nomes e mapa). Uso o centro dos DEMs de 5 m do PGDA com o mesmo nome, medido
  do cabeçalho de cada GeoTIFF. A correspondência é **por nome**, não oficial.

| proposta | alvo | centro (lat, lon) | observação |
|---|---|---|---|
| A | Haworth | −86,764, −22,78 | região Artemis III |
| A | Malapert Massif | −85,995, −0,24 | região Artemis III (PGDA Site23) |
| A | Mons Mouton Plateau | −85,427, 31,74 | PGDA Site20v2 «Leibnitz beta plateau»; Leibnitz Beta é o nome antigo de Mons Mouton |
| A | Nobile Rim 2 | −83,954, 58,82 | região Artemis III (PGDA DM2) |
| A | de Gerlache Rim | −88,683, −67,93 | PGDA Site11; não sei se é a «de Gerlache Rim 2» da NASA |
| A | Connecting Ridge | −89,463, −137,49 | alvo atual (Site01); estava nas 13 regiões de 2022, saiu da lista de 2024 |
| B | Nobile Rim 1 | −85,438, 37,37 | **13,6 km** de Mons Mouton Plateau: as janelas de 27 km se sobrepõem |

**Sem centro disponível (preciso de coordenadas suas, ou deixo de fora):** Peak near Cabeus B, Mons Mouton
(cume ≈ 84,6°S, 31,0°E segundo a Wikipédia; ~25 km do Plateau, então haveria sobreposição) e Slater Plain.
Outros pares próximos que evitei: Connecting Ridge × Shackleton Rim (11,2 km) e de Gerlache Site11 × SL2 (14,0 km).

## Marte — fonte proposta: DTMs CTX controlados da USGS (STAC)
- **Catálogo:** `https://stac.astrogeology.usgs.gov/api/`, coleção `mro_ctx_controlled_usgs_dtms`.
  DTMs de ~20 m, controlados ao MOLA, COG na AWS (`astrogeo-ard`), 7–19 MB cada, **sem login**.
- **Cobertura:** encontrei DTMs em todos os locais testados (Gale 20+, InSight 20+, Jezero 20+, Gusev 20+,
  Oxia 13, Meridiani 6, Utopia 1, Ares Vallis 1, Chryse/Viking 1 1).
- **Limitação importante:** cada DTM é uma faixa de ~31 km de largura × 45–75 km, com só 66–79% de pixels
  válidos (borda diagonal). **Um quadrado de 27×27 km raramente cabe inteiro num único DTM.**
- **Jezero** continua com o GeoTIFF atual (mosaico USGS de 89×101 km): a janela central de 27 km tem 100% de
  cobertura válida, então a grade 3×3 funciona.

| proposta | alvo | ponto (lat, lon) |
|---|---|---|
| A | Jezero (Perseverance) | 18,435, 77,790 (centro do GeoTIFF atual) |
| A | Gale (Curiosity) | −4,589, 137,442 |
| A | Elysium Planitia (InSight) | 4,502, 135,623 |
| A | Oxia Planum (ExoMars) | 18,20, −24,50 |
| A | Meridiani Planum (Opportunity) | −1,946, −5,527 |
| A | Gusev (Spirit) | −14,568, 175,473 |
| B | Utopia Planitia (Zhurong) | 25,066, 109,925 |
| B | Ares Vallis (Pathfinder) | 19,13, −33,22 |

Os pontos de pouso vêm do meu conhecimento prévio e servem só para buscar o DTM no STAC.
**Precisam ser confirmados** antes de entrarem em `entrada/alvos.csv`.

## Decisão de método para Marte (preciso da sua escolha)
1. **Recomendado — recortes válidos dentro de um único DTM:** para cada alvo, escolher entre os DTMs que
   contêm o ponto aquele que comporta mais recortes de 9 km 100% válidos, e usar até 9 recortes mais próximos
   do ponto (a grade não precisa ser 3×3 quadrada). Não mistura DTMs, então não cria degraus artificiais.
   `tile_id` continua `{site_id}_r{linha}c{coluna}` na grade alinhada ao DTM.
2. **Mosaico de vários DTMs** numa janela de 27 km (como o PGC na Terra). Grade 3×3 igual à da Terra, mas as
   costuras entre DTMs podem ter pequenos desníveis verticais que inflam declividade e rugosidade.

## Contagem prevista
Terra 43×9 = 387; Lua (só A) 6×9 = 54; Marte (só A) 6×≤9 ≤ 54. Total ≈ 495 linhas, dentro da faixa de
pré-treino do ZEUS (~100 a ~2500 linhas). Lua e Marte ficam com ~11% cada.

## Fontes
- PGDA produto 78 (DEMs 5 m por local): https://pgda.gsfc.nasa.gov/products/78
- PGDA produto 90 (mosaico 20 m): https://pgda.gsfc.nasa.gov/products/90
- NASA, 9 regiões Artemis III (out/2024): https://www.nasa.gov/news-release/nasa-provides-update-on-artemis-iii-moon-landing-regions/
- Resumo LPSC 2026 (George et al.): https://ntrs.nasa.gov/citations/20250011660
- Mons Mouton: https://en.wikipedia.org/wiki/Mons_Mouton e https://svs.gsfc.nasa.gov/5074
- STAC USGS (CTX DTMs): https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms

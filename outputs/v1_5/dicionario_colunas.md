# Dicionário de colunas — protocolo `v1_5`

Uma linha = um recorte de 9×9 km em grade de 40 m (225×225 px). `zeus_input.csv` e `tabela_completa.csv` têm as mesmas linhas na mesma ordem.

`zeus_input.csv` contém apenas: `median_slope_deg`, `p90_slope_deg`, `median_roughness_m`, `p90_roughness_m`, `robust_relief_p95_p5_m`, `frac_solo_exposto`, `frac_neve_gelo`, `frac_vegetacao`, `frac_construido`.

| coluna | definição | unidade | fonte |
|---|---|---|---|
| `tile_id` | Identificador único do recorte 9×9 km: `{site_id}_r{linha}c{coluna}` (linhas/colunas 1..3 na grade 3×3 de 27 km; o recorte central `r2c2` é o recorte de 9 km centrado no ponto do local). | — | gerado |
| `site_id` | Identificador do local (Terra: `earth_` + nome normalizado; alvos: id do alvo). | — | terra_por_local.csv / alvos |
| `site_name` | Nome legível do local. | — | terra_por_local.csv / alvos |
| `body` | Corpo celeste: EARTH, MOON ou MARS. | — | gerado |
| `tipo` | candidato (análogo candidato), controle (local comum, p.ex. cidade/floresta, para checar falsos análogos) ou alvo (local lunar/marciano de referência). `analogo` do CSV original foi mapeado para `candidato`. | — | terra_por_local.csv |
| `lat` | Latitude do centro do recorte. Terra: WGS84. Lua/Marte: planetocêntrica no CRS geodésico do próprio corpo (esfera de referência do GeoTIFF), calculada do centro do recorte. | graus | calculado |
| `lon` | Longitude do centro do recorte, positiva para leste, normalizada para -180..180. Mesma regra de CRS de `lat`. | graus | calculado |
| `source_dataset` | Produto DEM de origem. | — | metadados do processamento |
| `native_res_m` | Resolução nativa do DEM de origem (antes do regradeamento para 40 m). | m | metadados do raster |
| `valid_coverage_pct` | Porcentagem de pixels com elevação válida no recorte (mínimo aceito 99,9%). | % | calculado |
| `nodata_pixels` | Número de pixels sem dado no recorte de 225×225. | pixels | calculado |
| `protocol` | Versão do protocolo de cálculo (`v1_3_1` ou `v1_4`). Valores de versões diferentes não são comparáveis numericamente. | — | gerado |
| `median_slope_deg` | Mediana da declividade (np.gradient sobre DEM suavizado com gaussiano σ=1 px, grade 40 m). | graus | calculado do DEM |
| `p90_slope_deg` | Percentil 90 da declividade. | graus | calculado do DEM |
| `median_roughness_m` | Mediana da rugosidade. V1.3.1: DP local 5×5 do DEM suavizado (inclui a rampa/tendência). V1.4: DP local 5×5 do resíduo gauss(σ=1) − gauss(σ=5) (sem tendência). | m | calculado do DEM |
| `p90_roughness_m` | Percentil 90 da rugosidade (mesma definição de `median_roughness_m`). | m | calculado do DEM |
| `robust_relief_p95_p5_m` | Relevo robusto: percentil 95 − percentil 5 das elevações válidas originais. | m | calculado do DEM |
| `mean_slope_deg` | Média da declividade. | graus | calculado do DEM |
| `roughness_m` | Média da rugosidade (mesma definição de `median_roughness_m` na versão do protocolo). | m | calculado do DEM |
| `relative_relief_m` | Relevo relativo: elevação máxima − mínima (sensível a outliers). | m | calculado do DEM |
| `roughness_legacy_mean_m` | Média da rugosidade antiga (V1.3.1, com tendência). Em `v1_3_1` é igual a `roughness_m`. | m | calculado do DEM |
| `roughness_legacy_median_m` | Mediana da rugosidade antiga (com tendência). | m | calculado do DEM |
| `roughness_legacy_p90_m` | Percentil 90 da rugosidade antiga (com tendência). | m | calculado do DEM |
| `frac_solo_exposto` | Fração do recorte em solo exposto/vegetação esparsa (WorldCover classe 60). Lua e Marte: 1 (atribuído). | fração 0–1 | ESA WorldCover 10 m v200 (2021) |
| `frac_neve_gelo` | Fração em neve e gelo permanentes (classe 70). Lua/Marte: 0 (atribuído; gelo em crateras polares sombreadas não é cobertura visível). | fração 0–1 | ESA WorldCover |
| `frac_vegetacao` | Soma das classes de vegetação (10, 20, 30, 40, 90, 95, 100). Lua/Marte: 0. | fração 0–1 | ESA WorldCover |
| `frac_construido` | Fração construída/urbana (classe 50). Lua/Marte: 0. | fração 0–1 | ESA WorldCover |
| `frac_arvore … frac_musgo_liquen` | Fração de cada uma das 11 classes WorldCover (10 árvores, 20 arbustos, 30 campo, 40 agricultura, 50 construído, 60 solo exposto, 70 neve/gelo, 80 água, 90 área úmida, 95 mangue, 100 musgo/líquen). Somam 1 nos pixels com dado. | fração 0–1 | ESA WorldCover |
| `cover_source` | `worldcover` (medido), `atribuido_corpo_sem_vegetacao` (Lua/Marte) ou `atribuido_manto_de_gelo` (interior da Antártida, fora da cobertura do WorldCover). | — | gerado |

## Notas desta versão

- v1_5 = colunas de terreno idênticas à v1_4 + cobertura superficial. Os valores de terreno não mudaram.
- Cobertura (Terra): ESA WorldCover 2021 v200, 10 m, reprojetado por vizinho mais próximo para uma grade de 10 m alinhada à grade de análise; frações sobre os pixels com dado (exige ≥ 99,9% com dado).
- Lua e Marte: valores atribuídos (solo exposto = 1). Isso é um fato físico, não uma medição; a coluna `cover_source` diz qual é o caso.
- Antártida: fora do WorldCover. Dome C, Vostok e Dome Argus: neve/gelo = 1 atribuído. **Vales Secos de McMurdo ficam fora da v1_5** até haver um mapa de afloramentos rochosos (ver relatório).
- O ZEUS recebe 4 colunas de cobertura (solo exposto, neve/gelo, vegetação, construído); água e as 11 classes detalhadas ficam só na tabela completa.
- **Piso de ruído do NASADEM** (herdado da v1_4): superfícies planas NASADEM parecem mais inclinadas/rugosas do que são. Ver `outputs/v1_4/investigacao_lua/diagnostico.md`.

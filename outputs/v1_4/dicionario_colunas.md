# Dicionário de colunas — protocolo `v1_4`

Uma linha = um recorte de 9×9 km em grade de 40 m (225×225 px). `zeus_input.csv` e `tabela_completa.csv` têm as mesmas linhas na mesma ordem.

`zeus_input.csv` contém apenas: `median_slope_deg`, `p90_slope_deg`, `median_roughness_m`, `p90_roughness_m`, `robust_relief_p95_p5_m`.

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

## Notas desta versão

- **Rugosidade sem tendência**: `median_roughness_m`, `p90_roughness_m` e `roughness_m` usam o DP local 5×5 de gauss(σ=1 px) − gauss(σ=5 px ≈ 200 m). A versão antiga (com tendência) está em `roughness_legacy_*`.
- Grade: cada local terrestre e alvo lunar/Jezero tem uma janela de 27×27 km fatiada em 3×3 recortes de 9 km (`r1c1` = canto noroeste da grade no CRS de análise; `r2c2` = centro, idêntico ao recorte do V1.3.1). A janela é lida com margem de 24 px para que os filtros tenham contexto; essa margem é a única borda excluída.
- Marte (exceto Jezero): DTM CTX único da USGS (STAC), reprojetado para azimutal equidistante local; até 9 recortes de 9 km totalmente válidos, os mais próximos do ponto do alvo. `r1c1` = recorte mais ao noroeste entre os escolhidos; a grade pode não ser 3×3 completa.
- Lua: mosaico LOLA 20 m (PGDA, Barker et al. 2023), lido por janela (COG). Os centros das regiões vêm dos DEMs de 5 m do PGDA com o mesmo nome (correspondência por nome, não oficial).
- Lat/lon: centro de cada recorte pela transformação do raster; Terra em WGS84, Lua/Marte no CRS geodésico esférico do próprio corpo; longitude leste-positiva em -180..180.
- Valores `v1_4` não são comparáveis numericamente com `v1_3_1` para a rugosidade (definição mudou).
- **Piso de ruído do NASADEM**: em superfícies quase planas o NASADEM mostra ~0,5–0,9° de declividade e ~0,5–0,8 m de rugosidade só por ruído (Salar de Uyuni: 0,6° / 0,5 m; gelo REMA/ArcticDEM: 0,008 m). Recortes terrestres planos com `source_dataset` NASADEM parecem mais inclinados/rugosos do que são. Não corrigido (decisão do projeto); ver `outputs/v1_4/investigacao_lua/diagnostico.md`.
- Rugosidade lunar baixa (~1 m) foi checada contra DEMs LOLA 5 m e DTMs estéreo Kaguya: é consistente, não é artefato. Nobile Rim 2 tem resolução efetiva pior (~30 m).

# Metodologia — Space Analogs (NASA Space Apps 2026)

Este documento explica **o que o projeto faz, como e por quê**, na ordem em que os dados são produzidos.
Os detalhes de cada coluna estão em `outputs/v1_5/dicionario_colunas.md`; os números de qualidade, em
`outputs/v1_5/relatorio_qualidade.md`.

## Pergunta
Quais locais da Terra se parecem fisicamente com as regiões candidatas a base na Lua (polo sul, Artemis) e com
locais de interesse em Marte? Hoje a resposta usa **relevo**, **cobertura superficial**, **temperatura da
superfície** e **geologia** (classe litológica harmonizada).

## Visão geral do pipeline

```
DEMs ──► terreno v1_4 ──► + cobertura = v1_5 ──► + temperatura = v1_6 ──► + geologia = v1_7
      ──► ZEUS (embeddings + clusters) └─► similaridade (ranking) ──► site
```

Um comando refaz tudo a partir da cobertura: `python -m src.rodar_tudo` (use `--desde terreno` para refazer
também o relevo). Cada etapa grava em `outputs/` e registra falhas em `processing_status.csv`.

| etapa | módulo | saída |
|---|---|---|
| 1. Terreno | `src/v1_4.py` | `outputs/v1_4/` (484 recortes) |
| 2. Cobertura | `src/cobertura.py` | `outputs/v1_5/` (475 recortes) |
| 3. Temperatura | `src/temperatura.py` (terra, lua, marte, montar) | `outputs/v1_6/` (475 recortes) |
| 4. Geologia | `src/geologia.py` (terra, lua, marte, montar) | `outputs/v1_7/` (471 recortes) |
| 5. ZEUS | `src/zeus_pipeline.py` (usa `entrega_zeus/rodar_zeus.py`) | `outputs/v1_7/zeus/` |
| 6. Similaridade | `src/similaridade_sites.py` | `outputs/v1_7/similaridade/` |
| 7. Site | `src/exportar_site.py` | `outputs/site/dados_site.json`, `outputs/site/relevo/*.png` |

## 1. Unidade de análise: o recorte
- **Recorte** = quadrado de 9×9 km numa grade de 40 m (225×225 px). Uma linha das tabelas = um recorte.
- Cada **local** é representado por vários recortes: uma janela de 27×27 km fatiada em 3×3 (Terra, Lua, Jezero) ou
  até 9 recortes totalmente válidos dentro de um DTM (demais locais de Marte). Assim um local não depende de um
  único quadrado, e dá para ver a variação interna dele.
- **Por que 40 m:** é a menor grade comum sem "inventar" resolução. Os DEMs polares da Terra têm 32 m e o NASADEM
  ~30 m; Lua e Marte têm 20 m.

## 2. Fontes de elevação
| corpo | fonte | resolução | acesso |
|---|---|---|---|
| Terra 56°S–60°N | NASADEM (SRTM reprocessado) | ~30 m | Earthdata (login) |
| Terra polar | ArcticDEM / REMA mosaicos (PGC) | 32 m | STAC PGC, sem login (são modelos de superfície) |
| Lua (polo sul) | LOLA LDEM 80S 20 m/pix (PGDA, Barker et al. 2023) | 20 m | COG, sem login |
| Marte – Jezero | Mars 2020 CTX DEM (USGS) | 20 m | arquivo local |
| Marte – outros | DTMs CTX controlados (USGS STAC) | ~20 m | COG, sem login |

**Alvos** (`entrada/alvos.csv`, aprovados pelo usuário): Lua = Haworth, Malapert Massif, Mons Mouton Plateau,
Nobile Rim 2, de Gerlache Rim, Connecting Ridge; Marte = Jezero, Gale, InSight, Oxia Planum, Meridiani, Gusev.

## 3. Features de relevo (v1_4)
1. **Suavização** gaussiana σ = 1 px, para reduzir ruído pixel a pixel.
2. **Declividade** = ângulo do gradiente (`np.gradient`) do DEM suavizado. Usamos a mediana e o percentil 90.
3. **Rugosidade sem tendência** = desvio-padrão local (janela 5×5) do resíduo `gauss(σ=1) − gauss(σ=5)`.
   Remover a superfície regional (~200 m) impede que uma encosta lisa conte como "rugosa". A versão antiga
   (com tendência, quase igual à declividade, r = 0,998) continua em `roughness_legacy_*`.
4. **Relevo robusto** = percentil 95 − percentil 5 da elevação no recorte.
5. **Bordas e lacunas:** a janela é lida com 24 px de margem, para os filtros terem contexto real. Pixels a até
   7/23 px de uma lacuna são excluídos. Recorte com menos de 99,9% de dados válidos é descartado.

## 4. Cobertura superficial (v1_5)
- **Terra:** ESA WorldCover 2021 (10 m, 11 classes) contado em cada recorte (4×4 subpixels por pixel de 40 m).
  O ZEUS recebe 4 frações: solo exposto, neve/gelo, vegetação e área construída.
- **Lua e Marte:** solo exposto = 1, o resto 0. É um **valor atribuído** (fato físico), não uma medição;
  `cover_source` diz isso.
- **Antártida:** fora do WorldCover. Usamos o mapa de afloramentos rochosos *Ice-free Antarctica* (Toth &
  Terauds 2023, AADC, 100 m, CC BY 4.0): fração de rocha → solo exposto; o resto → gelo. Qualquer valor > 0 do
  raster conta como rocha (é a união de duas camadas; o significado de 1/2/3 não é documentado), e o produto
  não separa gelo de mar. Resultado: McMurdo 25–86% de rocha por recorte; os domos (Dome C, Vostok, Argus) 0%,
  o que confirma por medição o que antes era atribuído.
- **Por que isso importa:** sem a cobertura, cidades planas (Londres, Nova York) caíam no mesmo grupo de Marte.
  Com ela, os controles vão para o fim do ranking (posições 30–38 de 42).

## 4b. Temperatura da superfície (v1_6)
Sempre temperatura **da superfície** (não do ar), em K, porque é o que existe para Lua e Marte.

| corpo | fonte | escala | o que se calcula |
|---|---|---|---|
| Terra | NASA POWER, climatologia da temperatura de pele (TS) da reanálise MERRA-2 (~0,5°×0,625°), API sem login | por local | média anual (TS), máxima (TS_MAX) |
| Lua | LRO Diviner Polar Resource Product (PDS, 605 MB): média e máxima anuais de modelo térmico ajustado ao 1º ano de observações (Paige et al. 2010), malha de ~0,5 km | **por recorte** | média dos triângulos dentro do recorte |
| Marte | NASA Ames Legacy Mars GCM (Haberle et al. 2019), `tsurf` 5°×6°, 16 horários/sol; 4 trechos de 10 sóis em Ls 0/90/180/270 (~1,2 GB) | por local | média das 4 estações; maior valor |

- Features no ZEUS: `t_sup_media_K` e `t_sup_max_K` — as únicas disponíveis nos três corpos (o Diviner PRP não
  tem mínima). Mínima e amplitude diária de Terra e Marte ficam em `outputs/v1_6/temperatura/`.
- **Cuidado:** são três tipos de produto (reanálise, modelo ajustado a observação, modelo climático). Servem para
  comparar ordem de grandeza (Lua 107–140 K de média, Marte ~223 K, Antártida ~217 K, desertos ~300 K), não
  diferenças de poucos kelvin. Marte com 4 estações subestima um pouco a máxima anual.
- Fontes descartadas: Diviner PCP (ideal, mas 30,7 GB), MGCM FV3 (arquivos de 4–45 GB, servidor sem leitura
  parcial), Mars Climate Database (exige cadastro).
- Efeito: nenhum local da Terra é termicamente parecido com o polo sul lunar, e o ZEUS passa a isolar a Lua;
  para Marte sobem os desertos frios e altos (Askja, Changtang, Chajnantor). Na Antártida, os domos de gelo são os
  mais parecidos termicamente com Marte, mas ficam longe pela cobertura (gelo). Os Vales Secos de McMurdo (frio
  + rocha exposta) são o 1º lugar para a Lua.

## 4c. Geologia (v1_7)
Classe litológica **harmonizada** no centro de cada recorte, traduzida de mapas geológicos regionais para um
vocabulário comum: `vulcanica`, `cristalina` (intrusiva/metamórfica), `sedimentar`, `evaporitica`, `gelo`,
`impacto_terras_altas`. Entra no ZEUS como one-hot (`lito_*`). É uma **interpretação** com regras explícitas em
`src/geologia.py`, não uma medida.

| corpo | fonte | regra |
|---|---|---|
| Terra | Macrostrat API (mapas compilados, CC-BY 4.0), escala mais detalhada disponível (large→tiny) | palavras-chave no nome/litologia da unidade (ex.: basalt→vulcanica; granite, gneiss→cristalina; evaporite→evaporitica) |
| Lua | USGS Unified Geologic Map of the Moon 1:5M (raster 64 px/grau) | unidades de cratera e bacia → `impacto_terras_altas` |
| Marte | USGS Geologic Map of Mars 1:20M (SIM 3292), shapefile + Descrição das Unidades (DMU) | **interpretação oficial da DMU**: o primeiro material citado define a classe (ex.: eHt → sedimentar; HNt → impacto; eHv → vulcânica); unidades fora da tabela usam o grupo do nome |

- Marte por local: Gusev vulcânica; Gale, InSight e Meridiani sedimentar (Gale com parte de impacto); Jezero e
  Oxia impacto/terras altas (unidades mistas; a classe única simplifica).
- Fora da v1_7: 4 recortes de Singapura (Macrostrat sem unidade, provavelmente mar).
- Efeito: Gusev tem análogos vulcânicos (Askja, Chajnantor, Lanzarote); Meridiani (sulfatos) tem Haughton,
  Changtang e a bacia salina de Qaidam. Para a Lua e as terras altas de Marte não há classe equivalente na Terra.

## 5. ZEUS (embeddings e clusters)
- [ZEUS](https://github.com/gmum/zeus) é um transformer pré-treinado (base TabPFN v1) que, sem treino novo
  ("zero-shot"), transforma uma tabela numérica em embeddings onde linhas parecidas ficam próximas.
- O que o código oficial faz e nós reproduzimos: padronização + MinMax(−1, 1), preenchimento com zeros até 30
  colunas, embedding de 512 dimensões, K-Means com 100 inicializações. **Nosso único acréscimo:** log1p antes,
  porque as features são magnitudes ≥ 0 muito assimétricas (relevo de 1 m a 3000 m).
- Rodamos k = 2…10, com 5 sementes por k (estabilidade ≈ 1,0). O **k sugerido** para exibição é o de maior
  silhueta entre 3 e 8 (hoje k = 6, na v1_7). O ZEUS recebe todas as colunas sem pesos (modelo pré-treinado);
  os pesos por grupo valem só para o score de similaridade. O ZEUS foi pré-treinado com conjuntos de ~100 a ~2500 linhas, e temos 475.
- Checkpoint: `cache/zeus_ckpt/zeus.pt` (305 MB, Google Drive do README do ZEUS). Roda em CPU em ~1,5 min.

## 5b. Camada de clima de Marte (contribuição de Luís G. O. Miranda; `src/clima_marte.py`)
- **O que é:** terceira opinião, ao lado do ZEUS, **fora do score**. Compara o clima de cada local da Terra com o do
  modelo climático global de Marte da NASA Ames (Beta Output Release 1, FV3, células de 2°, doi 10.25966/rjgg-r639).
  Terra: 1 ano de dados diários da API Meteomatics (conta do hackathon), para os nossos 43 locais e uma grade de 5°
  em terra firme (507 pontos ao todo).
- **Grandezas (9):** temperatura média do ar e da superfície; variação sazonal (máx − mín da média móvel de 5 dias /
  médias de 5 sóis) do ar e da superfície; amplitude diária do ar e da superfície; pressão (log10); precipitação
  (log(1+x); 0 em Marte); poeira (Terra: profundidade óptica **só de poeira mineral**, `dust_aod_550nm`; Marte:
  `taudust_VIS`).
- **Métrica:** similaridade de Gower, `s_k = 1 − |x − y| / R_k` (R_k = amplitude no conjunto Terra + Marte), média
  ponderada com peso 0,5 nas seis térmicas (cada dimensão física conta uma vez) — a configuração "pesos corrigidos"
  do relatório original. Para cada alvo de Marte usamos a célula do modelo mais próxima do centro do alvo.
- **Mudanças em relação ao original:** (1) poeira mineral em vez da AOD total (que inclui poluição; correção
  recomendada pelo próprio autor); (2) os nossos 6 alvos em vez de 3 sítios fixos.
- **Teste:** com AOD total, a nossa reimplementação reproduz os valores do original para Jezero, Gale e Elysium
  (diferença máxima 1×10⁻⁷).
- **Resultado:** separa análogos de controles (AUC 0,98–0,995) e tem correlação ≈ 0 com o nosso score (Spearman
  −0,05 a 0,08): é outra dimensão. Mais parecidos em clima: Dome Argus, Tanezrouft (Saara), Denali, Vostok, Rub al
  Khali — os mesmos para os seis alvos. Askja, nº 1 do nosso ranking para Marte, é o último em clima.
- **Por que fora do score:** escala diferente (região de ~120 km × quadrado de 9 km), Terra com 1 ano só, e o clima
  quase não distingue um alvo de Marte de outro.
- Saídas: `outputs/v1_7/clima/clima_marte_por_alvo.csv` e `clima_marte_resumo.json`. Entradas copiadas dos zips do
  autor para `cache/clima_luis/` (`python -m src.clima_marte --extrair`).

## 6. Similaridade (ranking)
Para cada alvo (e para cada corpo, juntando os alvos):
1. **Peso igual por grupo** (relevo, cobertura, temperatura, geologia), para o número de colunas de um grupo não
   decidir a importância dele. Grupos numéricos: log1p → z-score → RMS das diferenças padronizadas (em
   "desvios-padrão"). Geologia: diferença direta das classes, sem z-score (classes raras não pesam mais):
   0 = mesma classe, 0,5 = uma indefinida, 1 = diferentes.
2. Distância entre recortes = √(média dos quadrados das distâncias dos grupos). Cada par também guarda a
   distância de cada grupo (`dist_terreno`, `dist_cobertura`, `dist_temperatura`, `dist_geologia`), que o site
   usa para explicar *em que* um local se parece com o alvo. Um ranking alternativo com peso igual por coluna é
   recalculado a cada execução (`ranking_por_corpo_peso_por_coluna.csv`) só para o teste de robustez.
3. **Distância alvo→local** = para cada recorte do alvo, o recorte mais parecido do local; depois a mediana. Um
   local é bom análogo se tem algum terreno parecido com cada parte do alvo.
4. **Score 0–100** = `100 / (1 + d / d50)`, com d50 = mediana de todas as distâncias alvo→local (1,29 na v1_7 com pesos por grupo). 50 = par
   típico; 100 = idêntico. É uma escala de leitura relativa a este conjunto de locais, não uma probabilidade.
5. **Medidas complementares:** distância no embedding ZEUS e fração dos recortes do alvo que caem num cluster que
   contém o local (`cocluster`). **Explicação por feature:** diferença padronizada de cada feature no par de
   recortes mais parecido (`contribuicoes.csv`), para o site mostrar *por que* dois locais são parecidos.
6. **Controle de qualidade embutido:** cidades e floresta entram no ranking de propósito. Se subirem, as features
   não estão discriminando.

Resultado atual (v1_7, pesos por grupo), em `outputs/v1_7/similaridade/resumo.md`. Mais parecidos com Marte:
Askja, Ilha Devon-Haughton, Changtang, Qaidam, Atacama-Chajnantor, Mauna Loa (HI-SEAS), Atacama-Yungay,
Lanzarote, Utah-MDRS, Danakil. Gusev (basáltico): Askja, Chajnantor, Lanzarote. Lua: scores ~50 (1º: Vales Secos de McMurdo); o que afasta todos os locais da
Terra é a temperatura (2,1–2,7 desvios). Askja aparece no topo de quase todos os alvos por ser intermediário
em tudo (basalto, frio, solo exposto, relevo moderado).

## 7. Validações e o que foi verificado
- Esquema, ausência de NaN, unicidade de `tile_id`, limites de lat/lon: automáticos em cada etapa.
- V1.3.1 reproduzida exatamente a partir do notebook original (12 recortes recalculados dos DEMs brutos).
- Recorte central `r2c2` da V1.4 × V1.3.1: mesmo DEM e mesmo relevo; diferenças pequenas por tratamento de borda.
- Rugosidade lunar: verificada contra DEMs LOLA 5 m e DTMs estéreo Kaguya (`outputs/v1_4/investigacao_lua/`).

## 7b. Validação (`python -m src.validacao`, saída em `outputs/v1_7/validacao/`)
| teste | resultado | leitura |
|---|---|---|
| candidatos × controles (AUC) | Lua 0,90 (p = 0,001); Marte 0,76 (p = 0,03) | as features separam análogos de cidades/floresta |
| lista publicada (Catálogo ESA/CAFE + PTAL) | Lua: AUC 0,85 (p = 0,001, n = 9), top 4 no catálogo; Marte: AUC 0,65 (p = 0,07, n = 13) | concorda com a literatura em análogos de terreno; os de Marte mal colocados (Pilbara, Rio Tinto, Teide, Namib) são análogos mineralógicos, astrobiológicos ou eólicos |
| robustez a pesos (Spearman) | Lua 0,91; Marte 0,90; top 10: 10/10 e 8/10 | a conclusão não depende do esquema de pesos |
| score × distância ZEUS (Spearman) | Lua 0,18; Marte 0,25 | ZEUS é visão complementar, não confirmação |

Locais usados na prática como análogos aparecem bem colocados: Ilha Devon/Haughton (2º Marte e Lua),
Mauna Loa/HI-SEAS (6º Marte e Lua), Utah/MDRS (9º Marte). **Viés de seleção:** a lista de locais já é feita de
análogos conhecidos; ver docs/LIMITACOES.md (A). Reprodutibilidade: refazer o pipeline do zero reproduz exatamente os
valores de todos os recortes (diferença 0,0), exceto as mudanças intencionais de centro de Jezero e Oxia.

## 8. Limitações conhecidas
- **Piso de ruído do NASADEM:** superfícies planas parecem ter ~0,6° e ~0,5 m de rugosidade (Salar de Uyuni).
  Documentado, não corrigido (decisão do projeto).
- Lista completa e comentada: [docs/LIMITACOES.md](docs/LIMITACOES.md).
- Centros lunares: DEMs PGDA de mesmo nome das regiões Artemis (correspondência não oficial). Marte: pontos de
  pouso conferidos (Planetary Society/artigos das missões); Jezero no Octavia E. Butler Landing; Oxia no centro IAU.
- Meridiani tem 1 recorte; Gusev, 8; Denali, 7. 4 recortes de Singapura ficam fora da v1_7 (sem geologia).
- Nobile Rim 2 tem resolução efetiva pior (~30 m).
- Geologia: interpretação de mapas regionais no centro do recorte; Marte só tem classe comparável com a Terra
  em Gusev (vulcânica); Lua e terras altas de Marte (impacto) não têm classe equivalente na Terra.

## 9. Esquema do JSON do site (`outputs/site/dados_site.json`)
```
meta:        protocolo, features[{coluna,nome,unidade,grupo}], k_disponiveis, k_sugerido, qualidade_k[],
             score (texto), contribuicao (texto), coordenadas (texto), fontes[{nome,uso,url,credito?}], avisos[]
locais[]:    site_id, nome, corpo (EARTH|MOON|MARS), tipo (candidato|controle|alvo), lat, lon (média dos recortes),
             n_recortes, fonte_dem, fonte_cobertura, media{feature}, desvio{feature}, imagem_relevo
recortes[]:  tile_id, site_id, lat, lon, features{...}, clusters{k2..k10}
similaridade:
  por_corpo{MOON|MARS: [ {site_id, posicao, score, dist_features, dist_zeus, cocluster{k}, recorte_alvo, recorte_terra} ]}
  por_alvo{alvo_id: [ ...mesmo formato... ]}
  contribuicoes{alvo_id: {site_id: {feature: diferença padronizada}}}
clima_marte: fonte, metodo, aerossol_terra, grandezas[{id,nome,unidade,peso}], avisos[],
  por_alvo{mars_*: {marte{grandeza}, celula[lat,lon_leste], validacao{...},
                    locais{site_id: {sim (0-100), pos_global, grandezas{s_k 0-100}, terra{valor físico}}}},
           MARS: {locais{site_id: {sim = média dos 6 alvos}}}}
```
Imagens: `outputs/site/relevo/{site_id}.png` (relevo sombreado da janela, recortes válidos contornados em
amarelo; fundo transparente onde não há dado).

## 10. Créditos
NASADEM (NASA/USGS LP DAAC); ArcticDEM e REMA (Polar Geospatial Center; usar o texto de citação oficial do PGC);
LOLA (NASA GSFC PGDA, Barker et al. 2023, doi:10.60903/gsfcpgda-lola-spole); DTMs CTX e Mars 2020 CTX DEM (USGS
Astrogeology); Macrostrat (CC-BY 4.0); USGS Unified Geologic Map of the Moon (Fortezzo et al. 2020, CC0); USGS Geologic
Map of Mars SIM 3292 (Tanaka et al. 2014); NASA POWER (MERRA-2); LRO Diviner PRP (UCLA/NASA, Paige et al. 2010); NASA Ames Legacy Mars GCM
(Haberle et al. 2019); ESA WorldCover ("© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021)
processed by ESA WorldCover consortium", CC BY 4.0); ZEUS (GMUM, Apache-2.0, baseado no TabPFN v1).

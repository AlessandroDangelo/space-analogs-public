# Diagnóstico: a rugosidade lunar da V1.4 (~1 m) é artefato do DEM?

**Conclusão: não.** Três verificações independentes dão a mesma rugosidade baixa nas encostas lunares.
O problema de comparabilidade mais sério está do lado da Terra: o **piso de ruído do NASADEM**.

Reproduzir: `python -m src.investigar_lua` (itens 1–2) e `python -m src.investigar_lua kaguya` (item 3).

## 1. Resolução efetiva do mosaico LOLA 20 m (`comparacao_lua.csv`)
Mapa `LDEM_80S_20MPP_ADJ_EFFRES.TIF` (PGDA) regradeado nos 54 recortes:
- Mediana por recorte entre 13 e 20 m em Haworth, Malapert, Mons Mouton Plateau, de Gerlache e Connecting Ridge.
  Menos de 6% dos pixels acima de 40 m. Ou seja, nesses locais o DEM resolve detalhes **mais finos que a grade
  de análise (40 m)**.
- **Exceção: Nobile Rim 2**, com mediana de 29–33 m e 25–37% dos pixels acima de 40 m. Ali a rugosidade pode
  estar parcialmente suavizada.

## 2. Mosaico 20 m × DEMs LOLA 5 m por local (`resumo_5m_vs_20m.csv`)
Mesma grade de 40 m e mesmo cálculo, nos 14 recortes cobertos pelos DEMs 5 m (todos os 9 de Haworth + o central
dos outros 5 alvos): razão de 0,998 a 1,000 em todas as features. O mosaico não suaviza além do DEM de 5 m.
(As duas fontes vêm do mesmo laser, por isso o item 3 é necessário.)

## 3. Fonte independente: DTMs estéreo Kaguya TC v2 (USGS STAC) (`resumo_kaguya_vs_lola.csv`)
Comparação pareada (mesmos pixels nas duas fontes), em 9 pares / 7 recortes / 3 locais (Haworth, Malapert,
Nobile Rim 2), com 54–64% de pixels pareados. Nenhum recorte tem cobertura Kaguya completa, por causa das sombras
polares.

| feature | LOLA 20 m | Kaguya | razão Kaguya/LOLA |
|---|---|---|---|
| declividade mediana | 16,6° | 16,5° | 0,997 |
| rugosidade mediana | 0,99 m | 0,77 m | 0,76 |
| rugosidade p90 | 2,10 m | 1,67 m | 0,78 |

O Kaguya (fotogrametria, ~30 m, sem relação com o LOLA) dá a mesma declividade e rugosidade **ainda menor**.
Limitações: amostra pequena, só encostas iluminadas, e o GSD do Kaguya (~27–33 m) é próximo da grade de 40 m.

## 4. Interpretação física
Razão rugosidade/declividade (mediana por local): Lua 0,07–0,11; Gale (Marte) 0,08; montanhas terrestres
0,26–0,38 (Teide, Kilimanjaro, Everest, Aconcagua). As encostas lunares são paredes de cratera lisas na escala
de 40–200 m, cobertas por regolito; as montanhas terrestres são dissecadas por rios e geleiras nessa escala.
Por isso os recortes lunares formam um grupo próprio no ZEUS. **Isso parece ser um resultado, não um defeito.**

## 5. Problema real encontrado: piso de ruído do NASADEM (Terra)
| local | fonte | declividade mediana | rugosidade mediana |
|---|---|---|---|
| Dome C, Summit, Vostok (gelo plano) | REMA/ArcticDEM | 0,02–0,09° | 0,005–0,008 m |
| Salar de Uyuni (uma das superfícies mais planas da Terra) | NASADEM | 0,61° | 0,51 m |
| Gobi, Lut, Danakil, Tanezrouft | NASADEM | 0,75–0,91° | 0,53–0,77 m |

O ruído do SRTM/NASADEM (alguns metros) produz cerca de 0,5–0,8° de declividade e 0,5 m de rugosidade mesmo em
superfícies quase perfeitamente planas. Consequências:
- Locais planos NASADEM parecem **mais inclinados e rugosos** do que são. Ficam artificialmente próximos de
  Jezero/InSight/Oxia (CTX: 0,5–0,8 m), cujo nível de ruído próprio também não está quantificado.
- REMA/ArcticDEM (gelo) ficam num extremo de suavidade que os outros DEMs não conseguem medir.
- Afeta sobretudo o extremo plano. Em terreno montanhoso o sinal domina o ruído.

## Opções (decisão do usuário)
1. **Manter como está e documentar** (já está no relatório). É o mais simples para entregar hoje.
2. **Subtrair um piso de ruído por fonte, em quadratura** (`sqrt(max(r² − r0², 0))`), com r0 estimado em
   superfícies planas conhecidas de cada fonte (p. ex. Uyuni para NASADEM). Só melhora a rugosidade; a declividade
   continua com viés. Exige escolher as superfícies de referência para cada fonte (NASADEM, ArcticDEM/REMA, CTX, LOLA).
3. **Sinalizar recortes "abaixo do piso de ruído"** com uma coluna nova na tabela completa (não no zeus_input),
   para o site/colega interpretarem com cuidado.
4. **Marcar Nobile Rim 2 como resolução efetiva limitada** (opcional: trocar por outro alvo).

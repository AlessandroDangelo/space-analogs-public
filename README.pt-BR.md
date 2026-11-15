# Space Analogs — análogos terrestres para bases na Lua e em Marte

NASA Space Apps Challenge 2026, desafio *Identify Earth Locations that Analog the Permanent Moon Base Locations
and Mars*.

O projeto mede, com dados públicos da NASA, ESA e USGS, como é o terreno de 42 locais da Terra e de 12 locais
de interesse na Lua (regiões candidatas do programa Artemis no polo sul) e em Marte (locais de pouso), e
responde: **quais lugares da Terra mais se parecem com cada alvo, e em quê?**

## Resultado em uma frase
Para **Marte**, os locais mais parecidos são Askja (Islândia), Ilha Devon/Haughton, o planalto tibetano de
Changtang, a bacia de Qaidam, o Atacama, Mauna Loa/HI-SEAS e Utah/MDRS. Para a **Lua**, nenhum local da Terra chega
perto (scores ~50), sobretudo por causa da temperatura do polo sul lunar (média de 107–140 K); os menos diferentes
são os Vales Secos de McMurdo (Antártida), Askja, Haughton e Svalbard. A lição é que a Lua exige **combinar análogos por propósito**.

**Validação:** os quatro primeiros para a Lua e os dois primeiros para Marte estão no Catálogo de Análogos
Planetários da ESA (Lua: AUC 0,85, p = 0,001). O método separa análogos de lugares comuns (AUC 0,90 Lua, 0,76 Marte)
e é robusto à escolha de pesos (Spearman 0,90–0,91). Ele encontra **análogos de terreno e ambiente**, não de
composição mineral, e ordena uma lista de locais escolhida pela equipe (há viés de seleção; ver limitações).

## O que comparamos e por quê
| grupo | características | por que importa para uma missão |
|---|---|---|
| relevo | declividade, rugosidade sem tendência, relevo | pouso, mobilidade de rovers e EVA, linha de visada, sombra |
| cobertura | solo exposto, gelo, vegetação, área construída | realismo da superfície (poeira, instrumentos), gelo como recurso |
| temperatura | média e máxima anual da superfície | projeto térmico de equipamentos, baterias, habitat, trajes |
| geologia | classe de rocha (vulcânica, sedimentar, evaporítica, cristalina, gelo, impacto) | ciência de campo, coleta de amostras, recursos (ISRU) |

Detalhes e tipos de missão por característica: [docs/FEATURES_E_MISSOES.md](docs/FEATURES_E_MISSOES.md).

## Como funciona (resumo)
1. **Recortes:** cada local vira até 9 quadrados de 9×9 km numa grade de 40 m.
2. **Features:** 5 de relevo, 4 de cobertura, 2 de temperatura e 6 de geologia por recorte (protocolo `v1_7`).
3. **ZEUS:** um modelo zero-shot para dados tabulares agrupa os recortes em clusters (k = 2…10).
4. **Similaridade:** score de 0 a 100 entre cada local da Terra e cada alvo, com peso igual por grupo e a
   distância de cada grupo para explicar o resultado.
5. **Validação:** candidatos × controles (cidades/floresta), lista publicada de análogos e robustez a pesos.

Metodologia completa: [METODOLOGIA.md](METODOLOGIA.md). Limitações: [docs/LIMITACOES.md](docs/LIMITACOES.md).

## Como rodar
Requisitos: Python 3.11, ~6 GB de disco para caches, login NASA Earthdata (só para baixar NASADEM).
```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
```
Login Earthdata (uma vez, no seu terminal):
```
.venv\Scripts\python.exe -c "import earthaccess; earthaccess.login(strategy='interactive', persist=True)"
```
Dados que precisam estar no lugar antes (ver `CLAUDE.md`): `cache/zeus_ckpt/zeus.pt` (checkpoint do ZEUS),
`external/zeus` (clone de https://github.com/gmum/zeus) e os caches de temperatura e geologia (baixados pelos
módulos ou manualmente, conforme METODOLOGIA.md).
```
.venv\Scripts\python.exe -m src.rodar_tudo --desde terreno     # pipeline completo
.venv\Scripts\python.exe -m src.validacao                      # testes de validação
```

**Clima (terceira opinião, só Marte):** a camada de clima de Luís G. O. Miranda (modelo da NASA Ames × 1 ano de
dados Meteomatics) aponta outros análogos — platô antártico (Dome Argus, Vostok), Saara e Rub al Khali — e quase não
se correlaciona com o nosso ranking (Spearman ≈ 0). Ex.: Askja é análogo de terreno e rocha, não de clima. Ela é
mostrada no site ao lado do ranking, sem entrar no score (METODOLOGIA.md §5b).

## Onde estão os resultados
| arquivo | conteúdo |
|---|---|
| `outputs/v1_7/tabela_completa.csv` | uma linha por recorte, todas as features e metadados |
| `outputs/v1_7/zeus_input.csv` | só as 17 features numéricas (entrada do ZEUS) |
| `outputs/v1_7/dicionario_colunas.md` | definição, unidade e fonte de cada coluna |
| `outputs/v1_7/relatorio_qualidade.md` | validações, contagens, estatísticas |
| `outputs/v1_7/zeus/` | clusters, qualidade por k, análise dos clusters |
| `outputs/v1_7/similaridade/` | rankings, contribuições por feature, resumo |
| `outputs/v1_7/validacao/` | testes de validação |
| `outputs/v1_7/clima/` | camada de clima de Marte (similaridade de Gower por alvo e local) |
| `outputs/site/dados_site.json` + `relevo/*.png` | dados prontos para o site interativo |
| `site/` | **o site interativo** (estático; ver `site/README.md`) |

## Estrutura do repositório
```
entrada/        dados de entrada (somente leitura): locais, alvos, GeoTIFFs, lista de análogos publicados
src/            código (um módulo por etapa; src/rodar_tudo.py orquestra)
outputs/        resultados por versão de protocolo (v1_3_1 … v1_7) e dados do site
entrega_zeus/   pacote autônomo para rodar o ZEUS sobre a tabela
docs/           por que cada característica, tipos de missão, limitações
cache/          downloads (fora do git)
```

## Fontes de dados e créditos
NASADEM (NASA/USGS LP DAAC); ArcticDEM e REMA (Polar Geospatial Center); LOLA (NASA GSFC PGDA, Barker et al.
2023); DTMs CTX e Mars 2020 CTX DEM (USGS Astrogeology); ESA WorldCover 2021 (© ESA WorldCover project / Contains
modified Copernicus Sentinel data, CC BY 4.0); NASA POWER (MERRA-2); LRO Diviner PRP (Paige et al. 2010); NASA
Ames Legacy Mars GCM (Haberle et al. 2019); Macrostrat (CC BY 4.0); USGS Unified Geologic Map of the Moon
(Fortezzo et al. 2020); USGS Geologic Map of Mars SIM 3292 (Tanaka et al. 2014); ZEUS (GMUM, Apache-2.0); camada de clima: NASA Ames Mars Climate Modeling Center Beta Output Release 1 (doi 10.25966/rjgg-r639) e Meteomatics Weather API (conta do hackathon), trabalho de Luís G. O. Miranda.

## Próximos passos
**Trabalhos futuros:**
1. Busca sistemática no planeta (recortes amostrados em toda a superfície), para reduzir o viés de seleção e
   descobrir análogos novos; controles aleatórios estratificados.
2. Alvos de Marte nas *Human Exploration Zones* da NASA (mais alinhados a base permanente).
3. Dados de composição (abundância de rochas, minerais) para buscar também análogos mineralógicos.
4. Remover o piso de ruído do NASADEM em terrenos planos.

## Site interativo
```
cd site
python -m http.server 8765
```
Abra http://localhost:8765. Detalhes, atualização dos dados e publicação (GitHub Pages) em [site/README.md](site/README.md).

# Limitações do trabalho

Este projeto é um **MVP de hackathon**. Os resultados indicam *quais locais da Terra merecem atenção* como
análogos; não certificam nenhum local para uma missão. Abaixo, tudo o que sabemos que limita os resultados,
agrupado por tipo. Cada item diz o efeito prático e se tem solução.

## A. O que o ranking é e o que não é
- **É similaridade física**, medida em 4 grupos (relevo, cobertura, temperatura, geologia). **Não é** avaliação
  de habitabilidade, logística, custo, acesso, segurança ou legislação, que pesam muito na escolha real de um
  análogo.
- **O score é relativo** a este conjunto de 42 locais terrestres e 12 alvos: mudar os locais muda os números.
  Score 50 = par típico deste conjunto; não é uma probabilidade.
- **Nenhum local terrestre reproduz a Lua.** As temperaturas do polo sul lunar (média de 107–140 K) não existem na
  Terra, e a geologia de impacto/terras altas também não. Para a Lua, o ranking aponta os locais "menos
  diferentes", e o uso realista é combinar análogos por propósito (ver `docs/FEATURES_E_MISSOES.md`).
- **Viés de seleção dos locais terrestres.** Os 43 locais vieram da lista da equipe (`entrada/terra_por_local.csv`):
  38 análogos conhecidos ou plausíveis e 5 controles (cidades e floresta). O critério de escolha não está
  documentado no projeto, e não foi uma amostra aleatória nem uma busca global. Consequências:
  - **o método ordena estes locais; não descobre análogos novos** no planeta;
  - **validação parcialmente circular:** como a lista já é feita de análogos famosos, é esperado que vários
    apareçam bem colocados; a validação mede a ordem *dentro* desta lista, não a capacidade de achar análogos;
  - **viés geográfico e de tipo:** muitos desertos, montanhas altas e regiões polares; poucos ambientes tropicais
    ou costeiros; alguns continentes pouco representados;
  - **só 5 controles**, todos urbanos ou de floresta: o teste candidatos × controles separa bem
    "natural e árido × urbano ou vegetado", mas não separa análogos de desertos comuns;
  - **um ponto por local**, escolhido pela equipe: a janela de 27 km em volta dele pode não representar a região.
  *Trabalho futuro:* busca sistemática no planeta (recortes de 9 km amostrados em toda a superfície terrestre,
  filtrados por solo exposto ou gelo), controles aleatórios estratificados e teste de sensibilidade à posição.

## B. Dados de elevação (relevo)
- **Piso de ruído do NASADEM:** em superfícies planas o NASADEM mostra ~0,5–0,9° de declividade e ~0,5 m de
  rugosidade só por ruído (Salar de Uyuni: 0,6° / 0,5 m; gelo do REMA/ArcticDEM: 0,008 m). Locais planos fora dos
  polos parecem mais inclinados e rugosos. *Documentado, não corrigido.*
- **Fontes diferentes por região:** NASADEM (radar, ~30 m) entre 56°S e 60°N; ArcticDEM/REMA (estéreo, 32 m) nos
  polos, que são modelos de **superfície** (incluem gelo e, em tese, vegetação/estruturas).
- **Mesma grade (40 m) não é mesma resolução efetiva.** O LOLA lunar é interpolado entre trilhas do laser
  (resolução efetiva 13–20 m na maioria dos alvos; ~30 m em Nobile Rim 2). A rugosidade lunar foi conferida com
  DEMs de 5 m e com DTMs estéreo Kaguya (`outputs/v1_4/investigacao_lua/`).
- **Marte:** DTMs CTX são faixas estreitas. Meridiani tem só 1 recorte válido, Gusev 8, Gale 9.

## C. Locais e alvos
- **Centros das regiões lunares:** a NASA não publica coordenadas das 9 regiões Artemis III; usamos o centro dos
  DEMs PGDA de mesmo nome. A correspondência é por nome, não oficial. Três regiões ficaram de fora por falta de
  coordenadas (Peak near Cabeus B, Mons Mouton, Slater Plain).
- **Marte:** pontos de pouso conferidos na lista da Planetary Society (artigos de cada missão); Perseverance pelo
  ponto Octavia E. Butler Landing; Oxia Planum pelo centro do nome IAU (o centro da elipse do ExoMars não foi
  encontrado em fonte acessível).
- **Alvos de Marte são locais de pouso de rovers**, não zonas propostas para base humana. As "Human Exploration
  Zones" da NASA seriam alvos mais alinhados ao tema de base permanente.
- **Antártida:** cobertura pelo mapa de afloramentos do AADC (100 m); ele não separa gelo de mar, e o
  significado dos valores 1/2/3 não é documentado (usamos > 0 = rocha).

## D. Cobertura superficial
- **Lua e Marte: valor atribuído** (100% solo exposto), não medido. A cobertura diferencia locais da Terra entre si
  (e tira as cidades do topo), mas não diferencia alvos lunares/marcianos entre si (rochas, dunas, poeira).
- **Antártida:** fora do WorldCover; medida pelo mapa de afloramentos do AADC (rocha × gelo).

## E. Temperatura
- **Fontes de natureza diferente:** reanálise (Terra, MERRA-2 via NASA POWER, ~0,5°), modelo térmico ajustado a
  observações (Lua, Diviner), modelo climático (Marte, NASA Ames, 5°×6°). Comparáveis em ordem de grandeza, não
  em poucos kelvin.
- **Escala:** um valor por local na Terra e em Marte (fonte regional); por recorte na Lua.
- **Só média e máxima:** a mínima e a amplitude diária não existem no produto lunar usado.
- **Marte com 4 estações** (10 sóis cada): a máxima anual pode estar levemente subestimada.

### E2. Camada de clima de Marte (fora do score)
- **Modelo, não medição:** Marte vem de um modelo climático (células de 2°, ~120 km; em crateras a célula é mais
  alta que o ponto de pouso). Não foi confrontado com as medições dos rovers.
- **Um ano só na Terra** (Meteomatics, até nov/2026), não climatologia; Marte é um ano simulado.
- **Pressão e ciclo diurno não se aproximam:** a menor pressão da Terra é ~31× a maior de Marte; a amplitude diária
  de Marte (~80 K na superfície) é quase o dobro da maior da Terra. Os valores indicam o "menos diferente".
- **Pouca discriminação entre alvos:** os mais parecidos são quase os mesmos para os seis alvos de Marte.
- **Gower** depende da faixa de valores do conjunto (507 pontos + 16.200 células). Em Marte, cada hora do ciclo
  diurno é média de 5 sóis (suaviza extremos) e a temperatura do ar é a da camada mais baixa do modelo, não a 2 m.
- **Grandezas ausentes:** vento, umidade e radiação não entram.
- **Licença Meteomatics:** conta cedida no hackathon; o site publica só médias anuais e similaridades derivadas.

## F. Geologia
- **É interpretação**, não medida: unidades de mapas regionais traduzidas para 6 classes por regras explícitas
  (`src/geologia.py`). Escala dos mapas: Terra ~1:5M ou melhor (Macrostrat), Lua 1:5M, Marte 1:20M.
- **Um ponto por recorte** (o centro); recortes com geologia mista podem estar simplificados.
- **Marte:** as unidades dos alvos foram classificadas pela coluna de interpretação da Descrição das Unidades
  (DMU) do SIM 3292, com a regra "primeiro material citado". Várias unidades são misturas (por exemplo, Jezero:
  brechas de impacto, sedimentos e vulcânicas); a classe única simplifica essa mistura.
- **Sem composição mineral:** EMIT, CRISM e dados espectrais lunares não foram usados (cobertura irregular,
  processamento pesado).
- **Lua e terras altas de Marte** não têm classe equivalente na Terra; para elas a geologia não diferencia os
  locais terrestres.

## G. Método
- **Pesos:** peso igual por grupo é uma escolha razoável, mas não única. O teste de robustez
  (`outputs/v1_7/validacao/`) mostra quanto o ranking muda com peso por coluna.
- **ZEUS:** modelo zero-shot pré-treinado em dados sintéticos; recebe todas as colunas sem pesos. Os clusters são
  estáveis entre sementes, mas a interpretação deles é nossa.
- **Tipo de análogo:** o método encontra análogos de **terreno e ambiente**. Análogos mineralógicos ou
  astrobiológicos (Rio Tinto, Tenerife, citados no PTAL) ficam baixo no ranking, porque composição mineral não é
  medida.
- **ZEUS × score:** a distância no embedding do ZEUS concorda pouco com o score de similaridade (Spearman
  0,19–0,49). O ranking oficial é o score (explicável por grupo); o ZEUS é uma visão complementar de
  agrupamento, não uma confirmação.
- **Validação externa:** feita com o Catálogo de Análogos Planetários da ESA (30 locais) e o PTAL. Só 13 dos
  nossos locais aparecem nessas listas (vários por região, não pelo ponto exato), e estar fora do catálogo não
  significa não ser análogo. Revisões mais recentes em periódicos não foram consultadas (acesso pago).

## H. O que não foi testado
- GPU/CUDA e ambiente conda (testado em `venv`, Python 3.11, Windows, CPU).
- Reprodução em outra máquina.

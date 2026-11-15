# Por que comparar estas características e para que tipo de missão cada uma serve

Um **análogo terrestre** é um lugar da Terra onde se pode ensaiar, antes, algo que será feito na Lua ou em Marte:
testar um rover, treinar astronautas, validar um instrumento, ensaiar a montagem de uma base. Um análogo nunca é
igual ao alvo em tudo; ele é bom **para um propósito**. Por isso o projeto mede características separadas, e o
site mostra em que grupo cada local se parece com o alvo (`dist_terreno`, `dist_cobertura`, `dist_temperatura`,
`dist_geologia`), em vez de dar só um número.

> As relações abaixo são o raciocínio de engenharia e ciência por trás de cada característica. Elas explicam o
> uso possível dos resultados; **não** são requisitos oficiais de nenhuma missão.

## 1. Declividade (`median_slope_deg`, `p90_slope_deg`)
**O que mede:** a inclinação do terreno numa escala de 40 m. A mediana descreve o terreno típico; o percentil 90
descreve as partes mais íngremes.
**Por que importa para uma base:** o módulo de pouso precisa de chão pouco inclinado para não tombar. Rovers e
astronautas a pé gastam mais energia e correm mais risco em encostas. Habitats, painéis solares e antenas precisam
de áreas niveladas.
**Missões que um análogo de declividade ajuda a planejar:**
- ensaios de pouso e de detecção de obstáculos (sensores de navegação de descida);
- testes de mobilidade de rovers e de travessias de astronautas (EVA) em encostas reais;
- ensaios de terraplenagem e de assentamento de estruturas.

## 2. Rugosidade sem tendência (`median_roughness_m`, `p90_roughness_m`)
**O que mede:** o quanto o terreno é irregular em pequena escala (dezenas a centenas de metros), **depois de
remover a inclinação regional**. Uma encosta lisa tem rugosidade baixa mesmo sendo íngreme.
**Por que importa:** blocos, cristas, sulcos e pequenas crateras são os obstáculos reais para rodas, pés e pernas
de pouso. Esse é o motivo de termos separado rugosidade de declividade (na versão antiga, as duas eram quase a
mesma coisa).
**Missões:**
- testes de suspensão e de navegação autônoma de rovers;
- validação de algoritmos de desvio de obstáculos e de mapeamento a laser (lidar);
- planejamento de rotas de EVA e de tempo de travessia.

## 3. Relevo (`robust_relief_p95_p5_m`)
**O que mede:** a diferença de altitude dentro do recorte de 9 km (entre os percentis 5 e 95).
**Por que importa:** o relevo define **linha de visada** (comunicação direta entre base, rover e antena) e
**sombreamento**. No polo sul da Lua isso é decisivo: um pequeno desnível muda quantas horas de Sol um painel
recebe e cria crateras permanentemente sombreadas, onde pode haver gelo.
**Missões:**
- testes de comunicação e de retransmissão entre módulos;
- ensaios de operação com iluminação rasante e sombras longas (câmeras, navegação visual);
- exploração de bordas de cratera e de declives, onde fica a geologia mais exposta.

## 4. Temperatura da superfície (`t_sup_media_K`, `t_sup_max_K`)
**O que mede:** a temperatura média e a máxima anual **da superfície** (não do ar).
**Por que importa:** é a temperatura que equipamentos, rodas, baterias, trajes e fundações do habitat sentem.
Frio extremo deixa materiais quebradiços, reduz a capacidade das baterias e exige aquecimento; grandes oscilações
causam fadiga térmica.
**Missões:**
- testes de resistência térmica de equipamentos, baterias e materiais;
- ensaios de operação no frio (manutenção com luvas, partida a frio, aquecimento de habitat);
- testes de sistemas que lidam com gelo e de criogenia.
**Leitura do resultado:** nenhum lugar da Terra chega às médias de 107–140 K do polo sul lunar. Para a Lua, os
análogos térmicos mais próximos são os domos da Antártida (~215 K), mas eles diferem em cobertura (gelo). Isso
mostra que **nenhum análogo único** reproduz a Lua: é preciso combinar locais (um para relevo, outro para frio).

## 5. Cobertura superficial (`frac_solo_exposto`, `frac_neve_gelo`, `frac_vegetacao`, `frac_construido`)
**O que mede:** a fração do recorte em solo/rocha exposta, gelo, vegetação e área construída (Terra:
ESA WorldCover). Na Lua e em Marte a superfície é toda exposta (valor atribuído).
**Por que importa:** um análogo útil precisa de superfície **exposta**, como a da Lua e de Marte: vegetação e
cidades mudam a poeira, a aderência das rodas, a resposta de instrumentos de sensoriamento e o risco de
contaminação biológica. A cobertura também funciona como **filtro de realismo**: é ela que tira as cidades
(controles) do topo do ranking.
**Missões:**
- testes de mitigação de poeira e de abrasão em mecanismos;
- calibração de instrumentos de sensoriamento remoto e de espectroscopia sobre rocha nua;
- em áreas de gelo: ensaios de perfuração e de extração de água (ISRU).

## 6. Geologia (`lito_*`, `lito_classe`)
**O que mede:** o tipo de rocha dominante no recorte, em 6 classes comuns aos três corpos (vulcânica, cristalina,
sedimentar, evaporítica, gelo, impacto/terras altas).
**Por que importa:** é o que um geólogo-astronauta vai estudar e o que uma base vai usar como recurso:
- **vulcânica (basalto):** parecida com as planícies de Marte (por exemplo, Gusev) e com os mares lunares;
  serve para treinar coleta de amostras e para testar a produção de materiais de construção a partir do regolito;
- **sedimentar e evaporítica:** registram água antiga, o principal alvo científico em Marte (Jezero, Gale) e
  candidatos a recursos (sulfatos, sais);
- **impacto/terras altas:** é a geologia do polo sul lunar (crateras e bacias); na Terra, crateras de impacto
  como Haughton são os análogos mais diretos.
**Missões:**
- treinamento de geologia de campo de astronautas (como foi feito na era Apollo em campos vulcânicos);
- simulação de coleta e seleção de amostras para retorno;
- testes de instrumentos de análise química e mineral (Raman, espectrômetros);
- ensaios de ISRU (oxigênio, água e materiais de construção a partir de rocha local);
- astrobiologia (ambientes extremos como o Atacama hiperárido e o Rio Tinto ácido).

## Como os achados se conectam com o uso real (coerência)
Comparamos o ranking com o **Catálogo de Análogos Planetários da ESA** (Preston, Grady & Barber 2012, projeto
CAFE), que lista 30 locais de campo e indica para quais feições da Lua e de Marte cada um serve:
- **Lua:** os quatro primeiros do nosso ranking (Vales Secos de McMurdo, Islândia/Askja, Ilha Devon/Haughton,
  Svalbard) estão no catálogo como análogos lunares. Os 9 locais do catálogo ficam, em média, muito acima dos
  demais (AUC 0,85; p = 0,001).
- **Marte:** os dois primeiros (Askja e Haughton) também estão no catálogo. Atacama (5º e 7º), Mauna Loa/HI-SEAS
  (6º) e Utah/MDRS (9º) aparecem bem. Já **Pilbara, Rio Tinto, Teide e Namib** ficam baixo (21º–33º): no catálogo
  eles estão por **astrobiologia, mineralogia (sulfatos, óxidos de ferro) ou dunas**, que o projeto não mede
  (AUC 0,66; p = 0,07).

Conclusão: o método encontra **análogos de terreno e ambiente** (onde testar pouso, mobilidade, operação no frio,
geologia de campo) e concorda com a literatura nesse tipo de análogo. Para análogos de química e mineralogia
seriam necessários dados de composição. Detalhes em `outputs/v1_7/validacao/validacao.md`.

**Atenção ao viés de seleção:** a lista de locais da Terra já é formada majoritariamente por análogos conhecidos,
então era esperado que vários aparecessem bem colocados. A validação mede a ordem dentro desta lista, não a
capacidade de descobrir análogos novos (ver `docs/LIMITACOES.md`, item A).

## Combinação por tipo de missão (como o site pode usar)
| tipo de missão | grupos que mais importam | como ler no site |
|---|---|---|
| teste de pouso / navegação | terreno (declividade, rugosidade, relevo) | ordenar por `dist_terreno` |
| mobilidade de rover e EVA | terreno + cobertura | `dist_terreno` e `dist_cobertura` baixos |
| resistência de equipamentos / operação no frio | temperatura | ordenar por `dist_temperatura` |
| geologia de campo e amostragem | geologia + terreno | mesma `lito_classe` e `dist_terreno` baixo |
| ISRU (gelo, água, materiais) | cobertura (gelo) + geologia + temperatura | `frac_neve_gelo`, classe e frio |
| habitat de longa duração | todos (score total) | score geral |

# Site — Earth Dev Defense · Análogos terrestres para a Lua e Marte

Site estático, **em inglês** (exigência do julgamento global), (HTML + CSS + JavaScript, sem build e sem servidor de aplicação), com a identidade visual do
NASA Space Apps Challenge (azul `#08103F`, branco `#FCFBFF`, vermelho `#D42804`, lima `#EAFE07` para detalhes).

## Seções
Cada seção começa com uma frase que diz o que se vê ali e termina com o resultado principal em destaque. O que não
cabe na tela principal fica em expansíveis ("Saiba mais", "Ver detalhes", "Ver todas").
1. **Abertura** — pergunta, resumo, números do projeto (com ícones) e imagens reais do polo sul da Lua e de Marte.
2. **Desafio** — o pedido da NASA em uma frase (enunciado completo no expansível), trio de relevos reais
   Terra × Lua × Marte e os 6 motivos para buscar análogos.
3. **Análise** (6 passos, com atalhos que acompanham a rolagem) — alvo, tipo de missão, ranking com pódio e empates
   agrupados, **globo 3D da Terra**, comparação lado a lado, segunda opinião do ZEUS e terceira, de clima (só Marte;
   trabalho de Luís G. O. Miranda, `src/clima_marte.py`).
4. **Metodologia** — fluxo das 7 etapas (fontes e resoluções no detalhe de cada uma), por que cada característica,
   validação (AUC), limitações (3 principais + "Ver todas") e fontes agrupadas por corpo.
5. **Equipe** — fotos, descrição e os 6 integrantes (dados de `data/equipe.json`).

## Ver no computador
O navegador não deixa uma página aberta como arquivo (`file://`) ler os JSON, então use um servidor local:
```
cd site
python -m http.server 8765
```
e abra http://localhost:8765. O globo 3D precisa de internet (só a biblioteca globe.gl vem de CDN; as texturas da
Terra estão em `assets/img/`) e de WebGL; sem isso, o restante do site funciona e o globo mostra um aviso.

## O que a equipe precisa completar
- **E-mail, Lattes e LinkedIn** de cada integrante: edite `data/equipe.json`. Campos vazios (`""`) ou `null`
  **não aparecem** para o público; não invente dados. Os nomes e a descrição vieram da página oficial da equipe.
- **Fotos individuais** opcionais em `assets/pessoas/` (sem foto aparecem as iniciais, no mesmo tamanho).
- **Logos:** `assets/logo-space-apps.png` (versão oficial para fundo escuro) e `assets/logo-equipe.jpg` (também usada
  como ícone da aba; o fundo preto se funde ao azul com `mix-blend-mode`).

## Atualizar os dados e os recursos visuais
Depois de rodar o pipeline (`python -m src.rodar_tudo` e `python -m src.validacao`):
```
python -m src.exportar_site     # dados_site.json + relevos (outputs/site/)
python -m src.publicar_site     # copia para site/data/ e gera as miniaturas quadradas (requer Pillow)
```
Só quando mudarem (não fazem parte do pipeline):
```
python -m src.imagens_site      # imagens NASA/JPL/USGS e texturas do globo -> site/assets/img/*.webp
python -m src.icones_site       # sprite de ícones Lucide -> site/assets/icones.svg
```
Ao mudar `style.css` ou `app.js`, aumente o `?v=` no `index.html` para os navegadores não usarem a versão antiga.

## Conferir que nenhum número mudou
`verificar_numeros.js` (não é carregado pelo site) gera uma impressão digital SHA-256 de todos os rankings, notas,
coclusters do ZEUS e da camada de clima, em todas as combinações de corpo × alvo × missão × controles. No console da
página: `await (0, eval)(await (await fetch('verificar_numeros.js')).text())`. Valor de referência (v1_7, antes e depois
do redesign de 2026-11-15): `1651eae9…` (versão antiga do script). Desde a tradução para inglês o script ignora textos e o valor de referência é `4f467eb7840d…` (mesmos números: 42.738 valores conferidos um a um contra a versão em português); também devolve a nota
de Atacama–Chajnantor × Marte (65), as 4 AUCs (0,85 / 0,65 / 0,89 / 0,76) e as contagens (43 / 12 / 480 / 17).

## Publicar
Qualquer hospedagem de arquivos estáticos serve. No GitHub Pages: envie o repositório e publique a pasta `site/`.

## Decisões de design e dados
- Tokens únicos em `style.css` (cores, espaços, raios, sombra, escala tipográfica, movimento): um estilo de card,
  botão, chip, expansível e título de seção. Ícones de um só conjunto (Lucide, traço 1,75).
- Cores dos dados validadas para daltonismo sobre o fundo azul: alvo `#3987e5` (círculo) × Terra `#D42804`
  (losango). O lima do evento fica só em detalhes de interface e marcadores.
- Empates no ranking são agrupados pela nota exibida (inteira); as notas e a ordem não mudam.
- As notas por grupo são relativas aos outros lugares da Terra; o rótulo de uma palavra e o detalhe (desvios-padrão)
  dão a leitura absoluta, e "Serve para" só aparece quando o grupo é parecido de fato.
- Imagens só reais e de uso livre (NASA/JPL/USGS, domínio público), baixadas para o projeto em WebP, com crédito na
  seção de fontes. Movimento curto e só de resposta (hover, pressão, transições), desligado com `prefers-reduced-motion`.
- Cada gráfico tem tabela equivalente; funciona por teclado e em 375, 768 e 1440 px sem rolagem horizontal.

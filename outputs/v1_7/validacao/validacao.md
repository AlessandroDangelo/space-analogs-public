# Validação do ranking — protocolo `v1_7`

## 1. Candidatos × controles

AUC = probabilidade de um candidato ter score maior que um controle (0,5 = acaso, 1 = perfeito).

| corpo | candidatos | controles | AUC | p (Mann-Whitney, unilateral) | posições dos controles |
|---|---|---|---|---|---|
| MOON | 38 | 5 | 0.895 | 0.0012 | [32, 34, 36, 40, 43] |
| MARS | 38 | 5 | 0.758 | 0.0325 | [26, 28, 31, 32, 42] |

## 2. Análogos publicados

Fonte: `entrada\analogos_publicados_v2.csv` (22 pares local×corpo). Cada linha cita a publicação.

- **MOON:** Vales Secos de McMurdo (1º de 38), Islandia - Askja (2º de 38), Ilha Devon - Haughton (3º de 38), Svalbard - Bockfjorden (4º de 38), Mauna Loa - HI-SEAS (7º de 38), Atacama - Chajnantor (8º de 38), Teide (12º de 38), Atacama - Yungay (13º de 38), Deserto de Simpson (33º de 38). AUC publicados × demais candidatos = 0.854 (p = 0.001, n = 9).
- **MARS:** Islandia - Askja (1º de 38), Ilha Devon - Haughton (2º de 38), Atacama - Chajnantor (5º de 38), Mauna Loa - HI-SEAS (6º de 38), Atacama - Yungay (7º de 38), Utah - MDRS (9º de 38), Vales Secos de McMurdo (16º de 38), Svalbard - Bockfjorden (20º de 38), Namibe (22º de 38), Deserto de Simpson (25º de 38), Teide (26º de 38), Pilbara (31º de 38), Rio Tinto (34º de 38). AUC publicados × demais candidatos = 0.652 (p = 0.066, n = 13).

Estar fora da lista não significa não ser análogo (o catálogo tem 30 locais). Locais do catálogo citados por astrobiologia ou mineralogia não são capturados pelas nossas features. A lista de candidatos já é feita de análogos conhecidos (viés de seleção), então o teste mede a ORDEM dentro dela.

## 3. Robustez à escolha de pesos e de método

| corpo | comparação | Spearman ρ | top 10 em comum |
|---|---|---|---|
| MOON | peso por grupo × peso por coluna | 0.919 | 9/10 |
| MOON | distância nas features × distância no ZEUS | 0.174 | 1/10 |
| MARS | peso por grupo × peso por coluna | 0.894 | 8/10 |
| MARS | distância nas features × distância no ZEUS | 0.219 | 4/10 |

## Leitura

- Teste 1 mostra se as features separam análogos de lugares comuns (cidades, floresta).
- Teste 2 é a comparação com a literatura; hoje limitado pelo acesso às listas publicadas.
- Teste 3 mostra se a conclusão depende de decisões nossas (pesos) ou do método (features × ZEUS).

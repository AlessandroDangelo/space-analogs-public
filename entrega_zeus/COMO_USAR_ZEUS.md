# Como rodar o ZEUS nesta tabela

Não precisa de GPU (45 linhas ≈ 30 s; 450 linhas ≈ 75 s em CPU). Rode tudo **dentro da pasta `entrega_zeus/`**.

**1. Ambiente** (conda, Python 3.11)
```
conda create -n zeus python=3.11 -y
conda activate zeus
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

**2. Código do ZEUS** (versão testada: commit `3f75d28`)
```
git clone https://github.com/gmum/zeus zeus_repo
git -C zeus_repo checkout 3f75d28
```

**3. Checkpoint** `zeus.pt` (305 MB)
```
gdown 1D7uikacymUnmmMxjUjBuCNIomqhBWS67 -O zeus.pt
```
Se o `gdown` falhar: abra https://drive.google.com/file/d/1D7uikacymUnmmMxjUjBuCNIomqhBWS67/view
(link do README do ZEUS), clique em *Download* e salve como `entrega_zeus/zeus.pt`.

**4. Rodar** (embeddings + K-Means k = 2..10, 5 sementes)
```
python rodar_zeus.py
```

**5. Analisar**
```
python analisar_clusters.py
```
Pronto. Abra `analise_clusters.md`.

## Arquivos

| arquivo | o que é |
|---|---|
| `zeus_input.csv` | **entrada**: 17 features numéricas por recorte (5 de relevo, 4 de cobertura, 2 de temperatura, 6 de geologia one-hot), sem IDs. |
| `tabela_completa.csv` | mesmas linhas, na mesma ordem, com IDs, corpo, tipo, lat/lon e metadados. |
| `dicionario_colunas.md` | definição, unidade e fonte de cada coluna. |
| `clusters_zeus.csv` | **saída**: `tile_id` + `cluster_k2` … `cluster_k10` (número do cluster de cada recorte para cada k). |
| `embeddings_zeus.csv` | embedding de 512 dimensões do ZEUS por recorte (o que o K-Means agrupa). |
| `qualidade_k.csv` | por k: silhueta (maior = clusters mais separados) e estabilidade entre sementes (1 = idêntico). |
| `analise_clusters.md` | composição de cada cluster por corpo, locais da Terra junto com Lua/Marte, checagem de sanidade. |
| `analogos_por_k.csv` | lista plana: para cada k, cada recorte da Terra que caiu no mesmo cluster de um recorte lunar/marciano. |

## O que já está decidido (não precisa mexer)
- Pré-processamento e inferência iguais ao código do ZEUS (StandardScaler → MinMax(−1,1), zeros até 30 colunas,
  K-Means com `n_init=100` sobre o embedding normalizado). Única etapa extra: `log1p` nas features (todas ≥ 0 e
  muito assimétricas); sem ela os clusters ficam desbalanceados. Desligar: `python rodar_zeus.py --sem-log`.
- Para cada k ficam 5 sementes (0–4); guarda-se a de menor inércia.
- Lua e Marte entram junto com a Terra no mesmo ajuste (o ZEUS é zero-shot, não há "treino").

**Versão atual: `v1_7`** (coluna `protocol`): relevo + cobertura + temperatura da superfície + geologia, vários recortes de 9 km por local (Terra, 6 regiões lunares, 6 locais
de Marte), rugosidade sem tendência. Se chegar uma tabela nova, basta trocar os dois CSVs e repetir os passos 4–5.

Não testado: GPU/CUDA e o ambiente conda (o teste foi em `venv` com Python 3.11 no Windows).

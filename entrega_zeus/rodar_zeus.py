"""Gera embeddings ZEUS para zeus_input.csv e roda K-Means para k = 2..10.

Uso (de dentro da pasta entrega_zeus/):
    python rodar_zeus.py
Opções (não é preciso mudar nada para o uso normal):
    --entrada zeus_input.csv  --tabela tabela_completa.csv  --checkpoint zeus.pt
    --zeus-dir zeus_repo      --saida clusters_zeus.csv     --device auto|cpu|cuda
    --sem-log                 (desliga o log1p aplicado antes do pré-processamento do ZEUS)

O pré-processamento e a inferência reproduzem o código do ZEUS (github.com/gmum/zeus):
- colunas numéricas: StandardScaler -> MinMaxScaler(-1, 1)   (zeus/datasets.py, load_real_datasets)
- completa com zeros até dim=30                              (zeus/utils.py, evaluate_model)
- modelo: Linear(30->512) + 12 camadas Transformer, 4 cabeças, 1024 ocultos, 10 centros
  (zeus/initialziation.py + zeus/configs.py, valores padrão)
- embeddings: saída sem os 10 tokens de centro, MinMaxScaler(-1, 1), K-Means n_init=100
  (zeus/utils.py, predict_clusters)
Única etapa extra (decisão do projeto, desligável com --sem-log): log1p nas features,
porque todas são magnitudes físicas >= 0 muito assimétricas (relevo de 1 m a 3000 m).

Saídas:
    clusters_zeus.csv       tile_id + cluster_k2 ... cluster_k10
    embeddings_zeus.csv     tile_id + emb_000 ... emb_511 (embedding normalizado usado no K-Means)
    qualidade_k.csv         por k: silhueta no embedding e estabilidade entre sementes (ARI médio)
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
KS = range(2, 11)
SEMENTES = [0, 1, 2, 3, 4]
# Configuração do checkpoint publicado (zeus/configs.py, valores padrão).
DIM, EMBED, HEADS, HID, LAYERS, CENTROS = 30, 512, 4, 1024, 12, 10


def carregar_modelo(zeus_dir: Path, checkpoint: Path, device: str):
    import torch
    sys.path.insert(0, str(zeus_dir))
    try:
        from zeus.configs import LossType
        from zeus.model import encoders
        from zeus.model.zeus import ZeusTransformerModel
    except ImportError as e:
        raise SystemExit(f'Não consegui importar o ZEUS de {zeus_dir}: {e}\n'
                         'Rode: git clone https://github.com/gmum/zeus zeus_repo')
    encoder = encoders.Linear(DIM, EMBED, replace_nan_by_zero=True)
    model = ZeusTransformerModel(encoder, CENTROS, EMBED, HEADS, HID, LAYERS, 0.0,
                                 efficient_eval_masking=True, n_clusters=CENTROS,
                                 dist_based_logit=False, loss_type=LossType.CENTER)
    if not checkpoint.is_file():
        raise SystemExit(f'Checkpoint não encontrado: {checkpoint}. Veja COMO_USAR_ZEUS.md (passo 3).')
    try:
        ck = torch.load(str(checkpoint), map_location='cpu', weights_only=True)
    except Exception:
        # O checkpoint oficial pode conter objetos além dos pesos; é o mesmo carregamento do ZEUS.
        ck = torch.load(str(checkpoint), map_location='cpu', weights_only=False)
    estado = ck['model'] if isinstance(ck, dict) and 'model' in ck else ck
    res = model.load_state_dict(estado, strict=False)  # igual ao zeus/initialziation.py
    # A cabeça `decoder` não é usada no forward com loss CENTER (o modelo retorna antes dela);
    # o checkpoint publicado tem outra cabeça. Qualquer outro peso ausente é erro.
    faltando = [k for k in res.missing_keys if not k.startswith('decoder.')]
    if faltando:
        raise SystemExit(f'Checkpoint incompatível; pesos ausentes: {faltando[:5]} ...')
    if res.unexpected_keys:
        print(f'Aviso: {len(res.unexpected_keys)} chaves extras no checkpoint ignoradas '
              f'(ex.: {res.unexpected_keys[:3]})')
    return model.to(device).eval()


def preprocessar(X: np.ndarray, usar_log: bool) -> np.ndarray:
    from sklearn.preprocessing import MinMaxScaler, StandardScaler
    if usar_log:
        if (X < 0).any():
            raise SystemExit('log1p exige valores >= 0; use --sem-log.')
        X = np.log1p(X)
    X = MinMaxScaler(feature_range=(-1, 1)).fit_transform(StandardScaler().fit_transform(X))
    if X.shape[1] > DIM:
        raise SystemExit(f'Mais de {DIM} colunas; o ZEUS aplicaria PCA. Não previsto nesta entrega.')
    return np.hstack([X, np.zeros((X.shape[0], DIM - X.shape[1]))]).astype(np.float32)


def embeddings(model, X: np.ndarray, device: str) -> np.ndarray:
    import torch
    from sklearn.preprocessing import MinMaxScaler
    torch.manual_seed(42)
    with torch.no_grad():
        out = model(torch.tensor(X).unsqueeze(1).to(device))
    out = out[:-CENTROS].squeeze(1).cpu().numpy()
    return MinMaxScaler((-1, 1)).fit_transform(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--entrada', default=AQUI / 'zeus_input.csv', type=Path)
    ap.add_argument('--tabela', default=AQUI / 'tabela_completa.csv', type=Path)
    ap.add_argument('--checkpoint', default=AQUI / 'zeus.pt', type=Path)
    ap.add_argument('--zeus-dir', default=AQUI / 'zeus_repo', type=Path)
    ap.add_argument('--saida', default=AQUI / 'clusters_zeus.csv', type=Path)
    ap.add_argument('--device', default='auto')
    ap.add_argument('--sem-log', action='store_true')
    a = ap.parse_args()

    import torch
    from sklearn.cluster import KMeans
    from sklearn.metrics import adjusted_rand_score, silhouette_score

    device = ('cuda' if torch.cuda.is_available() else 'cpu') if a.device == 'auto' else a.device
    df = pd.read_csv(a.entrada)
    tab = pd.read_csv(a.tabela, usecols=['tile_id'])
    if len(df) != len(tab):
        raise SystemExit(f'{a.entrada.name} ({len(df)}) e {a.tabela.name} ({len(tab)}) têm linhas diferentes.')
    if df.isna().any().any() or not all(pd.api.types.is_numeric_dtype(df[c]) for c in df):
        raise SystemExit('zeus_input.csv deve ser só numérico e sem NaN.')
    print(f'{len(df)} linhas x {df.shape[1]} features | device={device} | log1p={not a.sem_log}')
    if len(df) > 2500:
        print('Aviso: o ZEUS foi pré-treinado com conjuntos de ~100 a ~2500 linhas.')

    model = carregar_modelo(a.zeus_dir, a.checkpoint, device)
    E = embeddings(model, preprocessar(df.to_numpy(dtype=float), not a.sem_log), device)

    clusters = pd.DataFrame({'tile_id': tab.tile_id})
    qual = []
    for k in KS:
        if k >= len(df):
            break
        rodadas = [KMeans(n_clusters=k, n_init=100, random_state=s).fit(E) for s in SEMENTES]
        melhor = min(rodadas, key=lambda m: m.inertia_)
        clusters[f'cluster_k{k}'] = melhor.labels_
        aris = [adjusted_rand_score(x.labels_, y.labels_) for x, y in itertools.combinations(rodadas, 2)]
        qual.append({'k': k, 'silhueta_embedding': silhouette_score(E, melhor.labels_),
                     'ari_medio_entre_sementes': float(np.mean(aris)), 'inercia': melhor.inertia_,
                     'tamanhos': ' '.join(map(str, np.bincount(melhor.labels_)))})
        print(f'k={k:2d}  silhueta={qual[-1]["silhueta_embedding"]:.3f}  '
              f'estabilidade(ARI)={qual[-1]["ari_medio_entre_sementes"]:.3f}  tamanhos={qual[-1]["tamanhos"]}')

    clusters.to_csv(a.saida, index=False)
    emb = pd.DataFrame(E, columns=[f'emb_{i:03d}' for i in range(E.shape[1])])
    emb.insert(0, 'tile_id', tab.tile_id)
    emb.to_csv(a.saida.with_name('embeddings_zeus.csv'), index=False, float_format='%.6f')
    pd.DataFrame(qual).to_csv(a.saida.with_name('qualidade_k.csv'), index=False)
    print(f'OK: {a.saida.name}, embeddings_zeus.csv, qualidade_k.csv')


if __name__ == '__main__':
    main()

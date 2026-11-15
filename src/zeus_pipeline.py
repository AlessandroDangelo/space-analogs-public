"""Clusterização ZEUS dentro do pipeline do projeto (substitui o passo do colega).

Uso:  python -m src.zeus_pipeline [--protocolo v1_5]
Lê   outputs/<protocolo>/zeus_input.csv e tabela_completa.csv
Gera outputs/<protocolo>/zeus/: clusters_zeus.csv, embeddings_zeus.csv, qualidade_k.csv,
     analise_clusters.md, analogos_por_k.csv

A implementação é a mesma de entrega_zeus/rodar_zeus.py e analisar_clusters.py (importada daqui, para haver um
único código): pré-processamento log1p → StandardScaler → MinMax(−1,1) → zeros até 30 colunas → modelo ZEUS
(checkpoint zeus.pt) → embedding de 512 dimensões normalizado → K-Means (n_init=100, sementes 0–4, guarda a de
menor inércia) para k = 2..10. Requer: cache/zeus_ckpt/zeus.pt e external/zeus (clone do repositório oficial).
"""
from __future__ import annotations

import argparse
import subprocess
import sys

from . import config as C

ENTREGA = C.BASE / 'entrega_zeus'
CHECKPOINT = C.BASE / 'cache' / 'zeus_ckpt' / 'zeus.pt'
ZEUS_DIR = C.BASE / 'external' / 'zeus'


def _rodar(script, args):
    cmd = [sys.executable, str(ENTREGA / script), *map(str, args)]
    print('>', ' '.join(cmd[1:]), flush=True)
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--protocolo', default='v1_7')
    a = ap.parse_args()
    base = C.OUTPUTS / a.protocolo
    out = base / 'zeus'
    out.mkdir(parents=True, exist_ok=True)
    if not CHECKPOINT.is_file() or not ZEUS_DIR.is_dir():
        raise SystemExit(f'Faltam {CHECKPOINT} ou {ZEUS_DIR}; ver entrega_zeus/COMO_USAR_ZEUS.md passos 2–3.')
    _rodar('rodar_zeus.py', ['--entrada', base / 'zeus_input.csv', '--tabela', base / 'tabela_completa.csv',
                             '--checkpoint', CHECKPOINT, '--zeus-dir', ZEUS_DIR, '--saida', out / 'clusters_zeus.csv'])
    _rodar('analisar_clusters.py', ['--clusters', out / 'clusters_zeus.csv', '--tabela', base / 'tabela_completa.csv',
                                    '--qualidade', out / 'qualidade_k.csv', '--saida', out / 'analise_clusters.md'])


if __name__ == '__main__':
    main()

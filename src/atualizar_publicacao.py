"""Copia site/ para o repositório de publicação (GitHub Pages) e cria um commit lá. Não envia nada:
o envio (push) é feito pelo GitHub Desktop, com a conta da equipe.

Uso:  python -m src.atualizar_publicacao [--destino ../earth-dev-defense-site]
- apaga e recopia tudo, menos .git e .nojekyll; ignora arquivos só de desenvolvimento (verificar_numeros.js)
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from .config import BASE

IGNORAR = {'verificar_numeros.js'}
MANTER = {'.git', '.nojekyll'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--destino', default=str(BASE.parent / 'earth-dev-defense-site'))
    a = ap.parse_args()
    dst = Path(a.destino)
    if not (dst / '.git').is_dir():
        raise SystemExit(f'{dst} não é o repositório de publicação (sem .git).')
    for item in dst.iterdir():
        if item.name not in MANTER:
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    for item in (BASE / 'site').iterdir():
        if item.name in IGNORAR:
            continue
        (shutil.copytree if item.is_dir() else shutil.copy2)(item, dst / item.name)
    (dst / '.nojekyll').touch()
    subprocess.run(['git', 'add', '-A'], cwd=dst, check=True)
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=dst).returncode == 0:
        print('Nada mudou no site.')
        return
    subprocess.run(['git', 'commit', '-q', '-m', 'Atualiza o site a partir do repositório do projeto'], cwd=dst, check=True)
    print(f'Commit criado em {dst}. Agora abra o GitHub Desktop e clique em "Push origin".')


if __name__ == '__main__':
    main()

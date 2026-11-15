"""Monta a cópia PÚBLICA do código (repositório github.com/earthdevdefense/space-analogs), com cuidados de segurança
e LGPD. Não envia nada: o envio é feito pela equipe (GitHub Desktop).

O que faz (a partir do último commit, `git archive HEAD`, sem o histórico):
- tira documentos internos: CLAUDE.md, CONTINUAR_DAQUI.md, docs/AVALIACAO_CONTRIBUICOES.md, src/empacotar_compartilhamento.py;
- LGPD (minimização): site/data/equipe.json só com nomes e função; sem e-mails, Lattes, LinkedIn nem fotos de pessoas
  (os contatos ficam só no site publicado, com consentimento de cada integrante);
- dados de terceiros com licença restrita: entrada/terra_por_local.csv só com local, tipo, lat, lon (sem os valores da
  Meteomatics); sai outputs/v1_7/clima/clima_marte_por_alvo.csv (médias anuais derivadas da Meteomatics);
- limpa as saídas do notebook original (entrada/DadosTerra.ipynb);
- acrescenta README.md em inglês (o README em português vira README.pt-BR.md), LICENSE (MIT, só para o código) e
  confere que nenhum arquivo tem e-mail, senha/token ou caminho local.

Uso:  python -m src.preparar_codigo_publico [--destino ../space-analogs-public]
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shutil
import subprocess
import tarfile
from pathlib import Path

from .config import BASE

SITE = 'https://earthdevdefense.github.io'
CODIGO = 'https://github.com/earthdevdefense/space-analogs'
FORA = ['CLAUDE.md', 'CONTINUAR_DAQUI.md', 'docs/AVALIACAO_CONTRIBUICOES.md', 'src/empacotar_compartilhamento.py',
        'outputs/v1_7/clima/clima_marte_por_alvo.csv', 'site/verificar_numeros.js']
FORA_PASTAS = ['site/assets/pessoas']
FORA_PADROES = ['site/assets/equipe-*.jpg']

README_EN = f"""# Space Analogs — Earth Dev Defense

**Where on Earth can we rehearse life on the Moon and Mars?**
NASA Space Apps Challenge 2026 · Ouro Preto, Brazil · challenge *“Identify Earth Locations that Analog the Permanent Moon
Base Locations and Mars”*.

- **Live website:** {SITE}
- **Code (this repository):** {CODIGO}

We compare 43 places on Earth with 12 targets (6 candidate base regions at the lunar south pole and 6 Mars landing
sites) using open data from NASA, ESA and USGS. Every place is cut into 9×9 km tiles on the same 40 m grid on all three
worlds, and we measure four groups with equal weight: terrain (slope, roughness, relief), ground cover, surface
temperature and geology. The result is a 0–100 similarity score per target and per mission type, plus two
complementary views: ZEUS (zero-shot AI clustering) and a Mars climate layer.

## Results in one paragraph
For **Mars**, the most similar places are Askja (Iceland), Devon Island/Haughton and the Changtang plateau (Tibet). For
the **Moon**, nothing on Earth comes close (scores around 50), mostly because of the extreme cold of the lunar south
pole, so lunar analogs must be combined by mission type. Validation: places in ESA’s Catalogue of Planetary Analogues
rank on top for the Moon (AUC 0.85, p = 0.001); analogs rank above cities and rainforest (AUC 0.89 Moon, 0.76 Mars).
**Limits:** the 43 places were chosen by the team (selection bias); the method finds terrain and environment analogs,
not mineralogical ones. Full list in `docs/LIMITACOES.md`.

## Repository map
| path | what |
|---|---|
| `src/` | pipeline (Python): terrain, ground cover, temperature, geology, ZEUS, similarity, validation, site export |
| `site/` | the static website (HTML/CSS/JS, no build) |
| `outputs/` | result tables by protocol version (`v1_7` is current) |
| `entrada/` | inputs: target list, published analog lists, place coordinates |
| `entrega_zeus/` | standalone ZEUS package |
| `METODOLOGIA.md`, `docs/` | full methodology, features and missions, limitations (in Portuguese) |

## How to run
Python 3.11:
```
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt          # Windows; use .venv/bin/python on Linux/macOS
.venv/Scripts/python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
python -m src.rodar_tudo --desde terreno     # full pipeline (downloads public data; NASADEM needs a free NASA Earthdata login)
python -m src.validacao
```
Earthdata login is done once in your own terminal (`earthaccess.login(strategy='interactive', persist=True)`); the code
never stores credentials. To see the website locally: `python -m http.server 8765 --directory site`.

## Data, licenses and privacy
- **Code:** MIT License (see `LICENSE`).
- **Third-party data keep their own licenses and credits** (NASA/USGS public domain; ESA WorldCover CC BY 4.0; AADC
  CC BY 4.0; Macrostrat CC BY 4.0; PGC citation required; ZEUS Apache-2.0). Full list on the website (Methodology →
  Data sources and credits) and in `src/exportar_site.py`.
- **Not included:** raw data from the Meteomatics API (hackathon account; its license does not allow redistribution).
  `entrada/terra_por_local.csv` here has only place names, types and coordinates.
- **Privacy (LGPD):** this repository has no personal contact data or photos; team contacts appear only on the website,
  with each member’s consent.

## Team
Earth Dev Defense — Pablo de Oliveira Passarini (team lead), Luís Gustavo de Oliveira Miranda, Henrique Ulhôa de Faria,
Icaro Luiz Lage Vasconcelos, Alessandro D’Angelo, Gabriel Correia Moreira.
"""

LICENSE = """MIT License

Copyright (c) 2026 Earth Dev Defense team (NASA Space Apps Challenge 2026, Ouro Preto, Brazil)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Note: this license covers the code only. Third-party datasets keep their own licenses (see README.md).
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--destino', default=str(BASE.parent / 'space-analogs-public'))
    a = ap.parse_args()
    dst = Path(a.destino)
    if dst.exists():
        for item in dst.iterdir():                     # recria tudo menos o .git (mantém o histórico de envios)
            if item.name != '.git':
                shutil.rmtree(item) if item.is_dir() else item.unlink()
    dst.mkdir(parents=True, exist_ok=True)

    tar = subprocess.run(['git', 'archive', '--format=tar', 'HEAD'], cwd=BASE, capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as tf:
        tf.extractall(dst)                             # conteúdo do próprio git (confiável)

    for f in FORA:
        (dst / f).unlink(missing_ok=True)
    for d in FORA_PASTAS:
        shutil.rmtree(dst / d, ignore_errors=True)
    for padrao in FORA_PADROES:
        for f in dst.glob(padrao):
            f.unlink()

    # LGPD: equipe só com nome e função
    eq_p = dst / 'site' / 'data' / 'equipe.json'
    eq = json.loads(eq_p.read_text(encoding='utf-8'))
    eq['_como_editar'] = 'Public code copy: contact data and photos removed (LGPD). See the live site for team contacts.'
    eq['fotos'] = []
    eq['integrantes'] = [{'nome': p['nome'], 'funcao': p.get('funcao', ''), 'email': None, 'lattes': None,
                          'linkedin': None, 'foto': ''} for p in eq['integrantes']]
    eq_p.write_text(json.dumps(eq, ensure_ascii=False, indent=2), encoding='utf-8')

    # Meteomatics: só nome, tipo e coordenadas
    loc_p = dst / 'entrada' / 'terra_por_local.csv'
    linhas = list(csv.DictReader(io.StringIO(loc_p.read_text(encoding='utf-8-sig'))))
    with loc_p.open('w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['local', 'tipo', 'lat', 'lon'])
        w.writeheader()
        for r in linhas:
            w.writerow({k: r[k] for k in ['local', 'tipo', 'lat', 'lon']})

    # notebook sem saídas
    nb_p = dst / 'entrada' / 'DadosTerra.ipynb'
    nb = json.loads(nb_p.read_text(encoding='utf-8'))
    for c in nb['cells']:
        if c.get('cell_type') == 'code':
            c['outputs'], c['execution_count'] = [], None
    nb_p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')

    # .gitignore sem nomes de documentos pessoais (troca por uma regra genérica)
    gi = dst / '.gitignore'
    linhas_gi = [l for l in gi.read_text(encoding='utf-8').splitlines() if 'CNH' not in l]
    gi.write_text('\n'.join(linhas_gi) + '\n\n# PDFs soltos na raiz (rascunhos, documentos pessoais)\n/*.pdf\n', encoding='utf-8')

    (dst / 'README.md').rename(dst / 'README.pt-BR.md')
    (dst / 'README.md').write_text(README_EN, encoding='utf-8')
    (dst / 'LICENSE').write_text(LICENSE, encoding='utf-8')

    # conferência final: nada de e-mail, segredo ou caminho local
    problemas = []
    for f in dst.rglob('*'):
        if '.git' in f.parts or not f.is_file() or f.suffix.lower() in {'.png', '.jpg', '.webp', '.pt', '.tif'}:
            continue
        txt = f.read_text(encoding='utf-8', errors='ignore')
        for nome, pad in [('e-mail', r'[A-Za-z0-9._%+-]+@(?!anthropic\.com)[A-Za-z0-9.-]+\.(com|br|org|edu)\b'),
                          ('segredo', r'(?i)(password|senha|token|api[_-]?key|secret)\s*[:=]\s*["\'][^"\']{6,}'),
                          ('caminho local', r'(?i)([A-Z]:\\\\(Users|Documents)\\\\|/[a-z]/Users/|/home/[a-z])')]:
            if re.search(pad, txt):
                problemas.append(f'{nome}: {f.relative_to(dst)}')
    total = sum(1 for f in dst.rglob('*') if f.is_file() and '.git' not in f.parts)
    print(f'{dst}: {total} arquivos')
    print('PROBLEMAS:' if problemas else 'Conferência: sem e-mails, segredos ou caminhos locais.', *problemas, sep='\n  ')


if __name__ == '__main__':
    main()

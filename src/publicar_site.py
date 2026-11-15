"""Copia os dados do pipeline para a pasta do site (site/data/).

Uso:  python -m src.publicar_site
- outputs/site/dados_site.json  -> site/data/dados_site.json
- outputs/site/relevo/*.png     -> site/data/relevo/*.png, reduzidas para no máximo LADO_MAX px no lado maior
  (o site exibe miniaturas; as imagens completas ficam em outputs/site/relevo/).
Rodar depois de `python -m src.rodar_tudo` (ou de `src.exportar_site`).
"""
from __future__ import annotations

import shutil
import warnings

import numpy as np
import rasterio
from rasterio.enums import Resampling

from . import config as C

ORIGEM = C.OUTPUTS / 'site'
DESTINO = C.BASE / 'site' / 'data'
LADO_MAX = 480
warnings.filterwarnings('ignore', category=rasterio.errors.NotGeoreferencedWarning)


def reduzir_png(src_path, dst_path):
    with rasterio.open(src_path) as s:
        f = max(s.width, s.height) / LADO_MAX
        if f <= 1:
            shutil.copy2(src_path, dst_path)
            return
        w, h = int(round(s.width / f)), int(round(s.height / f))
        rgb = s.read([1, 2, 3], out_shape=(3, h, w), resampling=Resampling.average)
        a = s.read(4, out_shape=(h, w), resampling=Resampling.average)
        a = np.where(a >= 255, 255, 0)                     # bordas: só opaco onde todo o bloco tinha dado
    with rasterio.open(dst_path, 'w', driver='PNG', width=w, height=h, count=4, dtype='uint8') as d:
        d.write(np.concatenate([rgb, a[None]]).astype('uint8'))
    for extra in dst_path.parent.glob(dst_path.name + '.aux.xml'):
        extra.unlink()


MINI = 240   # lado das miniaturas quadradas (cards de alvo, trio do Desafio)


def miniatura(src_path, dst_path):
    """Miniatura quadrada e padronizada do relevo (só apresentação, não altera dados): recorta a região com
    dado (alfa), escolhe o quadrado com mais pixels válidos ao longo do lado maior e grava WebP."""
    from PIL import Image
    with rasterio.open(src_path) as s:
        rgba = s.read()
    a = rgba[3] > 0
    linhas, cols = np.flatnonzero(a.any(1)), np.flatnonzero(a.any(0))
    r0, r1, c0, c1 = linhas[0], linhas[-1] + 1, cols[0], cols[-1] + 1
    # maior quadrado com >= 99,5% de pixels válidos (dados em faixa, como o DTM de InSight, não deixam borda irregular)
    ii = np.pad(a.astype(np.int64), ((1, 0), (1, 0))).cumsum(0).cumsum(1)          # imagem integral
    soma = lambda r, c, n: ii[r + n, c + n] - ii[r, c + n] - ii[r + n, c] + ii[r, c]
    pos, lado = (r0, c0), min(r1 - r0, c1 - c0)
    for n in range(lado, max(16, lado // 4), -4):
        achou = next(((r, c) for r in range(r0, r1 - n + 1, 4) for c in range(c0, c1 - n + 1, 4)
                      if soma(r, c, n) >= 0.995 * n * n), None)
        if achou:
            pos, lado = achou, n
            break
    rr, cc = pos
    img = Image.fromarray(np.moveaxis(rgba[:, rr:rr + lado, cc:cc + lado], 0, -1), 'RGBA')
    fundo = Image.new('RGBA', img.size, (16, 26, 85, 255))          # --azul-2 onde não há dado
    Image.alpha_composite(fundo, img).convert('RGB').resize((MINI, MINI), Image.LANCZOS) \
        .save(dst_path, 'WEBP', quality=80, method=6)


def main():
    (DESTINO / 'relevo').mkdir(parents=True, exist_ok=True)
    (DESTINO / 'miniaturas').mkdir(parents=True, exist_ok=True)
    for png in sorted((ORIGEM / 'relevo').glob('*.png')):
        miniatura(png, DESTINO / 'miniaturas' / (png.stem + '.webp'))
    shutil.copy2(ORIGEM / 'dados_site.json', DESTINO / 'dados_site.json')
    n, total = 0, 0
    for png in sorted((ORIGEM / 'relevo').glob('*.png')):
        dst = DESTINO / 'relevo' / png.name
        reduzir_png(png, dst)
        n += 1
        total += dst.stat().st_size
    print(f'OK: {DESTINO} — dados_site.json + {n} imagens ({total / 1e6:.1f} MB)')


if __name__ == '__main__':
    main()

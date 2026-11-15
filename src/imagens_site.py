"""Baixa as imagens reais usadas no visual do site e grava em WebP dentro de site/assets/img/ (sem hotlink).

Todas são de domínio público (NASA/JPL/USGS) ou derivadas da NASA (Blue Marble, distribuída pelo three-globe, MIT):
- lua_polo_sul.webp   PIA00001 "South Pole Region of the Moon as Seen by Clementine" — NASA/JPL/USGS
- marte_hemisferio.webp PIA00003 "Valles Marineris Hemisphere" (mosaico Viking) — NASA/JPL/USGS
- terra_blue_marble.webp / terra_relevo.webp  texturas do globo 3D (NASA Blue Marble e topografia), cópia do
  pacote three-globe@2.42.4 (antes carregadas por CDN)
Os créditos aparecem na seção "Fontes de dados e créditos" do site (src/exportar_site.py, FONTES).
Uso: python -m src.imagens_site   (requer Pillow, só para desenvolvimento)
"""
from __future__ import annotations

import io
import urllib.request

from PIL import Image

from .config import BASE

DEST = BASE / 'site' / 'assets' / 'img'
IMAGENS = {
    'lua_polo_sul.webp': ('https://images-assets.nasa.gov/image/PIA00001/PIA00001~large.jpg', 1000, 70),
    'marte_hemisferio.webp': ('https://images-assets.nasa.gov/image/PIA00003/PIA00003~large.jpg', 1000, 72),
    'terra_blue_marble.webp': ('https://cdn.jsdelivr.net/npm/three-globe@2.42.4/example/img/earth-blue-marble.jpg', 4096, 82),
    'terra_relevo.webp': ('https://cdn.jsdelivr.net/npm/three-globe@2.42.4/example/img/earth-topology.png', 2048, 80),
}


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for nome, (url, largura, q) in IMAGENS.items():
        dados = urllib.request.urlopen(url, timeout=120).read()
        im = Image.open(io.BytesIO(dados))
        if nome == 'lua_polo_sul.webp':   # recorta as legendas da borda (texto da missão e graus)
            w, h = im.size
            im = im.crop((round(w * .114), round(h * .114), round(w * .886), round(h * .886)))
        im = im.convert('L') if im.mode in ('L', 'I', 'I;16', 'P') and nome != 'terra_blue_marble.webp' else im.convert('RGB')
        if im.width > largura:
            im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
        im.save(DEST / nome, 'WEBP', quality=q, method=6)
        print(f'{nome}: {im.width}x{im.height}, {(DEST / nome).stat().st_size / 1e3:.0f} kB  <- {url}')


if __name__ == '__main__':
    main()

"""Gera site/assets/icones.svg: sprite com os ícones do site, todos do mesmo conjunto (Lucide, licença ISC),
mesmo traço (1,75) e viewBox 24. Uso no HTML: <svg class="ic"><use href="assets/icones.svg#i-nome"/></svg>.

Fonte: lucide-static@0.460.0 (https://lucide.dev, ISC). Uso: python -m src.icones_site
"""
from __future__ import annotations

import re
import urllib.request

from .config import BASE

VERSAO = '0.460.0'
ICONES = ['map-pin', 'crosshair', 'grid-3x3', 'sliders-horizontal', 'shield-check', 'triangle-alert', 'piggy-bank',
          'recycle', 'leaf', 'rocket', 'globe', 'plane-landing', 'thermometer-snowflake', 'pickaxe', 'wind',
          'mountain', 'layers', 'thermometer', 'gem', 'scan', 'scale', 'cpu', 'cloud-sun', 'mail', 'linkedin',
          'graduation-cap', 'menu', 'x', 'arrow-right', 'arrow-down', 'chevron-down', 'info', 'building-2']
DEST = BASE / 'site' / 'assets' / 'icones.svg'


def main():
    simbolos = []
    for nome in ICONES:
        svg = urllib.request.urlopen(
            f'https://cdn.jsdelivr.net/npm/lucide-static@{VERSAO}/icons/{nome}.svg', timeout=60).read().decode()
        corpo = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1).strip()
        corpo = re.sub(r'\s+', ' ', corpo)
        simbolos.append(f'<symbol id="i-{nome}" viewBox="0 0 24 24">{corpo}</symbol>')
    DEST.write_text(
        f'<!-- Ícones Lucide (lucide-static@{VERSAO}, ISC License, https://lucide.dev). Gerado por src/icones_site.py -->\n'
        '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="1.75" '
        'stroke-linecap="round" stroke-linejoin="round">\n' + '\n'.join(simbolos) + '\n</svg>\n', encoding='utf-8')
    print(f'{DEST}: {len(simbolos)} ícones, {DEST.stat().st_size / 1e3:.1f} kB')


if __name__ == '__main__':
    main()

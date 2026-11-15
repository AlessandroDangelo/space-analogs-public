"""Roda o pipeline inteiro, na ordem, a partir de uma etapa.

Uso:
    python -m src.rodar_tudo                   # cobertura → zeus → similaridade → site (terreno v1_4 já existe)
    python -m src.rodar_tudo --desde terreno   # refaz também o terreno v1_4 (~10 min; NASADEM em cache)
    python -m src.rodar_tudo --desde zeus      # só a partir da clusterização

Etapas: terreno (src.v1_4) → cobertura (src.cobertura, gera v1_5) → temperatura (src.temperatura, gera v1_6)
        → geologia (src.geologia, gera v1_7)
        → zeus (src.zeus_pipeline) → similaridade (src.similaridade_sites) → site (src.exportar_site)
"""
from __future__ import annotations

import argparse
import subprocess
import sys

ETAPAS = [
    ('terreno', ['-m', 'src.v1_4']),
    ('cobertura', ['-m', 'src.cobertura']),
    ('temp_terra', ['-m', 'src.temperatura', 'terra']),     # usa cache/power/ se já existir
    ('temp_lua', ['-m', 'src.temperatura', 'lua']),         # requer cache/diviner/dlre_prp_south.tab
    ('temp_marte', ['-m', 'src.temperatura', 'marte']),     # requer cache/mars_gcm/*.nc
    ('temperatura', ['-m', 'src.temperatura', 'montar']),   # gera v1_6
    ('geo_terra', ['-m', 'src.geologia', 'terra']),         # Macrostrat (cache em cache/macrostrat/)
    ('geo_lua', ['-m', 'src.geologia', 'lua']),
    ('geo_marte', ['-m', 'src.geologia', 'marte']),
    ('geologia', ['-m', 'src.geologia', 'montar']),         # gera v1_7
    ('zeus', ['-m', 'src.zeus_pipeline', '--protocolo', 'v1_7']),
    ('similaridade', ['-m', 'src.similaridade_sites', '--protocolo', 'v1_7']),
    ('clima', ['-m', 'src.clima_marte', '--protocolo', 'v1_7']),    # clima de Marte (Luís); requer --extrair 1x
    ('site', ['-m', 'src.exportar_site', '--protocolo', 'v1_7']),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde', default='cobertura', choices=[e for e, _ in ETAPAS])
    a = ap.parse_args()
    inicio = [e for e, _ in ETAPAS].index(a.desde)
    for nome, args in ETAPAS[inicio:]:
        print(f'\n===== {nome} =====', flush=True)
        subprocess.run([sys.executable, *args], check=True)
    print('\nPronto. Resultado para o site: outputs/site/dados_site.json e outputs/site/relevo/')


if __name__ == '__main__':
    main()

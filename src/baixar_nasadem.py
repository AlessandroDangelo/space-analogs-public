"""Baixa para cache/nasadem/ os tiles NASADEM das janelas de 27 km (V1.4) dos locais terrestres.

Uso:  python -m src.baixar_nasadem [--n 675]
Requer login Earthdata feito antes pelo usuário (netrc). Falhas por local vão para
outputs/v1_4/download_nasadem_status.csv.
"""
from __future__ import annotations

import argparse

import pandas as pd
from rasterio.warp import transform_bounds

from . import config as C
from .fontes_terra import alvo_grid, tiles_nasadem
from .util import ler_csv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=675, help='pixels da janela (675 x 40 m = 27 km)')
    a = ap.parse_args()
    cat = ler_csv(C.CSV_LOCAIS)
    status = []
    for _, r in cat.iterrows():
        fonte, crs, _cx, _cy, tf = alvo_grid(r.lat, r.lon, a.n)
        if fonte != 'NASADEM':
            continue
        bbox = transform_bounds(crs, 'EPSG:4326', tf.c, tf.f - a.n * C.RES_M,
                                tf.c + a.n * C.RES_M, tf.f, densify_pts=21)
        try:
            tiles = tiles_nasadem(bbox)
            status.append({'site_id': r.region_id, 'status': 'OK', 'tiles': ';'.join(p.name for p in tiles)})
            print('OK', r.local, len(tiles), flush=True)
        except Exception as e:
            status.append({'site_id': r.region_id, 'status': 'ERRO', 'tiles': f'{type(e).__name__}: {e}'})
            print('ERRO', r.local, e, flush=True)
    out = C.OUTPUTS / 'v1_4'
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(status).to_csv(out / 'download_nasadem_status.csv', index=False)
    print('Resumo:', pd.DataFrame(status).status.value_counts().to_dict())


if __name__ == '__main__':
    main()

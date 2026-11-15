"""Verifica se os módulos de src/ reproduzem o terrain_features_v1_3_1.csv original.

Uso:
    python -m src.verificar_v1_3_1                 # alvos planetários (só arquivos locais)
    python -m src.verificar_v1_3_1 --pgc ID [ID]   # + locais ArcticDEM/REMA via STAC PGC (sem login)

NASADEM não é testado aqui porque exige login Earthdata.
"""
from __future__ import annotations

import argparse
import io
import sys
import zipfile

import numpy as np
import pandas as pd

from . import config as C
from .features import calcular_features
from .fontes_terra import dem_terra
from .planetas import dem_planeta, procurar_planeta

ZIP_ENTREGA = C.ENTRADA / 'space_analogs_clustering_pronto_v1_3_1.zip'
CSV_NO_ZIP = '03_referencia_e_auditoria/terrain_features_v1_3_1.csv'
COLS = C.FEATURES + ['valid_coverage_pct', 'nodata_pixels', 'p05_elevation_m', 'p95_elevation_m']


def original():
    with zipfile.ZipFile(ZIP_ENTREGA) as z:
        return pd.read_csv(io.BytesIO(z.read(CSV_NO_ZIP))).set_index('region_id')


def comparar(ident, feat, ref, rtol=1e-9):
    linhas = []
    for c in COLS:
        a, b = float(feat[c]), float(ref.loc[ident, c])
        linhas.append((ident, c, b, a, abs(a - b), np.isclose(a, b, rtol=rtol, atol=1e-9)))
    return linhas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pgc', nargs='*', default=[], help='region_id terrestres ArcticDEM/REMA')
    a = ap.parse_args()
    ref = original()
    linhas = []
    for ident, _nome, _corpo, pattern, _src in C.PLANETA_CFG:
        dem, *_ = dem_planeta(procurar_planeta(pattern))
        linhas += comparar(ident, calcular_features(dem), ref)
    for ident in a.pgc:
        lat, lon = ref.loc[ident, ['center_lat', 'center_lon']]
        dem, *_ = dem_terra(float(lat), float(lon))
        # Mosaicos PGC podem ter sido reprocessados desde a execução original: tolerância maior.
        linhas += comparar(ident, calcular_features(dem), ref, rtol=1e-6)
    df = pd.DataFrame(linhas, columns=['region_id', 'coluna', 'original', 'recalculado', 'abs_diff', 'ok'])
    pd.set_option('display.width', 200)
    print(df.to_string(index=False))
    print('\nTODOS IGUAIS:', bool(df.ok.all()))
    sys.exit(0 if df.ok.all() else 1)


if __name__ == '__main__':
    main()

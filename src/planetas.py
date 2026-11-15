"""Leitura dos DEMs planetários (GeoTIFF projetado em metros, CRS do próprio corpo)."""
from __future__ import annotations

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.warp import reproject

from . import config as C


def procurar_planeta(padrao, base=None):
    # Procura os GeoTIFFs que o usuário baixou previamente (em entrada/).
    base = C.ENTRADA if base is None else base
    arqs = sorted(base.glob(padrao))
    if not arqs:
        arqs = sorted(base.rglob(padrao))
    return arqs[0] if arqs else None


def dem_planeta(arquivo, n=None):
    n = C.N if n is None else n
    with rasterio.open(str(arquivo)) as src:
        if src.crs is None or src.crs.linear_units not in ('metre', 'meter'):
            raise ValueError('DEM planetário não possui projeção linear em metros.')
        cx = (src.bounds.left + src.bounds.right) / 2
        cy = (src.bounds.bottom + src.bounds.top) / 2
        m = n * C.RES_M / 2
        dst_tf = from_origin(cx - m, cy + m, C.RES_M, C.RES_M)
        # Reprojeção/regradeamento dentro do CRS do próprio corpo; não usa WGS84.
        destino = np.full((n, n), np.nan, dtype='float64')
        reproject(source=rasterio.band(src, 1), destination=destino,
                  src_transform=src.transform, src_crs=src.crs,
                  src_nodata=src.nodata, dst_transform=dst_tf,
                  dst_crs=src.crs, dst_nodata=np.nan,
                  resampling=Resampling.average)
        return destino, dst_tf, src.crs, {
            'source_files': arquivo.name, 'source_native_resolution_m': abs(src.res[0]),
            'crs_analysis': src.crs.to_wkt(),
            'center_x_m': cx, 'center_y_m': cy,
            'center_lat': np.nan, 'center_lon': np.nan,
        }

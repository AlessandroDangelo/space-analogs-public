"""Utilitários do notebook V1.3.1: IDs, leitura do catálogo e gravação de recortes."""
from __future__ import annotations

import re
import unicodedata

import numpy as np
import pandas as pd
import rasterio


def slug(txt):
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ascii', 'ignore').decode('ascii')
    return re.sub('[^a-z0-9]+', '_', txt.lower()).strip('_')


def ler_csv(path):
    catalogo = pd.read_csv(path, encoding='utf-8-sig')
    req = {'local', 'tipo', 'lat', 'lon'}
    if not req.issubset(set(catalogo.columns)):
        raise ValueError(f'CSV precisa conter colunas {sorted(req)}')
    catalogo['lat'] = pd.to_numeric(catalogo.lat, errors='raise')
    catalogo['lon'] = pd.to_numeric(catalogo.lon, errors='raise')
    if catalogo[['lat', 'lon']].isna().any().any():
        raise ValueError('CSV possui lat/lon vazias')
    if not catalogo.lat.between(-90, 90).all() or not catalogo.lon.between(-180, 180).all():
        raise ValueError('Coordenadas fora de limites terrestres')
    if catalogo.local.duplicated().any():
        raise ValueError('Nomes de locais duplicados; alterar IDs')
    catalogo['region_id'] = catalogo.local.map(lambda x: 'earth_' + slug(x))
    if catalogo.region_id.duplicated().any():
        raise ValueError('IDs normalizados duplicados; necessário identificador distinto')
    return catalogo


def salvar_tif(arquivo, dem, tf, crs):
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    h, w = dem.shape
    with rasterio.open(str(arquivo), 'w', driver='GTiff', width=w, height=h,
                       count=1, dtype='float32', crs=crs, transform=tf,
                       nodata=-9999, compress='deflate', predictor=3) as dst:
        dst.write(np.where(np.isfinite(dem), dem, -9999).astype('float32'), 1)

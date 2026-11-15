"""Cálculo das 8 features topográficas do protocolo V1.3.1 (idêntico ao notebook)."""
from __future__ import annotations

import numpy as np
from scipy.ndimage import binary_dilation, distance_transform_edt, gaussian_filter, uniform_filter

from .config import BORDA_PX, MIN_VALID_PCT, N, RAIO_EXCLUSAO_NODATA, RES_M, RUGOSIDADE_JANELA, SIGMA_PX


def calcular_features(dem):
    """Extrai oito features; não altera o DEM original nem oculta os NoData.

    Até 0,1% de pixels faltantes: preenchimento vizinho apenas para permitir
    filtros numéricos, mas métricas de declividade e rugosidade ignoram 7 pixels
    de vizinhança de cada lacuna. Relevo e quantis usam somente pixels originais.
    """
    if dem.shape != (N, N):
        raise ValueError('Recorte não tem dimensões N × N.')
    dem = np.asarray(dem, dtype='float64')
    validos = np.isfinite(dem)
    n_validos = int(validos.sum())
    n_ausentes = int(validos.size - n_validos)
    cobertura = 100.0 * validos.mean()
    if cobertura < MIN_VALID_PCT - 1e-7:
        raise ValueError(
            f'Cobertura insuficiente: {cobertura:.4f}% '
            f'(mínima {MIN_VALID_PCT}%; ausentes {n_ausentes}/{validos.size})'
        )
    if n_validos == 0:
        raise ValueError('Recorte sem elevações válidas.')

    # Mantém dem inalterado: só interpola temporariamente para viabilizar filtros.
    if n_ausentes:
        indices = distance_transform_edt(
            ~validos, return_distances=False, return_indices=True
        )
        dem_filtro = dem.copy()
        dem_filtro[~validos] = dem[tuple(indices)][~validos]
    else:
        dem_filtro = dem

    z = gaussian_filter(dem_filtro, sigma=SIGMA_PX, mode='reflect')
    gy, gx = np.gradient(z, RES_M, RES_M)
    decliv = np.degrees(np.arctan(np.hypot(gx, gy)))
    ctr = z - z.mean()
    media = uniform_filter(ctr, size=RUGOSIDADE_JANELA, mode='reflect')
    media2 = uniform_filter(ctr**2, size=RUGOSIDADE_JANELA, mode='reflect')
    rug = np.sqrt(np.maximum(media2 - media**2, 0))

    # Máscara geográfica realmente usada para calcular métricas locais.
    area_metricas = np.ones((N, N), dtype=bool)
    if BORDA_PX:
        area_metricas[:BORDA_PX, :] = False
        area_metricas[-BORDA_PX:, :] = False
        area_metricas[:, :BORDA_PX] = False
        area_metricas[:, -BORDA_PX:] = False
    if n_ausentes:
        zona_exclusao = binary_dilation(
            ~validos,
            structure=np.ones((3, 3), dtype=bool),
            iterations=RAIO_EXCLUSAO_NODATA,
        )
        area_metricas &= ~zona_exclusao
    if not area_metricas.any():
        raise ValueError('Sem pixels confiáveis para métricas locais.')

    decl = decliv[area_metricas]
    r = rug[area_metricas]
    elevacoes = dem[validos]
    p05, p95 = np.percentile(elevacoes, [5, 95])

    return {
        'analysis_resolution_m': RES_M,
        'aoi_size_m': N * RES_M,
        'valid_coverage_pct': float(cobertura),
        'nodata_pixels': n_ausentes,
        'local_metrics_coverage_pct': float(100 * area_metricas.mean()),
        'nodata_treatment': 'nearest_for_filter_only_exclude_7px' if n_ausentes else 'none',
        'mean_slope_deg': float(decl.mean()),
        'roughness_m': float(r.mean()),
        'relative_relief_m': float(elevacoes.max() - elevacoes.min()),
        'median_slope_deg': float(np.median(decl)),
        'p90_slope_deg': float(np.percentile(decl, 90)),
        'median_roughness_m': float(np.median(r)),
        'p90_roughness_m': float(np.percentile(r, 90)),
        'p05_elevation_m': float(p05),
        'p95_elevation_m': float(p95),
        'robust_relief_p95_p5_m': float(p95 - p05),
    }

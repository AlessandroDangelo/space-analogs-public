"""Investigação: a rugosidade lunar da V1.4 (~1 m) é artefato do mosaico LOLA 20 m?

1) Resolução efetiva (LDEM_80S_20MPP_ADJ_EFFRES.TIF, PGDA) por recorte lunar.
2) Recalcula as features V1.4 com os DEMs LOLA 5 m por local (PGDA produto 78), regradeados na MESMA grade
   de 40 m, e compara com a tabela V1.4 (mosaico 20 m).
Uso: python -m src.investigar_lua   -> outputs/v1_4/investigacao_lua/
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject

from . import config as C
from .v1_4 import (N_JANELA, campos, features_recorte, grade_3x3, janela_raster, xy_no_crs)

OUT = C.OUTPUTS / 'v1_4' / 'investigacao_lua'
EFFRES = 'https://pgda.gsfc.nasa.gov/data/LOLA_20mpp/LDEM_80S_20MPP_ADJ_EFFRES.TIF'
MOSAICO = 'https://pgda.gsfc.nasa.gov/data/LOLA_20mpp/LDEM_80S_20MPP_ADJ.TIF'
# DEMs 5 m do PGDA (TIFF em faixas, não COG: baixados de https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/<Site>/)
L5 = C.BASE / 'cache' / 'lola5m'
DEM5 = {  # alvo -> DEM 5 m do PGDA com o mesmo centro
    'moon_haworth': str(L5 / 'Haworth_final_adj_5mpp_surf.tif'),
    'moon_malapert_massif': str(L5 / 'Site23_final_adj_5mpp_surf.tif'),
    'moon_mons_mouton_plateau': str(L5 / 'Site20v2_final_adj_5mpp_surf.tif'),
    'moon_nobile_rim_2': str(L5 / 'DM2_final_adj_5mpp_surf.tif'),
    'moon_de_gerlache_rim': str(L5 / 'Site11_final_adj_5mpp_surf.tif'),
    'moon_connecting_ridge': str(C.ENTRADA / 'Site01_final_adj_5mpp_surf.tif'),
}
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR', GDAL_HTTP_MAX_RETRY='3', GDAL_HTTP_RETRY_DELAY='1')
FEATS = ['median_slope_deg', 'p90_slope_deg', 'median_roughness_m', 'p90_roughness_m', 'robust_relief_p95_p5_m',
         'roughness_legacy_median_m']


def regradear(href, tf, crs, n=N_JANELA, resampling=Resampling.average):
    dst = np.full((n, n), np.nan, 'float64')
    with rasterio.Env(**ENV), rasterio.open(href) as src:
        reproject(rasterio.band(src, 1), dst, src_transform=src.transform, src_crs=src.crs, src_nodata=src.nodata,
                  dst_transform=tf, dst_crs=crs, dst_nodata=np.nan, resampling=resampling)
    return dst


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    alvos = pd.read_csv(C.ALVOS_CSV)
    alvos = alvos[alvos.corpo == 'MOON']
    tab = pd.read_csv(C.OUTPUTS / 'v1_4' / 'tabela_completa.csv').set_index('tile_id')
    linhas = []
    for _, a in alvos.iterrows():
        print(a.id, flush=True)
        cx, cy = xy_no_crs(MOSAICO, a.lat_centro, a.lon_centro)
        dem20, tf, crs, _ = janela_raster(MOSAICO, cx, cy)
        eff = regradear(EFFRES, tf, crs)
        dem5 = regradear(DEM5[a.id], tf, crs)
        F5 = campos(dem5)
        for nome, r0, c0 in grade_3x3():
            tid = f'{a.id}_{nome}'
            sl = (slice(r0, r0 + 225), slice(c0, c0 + 225))
            e = eff[sl]
            linha = {'tile_id': tid, 'effres_mediana_m': float(np.nanmedian(e)),
                     'effres_p90_m': float(np.nanpercentile(e, 90)),
                     'frac_effres_maior_40m': float(np.nanmean(e > 40)),
                     'frac_effres_maior_80m': float(np.nanmean(e > 80))}
            for f in FEATS:
                linha[f'{f}__20m'] = tab.loc[tid, f] if tid in tab.index else np.nan
            # o recorte 5 m só vale se o recorte E a margem dos filtros estiverem cobertos pelo DEM 5 m
            bloco = np.isfinite(dem5[r0 - 24:r0 + 249, c0 - 24:c0 + 249]).mean()
            feat5, motivo = features_recorte(F5, r0, c0) if bloco >= 0.999 else (None, 'fora do DEM 5 m')
            for f in FEATS:
                linha[f'{f}__5m'] = feat5[f] if feat5 else np.nan
            linha['obs_5m'] = motivo
            linhas.append(linha)
    df = pd.DataFrame(linhas)
    df.to_csv(OUT / 'comparacao_lua.csv', index=False)
    ok = df.dropna(subset=['median_roughness_m__5m'])
    resumo = []
    for f in FEATS:
        a20, a5 = ok[f'{f}__20m'], ok[f'{f}__5m']
        resumo.append({'feature': f, 'n_recortes': len(ok), 'mediana_20m': a20.median(), 'mediana_5m': a5.median(),
                       'razao_mediana_5m_sobre_20m': (a5 / a20).median()})
    pd.DataFrame(resumo).to_csv(OUT / 'resumo_5m_vs_20m.csv', index=False)
    pd.set_option('display.width', 200)
    print(df[['tile_id', 'effres_mediana_m', 'effres_p90_m', 'frac_effres_maior_40m',
              'median_roughness_m__20m', 'median_roughness_m__5m', 'obs_5m']].round(3).to_string(index=False))
    print(pd.DataFrame(resumo).round(3).to_string(index=False))


def kaguya(max_dtms=6):
    """3) Fonte independente: DTMs estéreo Kaguya TC v2 (USGS STAC), ~27–33 m, na mesma grade de 40 m."""
    from pystac_client import Client
    cli = Client.open('https://stac.astrogeology.usgs.gov/api/')
    alvos = pd.read_csv(C.ALVOS_CSV)
    alvos = alvos[alvos.corpo == 'MOON']
    tab = pd.read_csv(C.OUTPUTS / 'v1_4' / 'tabela_completa.csv').set_index('tile_id')
    linhas = []
    for _, a in alvos.iterrows():
        cx, cy = xy_no_crs(MOSAICO, a.lat_centro, a.lon_centro)
        _, tf, crs, _ = janela_raster(MOSAICO, cx, cy, n=8)          # só para obter a grade
        tf = rasterio.transform.from_origin(cx - N_JANELA * 20, cy + N_JANELA * 20, 40, 40)
        d = 0.05
        itens = list(cli.search(collections=['kaguya_terrain_camera_usgs_dtms_v2_southpolar'],
                                bbox=[a.lon_centro - d, a.lat_centro - 0.005, a.lon_centro + d, a.lat_centro + 0.005],
                                max_items=max_dtms).items())
        print(a.id, len(itens), 'DTMs Kaguya', flush=True)
        F20 = campos(regradear(MOSAICO, tf, crs))
        for it in itens:
            try:
                dem = regradear(it.assets['dtm'].href, tf, crs)
            except Exception as e:  # noqa: BLE001
                print('  falha', it.id, type(e).__name__)
                continue
            if np.isfinite(dem).mean() < 0.05:
                continue
            F = campos(dem)
            # comparação pareada: mesmos pixels nas duas fontes (válidos e fora das zonas de exclusão)
            mask_all = F['validos'] & ~F['excl_reg'] & F20['validos'] & ~F20['excl_reg']
            for nome, r0, c0 in grade_3x3():
                sl = (slice(r0, r0 + 225), slice(c0, c0 + 225))
                m = mask_all[sl]
                if m.mean() < 0.5:
                    continue
                linhas.append({'tile_id': f'{a.id}_{nome}', 'kaguya_dtm': it.id, 'gsd_m': it.properties.get('gsd'),
                               'frac_pixels_pareados': float(m.mean()),
                               'median_slope_deg__kaguya': float(np.median(F['decliv'][sl][m])),
                               'median_slope_deg__lola20m': float(np.median(F20['decliv'][sl][m])),
                               'median_roughness_m__kaguya': float(np.median(F['rug'][sl][m])),
                               'median_roughness_m__lola20m': float(np.median(F20['rug'][sl][m])),
                               'p90_roughness_m__kaguya': float(np.percentile(F['rug'][sl][m], 90)),
                               'p90_roughness_m__lola20m': float(np.percentile(F20['rug'][sl][m], 90))})
    df = pd.DataFrame(linhas)
    df.to_csv(OUT / 'comparacao_kaguya.csv', index=False)
    if df.empty:
        print('nenhum recorte com >= 50% de pixels pareados')
        return
    ks = ['median_slope_deg', 'median_roughness_m', 'p90_roughness_m']
    res = [{'feature': k, 'n_pares': len(df), 'recortes_distintos': df.tile_id.nunique(),
            'mediana_lola20m': df[f'{k}__lola20m'].median(), 'mediana_kaguya': df[f'{k}__kaguya'].median(),
            'razao_mediana_kaguya_sobre_lola': (df[f'{k}__kaguya'] / df[f'{k}__lola20m']).median()} for k in ks]
    pd.DataFrame(res).to_csv(OUT / 'resumo_kaguya_vs_lola.csv', index=False)
    print(pd.DataFrame(res).round(3).to_string(index=False))


if __name__ == '__main__':
    import sys
    kaguya() if 'kaguya' in sys.argv else main()

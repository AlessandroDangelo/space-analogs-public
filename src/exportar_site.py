"""Exporta os dados para o site interativo (JSON + imagens de relevo).

Uso:  python -m src.exportar_site [--protocolo v1_5]
Gera outputs/site/:
    dados_site.json        tudo o que o site precisa (ver a seção "Esquema do JSON" em METODOLOGIA.md)
    relevo/{site_id}.png   relevo sombreado da janela de cada local, com os recortes válidos contornados
Pré-requisitos: outputs/<protocolo>/tabela_completa.csv, zeus/ e similaridade/ (rodar antes
src.zeus_pipeline e src.similaridade_sites).
"""
from __future__ import annotations

import argparse
import json
import warnings
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import rasterio

from . import config as C
from .v1_4 import MARGEM, N_TILE

OUT = C.OUTPUTS / 'site'
# PNG é imagem simples (sem georreferência) de propósito; o aviso do GDAL é esperado.
warnings.filterwarnings('ignore', category=rasterio.errors.NotGeoreferencedWarning)

FEATURES_INFO = [  # column, display name (English, shown on the site), unit, group
    ('median_slope_deg', 'Median slope', '°', 'terreno'),
    ('p90_slope_deg', 'Slope (90th percentile)', '°', 'terreno'),
    ('median_roughness_m', 'Median roughness', 'm', 'terreno'),
    ('p90_roughness_m', 'Roughness (90th percentile)', 'm', 'terreno'),
    ('robust_relief_p95_p5_m', 'Relief (P95 − P5)', 'm', 'terreno'),
    ('frac_solo_exposto', 'Bare ground', 'fraction', 'cobertura'),
    ('frac_neve_gelo', 'Snow and ice', 'fraction', 'cobertura'),
    ('frac_vegetacao', 'Vegetation', 'fraction', 'cobertura'),
    ('frac_construido', 'Built-up area', 'fraction', 'cobertura'),
    ('t_sup_media_K', 'Mean annual surface temperature', 'K', 'temperatura'),
    ('t_sup_max_K', 'Maximum annual surface temperature', 'K', 'temperatura'),
    ('lito_vulcanica', 'Geology: volcanic', 'fraction of tiles', 'geologia'),
    ('lito_cristalina', 'Geology: crystalline (intrusive/metamorphic)', 'fraction of tiles', 'geologia'),
    ('lito_sedimentar', 'Geology: sedimentary', 'fraction of tiles', 'geologia'),
    ('lito_evaporitica', 'Geology: evaporite', 'fraction of tiles', 'geologia'),
    ('lito_gelo', 'Geology: ice', 'fraction of tiles', 'geologia'),
    ('lito_impacto_terras_altas', 'Geology: impact / highlands', 'fraction of tiles', 'geologia'),
]
# Place names shown on the site, in English (the pipeline keeps the original names in its tables).
NOMES_EN = {
    'earth_atacama_chajnantor': 'Atacama – Chajnantor', 'earth_atacama_yungay': 'Atacama – Yungay',
    'earth_bacia_de_qaidam': 'Qaidam Basin', 'earth_danakil_dallol': 'Danakil – Dallol',
    'earth_deserto_de_lut': 'Lut Desert', 'earth_deserto_de_mojave': 'Mojave Desert',
    'earth_deserto_de_simpson': 'Simpson Desert', 'earth_groenlandia_summit': 'Greenland – Summit',
    'earth_ilha_devon_haughton': 'Devon Island – Haughton', 'earth_islandia_askja': 'Iceland – Askja',
    'earth_londres': 'London', 'earth_mauna_loa_hi_seas': 'Mauna Loa – HI-SEAS', 'earth_namibe': 'Namib Desert',
    'earth_nova_york': 'New York', 'earth_planalto_do_tibete_changtang': 'Tibetan Plateau – Changtang',
    'earth_saara_tanezrouft': 'Sahara – Tanezrouft', 'earth_sao_paulo': 'São Paulo', 'earth_singapura': 'Singapore',
    'earth_svalbard_bockfjorden': 'Svalbard – Bockfjorden', 'earth_utah_mdrs': 'Utah – MDRS',
    'earth_vale_da_morte': 'Death Valley', 'earth_vales_secos_de_mcmurdo': 'McMurdo Dry Valleys',
}
FONTES = [
    {'grupo': 'terra', 'nome': 'NASADEM (NASA/USGS LP DAAC)', 'uso': 'Earth elevation between 56°S and 60°N (~30 m)',
     'url': 'https://lpdaac.usgs.gov/products/nasadem_hgtv001/'},
    {'grupo': 'terra', 'nome': 'ArcticDEM and REMA 32 m mosaics (Polar Geospatial Center)', 'uso': 'Polar Earth elevation',
     'url': 'https://www.pgc.umn.edu/data/', 'credito': 'Use the official PGC citation text'},
    {'grupo': 'lua', 'nome': 'LOLA LDEM 80S 20 m/pix (NASA GSFC PGDA, Barker et al. 2023)', 'uso': 'Lunar elevation (south pole)',
     'url': 'https://pgda.gsfc.nasa.gov/products/90', 'doi': '10.60903/gsfcpgda-lola-spole'},
    {'grupo': 'marte', 'nome': 'Controlled CTX DTMs (USGS Astrogeology, STAC) and Mars 2020 CTX DEM 20 m (USGS)',
     'uso': 'Mars elevation', 'url': 'https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms'},
    {'grupo': 'terra', 'nome': 'ESA WorldCover 2021 v200', 'uso': 'Earth land cover (10 m)',
     'url': 'https://esa-worldcover.org/',
     'credito': '© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by '
                'ESA WorldCover consortium (CC BY 4.0)'},
    {'grupo': 'terra', 'nome': 'Ice-free Antarctica — rock outcrop union (Toth & Terauds 2023, AADC)',
     'uso': 'Antarctic land cover (rock × ice)',
     'url': 'https://data.aad.gov.au/metadata/AAS_4568_ice-free_rock_outcrop_union', 'licenca': 'CC BY 4.0'},
    {'grupo': 'terra', 'nome': 'NASA POWER (climatology, MERRA-2)', 'uso': 'Earth surface temperature',
     'url': 'https://power.larc.nasa.gov/'},
    {'grupo': 'lua', 'nome': 'LRO Diviner Polar Resource Product (LRO-L-DLRE-5-PRP-V2.0)', 'uso': 'Lunar surface temperature',
     'url': 'https://pds-geosciences.wustl.edu/lro/urn-nasa-pds-lro_diviner_derived1/data_derived_prp/'},
    {'grupo': 'marte', 'nome': 'NASA Ames Legacy Mars GCM (Haberle et al. 2019)', 'uso': 'Mars surface temperature',
     'url': 'https://data.nas.nasa.gov/mcmcref/legacygcm/'},
    {'grupo': 'terra', 'nome': 'Macrostrat (compiled geologic maps, CC-BY 4.0)', 'uso': 'Earth geology',
     'url': 'https://macrostrat.org/'},
    {'grupo': 'lua', 'nome': 'USGS Unified Geologic Map of the Moon 1:5M (Fortezzo et al. 2020)', 'uso': 'Lunar geology',
     'url': 'https://astrogeology.usgs.gov/search/map/unified_geologic_map_of_the_moon_1_5m_2020'},
    {'grupo': 'marte', 'nome': 'USGS Geologic Map of Mars 1:20M, SIM 3292 (Tanaka et al. 2014)', 'uso': 'Mars geology',
     'url': 'https://pubs.usgs.gov/publication/sim3292'},
    {'grupo': 'ia_clima', 'nome': 'ZEUS (GMUM, built on TabPFN v1)', 'uso': 'Zero-shot embeddings and clusters',
     'url': 'https://github.com/gmum/zeus', 'licenca': 'Apache-2.0'},
    {'grupo': 'ia_clima', 'nome': 'NASA Ames Mars Climate Modeling Center, Beta Output Release 1 (FV3, doi 10.25966/rjgg-r639)',
     'uso': 'Mars climate (climate layer, work by Luís G. O. Miranda)',
     'url': 'https://data.nas.nasa.gov/mcmc/'},
    {'grupo': 'ia_clima', 'nome': 'Meteomatics Weather API (account provided to Space Apps participants)',
     'uso': 'Earth climate, 1 year of daily data (climate layer); the site shows only similarities and annual means',
     'url': 'https://www.meteomatics.com/en/api/'},
    {'grupo': 'imagens', 'nome': 'South Pole Region of the Moon as Seen by Clementine (PIA00001)',
     'uso': 'Opening background image', 'url': 'https://photojournal.jpl.nasa.gov/catalog/PIA00001',
     'credito': 'NASA/JPL/USGS', 'licenca': 'public domain'},
    {'grupo': 'imagens', 'nome': 'Valles Marineris Hemisphere, Viking mosaic (PIA00003)',
     'uso': 'Mars image in the opening', 'url': 'https://photojournal.jpl.nasa.gov/catalog/PIA00003',
     'credito': 'NASA/JPL/USGS', 'licenca': 'public domain'},
    {'grupo': 'imagens', 'nome': 'NASA Blue Marble and topography (textures distributed with three-globe)',
     'uso': '3D globe texture', 'url': 'https://visibleearth.nasa.gov/collection/1484/blue-marble',
     'credito': 'NASA Earth Observatory'},
    {'grupo': 'imagens', 'nome': 'Lucide icons', 'uso': 'Interface icons', 'url': 'https://lucide.dev',
     'licenca': 'ISC'},
    {'grupo': 'imagens', 'nome': 'globe.gl (Vasco Asturiano)', 'uso': 'Interactive 3D globe',
     'url': 'https://github.com/vasturiano/globe.gl', 'licenca': 'MIT'},
]
AVISOS = [
    'Similarity covers terrain, land cover, surface temperature and geology (a harmonized rock class, which is an '
    'interpretation of regional maps).',
    'Temperatures come from sources of different kinds (reanalysis on Earth, a model fitted to Diviner on the Moon, '
    'a climate model on Mars): comparable in order of magnitude, not within a few kelvin.',
    'Moon and Mars: land cover is assigned (bare ground = 1), not measured.',
    'Flat places on Earth measured with NASADEM look steeper/rougher than they are (DEM noise).',
    'Lunar region centers: PGDA DEMs with the same name (matched by name, not official). Mars: landing points '
    'checked; Oxia at the IAU name center.',
    'Antarctica: land cover from the AADC rock outcrop map (100 m), which does not separate ice from sea.',
    'The Earth places were chosen by the team (mostly known analogs): the ranking orders this list; it is not a '
    'search of the whole planet.',
    'The method finds terrain and environment analogs; mineralogical/astrobiological analogs (e.g. Rio Tinto) rank '
    'low because mineral composition is not measured.',
    'The ranking is the similarity score (explained by group); the ZEUS clusters are a complementary view.',
]


def _sem_nan(df):
    """Registros com NaN trocado por None (JSON válido para o navegador)."""
    return [{k: (None if isinstance(v, float) and v != v else v) for k, v in r.items()} for r in df.to_dict('records')]


def relevo_png(site_id, tiles, destino):
    """Relevo sombreado (azimute 315°, altura 45°) da janela, PNG RGBA, com contorno dos recortes."""
    with rasterio.open(C.OUTPUTS / 'v1_4' / 'dem_janelas' / f'{site_id}.tif') as d:
        z = d.read(1, masked=True).filled(np.nan).astype('float64')
        px = abs(d.transform.a)
    gy, gx = np.gradient(np.where(np.isfinite(z), z, np.nanmean(z)), px, px)
    slope = np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    az, alt = np.radians(315), np.radians(45)
    hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    g = np.clip(255 * hs, 0, 255).astype('uint8')
    rgb = np.stack([g, g, g]).copy()
    alpha = np.where(np.isfinite(z), 255, 0).astype('uint8')
    for t in tiles:
        rc = t.rsplit('_', 1)[1]
        r, c = int(rc[1:rc.index('c')]), int(rc[rc.index('c') + 1:])
        r0, c0 = MARGEM + (r - 1) * N_TILE, MARGEM + (c - 1) * N_TILE
        e = 3                                          # espessura do contorno (px)
        for k, v in enumerate((255, 200, 0)):          # contorno amarelo
            rgb[k, r0:r0 + e, c0:c0 + N_TILE] = v
            rgb[k, r0 + N_TILE - e:r0 + N_TILE, c0:c0 + N_TILE] = v
            rgb[k, r0:r0 + N_TILE, c0:c0 + e] = v
            rgb[k, r0:r0 + N_TILE, c0 + N_TILE - e:c0 + N_TILE] = v
    destino.parent.mkdir(parents=True, exist_ok=True)
    h, w = g.shape
    with rasterio.open(destino, 'w', driver='PNG', width=w, height=h, count=4, dtype='uint8') as dst:
        dst.write(np.concatenate([rgb, alpha[None]]))
    for extra in destino.parent.glob(destino.name + '.aux.xml'):
        extra.unlink()


CLIMA_GRANDEZAS = [  # (id, name, unit, weight) — order and weights from src/clima_marte.py
    ('temp_ar', 'Mean air temperature', 'K', 0.5), ('temp_sup', 'Mean surface temperature', 'K', 0.5),
    ('amp_sazonal_ar', 'Change over the year (air)', 'K', 0.5),
    ('amp_sazonal_sup', 'Change over the year (surface)', 'K', 0.5),
    ('amp_diurna_ar', 'Day–night change (air)', 'K', 0.5),
    ('amp_diurna_sup', 'Day–night change (surface)', 'K', 0.5),
    ('pressao', 'Atmospheric pressure', 'Pa', 1.0), ('precip', 'Rain', 'mm/day', 1.0),
    ('poeira', 'Dust in the atmosphere', 'optical depth', 1.0),
]
CLIMA_AVISOS = [
    'Mars is model output (2° cell, ~120 km, a regional mean), not measurement; Earth is a single year of daily data '
    '(Meteomatics, through Nov 2026), not a climatology.',
    'No place on Earth comes close to Mars in pressure (the lowest on Earth is ~31 times the highest on Mars) or in '
    'day–night change: the values point to the "least different" place, not an equivalent climate.',
    'Climate barely separates one Mars target from another: the most similar places are almost the same for all six.',
    'Gower similarity depends on the range of values in the analyzed set (507 Earth points + 16,200 Mars cells). It is '
    'kept out of the main score because it works at another scale (~120 km region × 9 km tiles).',
    'Dust on Earth = optical depth of mineral dust only (dust AOD 550 nm); the original report used total AOD, which '
    'includes pollution.',
]


def clima_marte(base):
    """Bloco da camada de clima (src.clima_marte); None se ainda não foi calculada."""
    p = base / 'clima' / 'clima_marte_por_alvo.csv'
    if not p.is_file():
        return None
    t = pd.read_csv(p)
    resumo = json.loads((base / 'clima' / 'clima_marte_resumo.json').read_text(encoding='utf-8'))
    ids = [g for g, *_ in CLIMA_GRANDEZAS]
    por_alvo = {}
    for alvo, g in t.groupby('alvo', sort=False):
        por_alvo[alvo] = {
            'marte': {v: resumo['celula_por_alvo'][alvo][v] for v in ids},
            'celula': [resumo['celula_por_alvo'][alvo]['lat'], resumo['celula_por_alvo'][alvo]['lon_leste']],
            'locais': {r['site_id']: {'sim': round(100 * r['sim_clima'], 1), 'pos_global': int(r['posicao_global']),
                                      'grandezas': {v: round(100 * r['s_' + v], 1) for v in ids},
                                      'terra': {v: round(r['x_' + v], 4) for v in ids}}
                       for r in g.to_dict('records')},
            'validacao': resumo['validacao'][alvo],
        }
    # visão "todos os alvos de Marte": média das similaridades dos seis alvos
    media = t.groupby('site_id')['sim_clima'].mean()
    por_alvo['MARS'] = {'locais': {s: {'sim': round(100 * v, 1)} for s, v in media.items()}}
    return {'fonte': resumo['fonte'], 'metodo': resumo['metodo'], 'aerossol_terra': resumo['aerossol_terra'],
            'n_terra_total': resumo['n_terra_total'], 'n_celulas_marte': resumo['n_celulas_marte'],
            'grandezas': [{'id': g, 'nome': n, 'unidade': u, 'peso': w} for g, n, u, w in CLIMA_GRANDEZAS],
            'avisos': CLIMA_AVISOS, 'por_alvo': por_alvo}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--protocolo', default='v1_7')
    a = ap.parse_args()
    base = C.OUTPUTS / a.protocolo
    tab = pd.read_csv(base / 'tabela_completa.csv')
    clus = pd.read_csv(base / 'zeus' / 'clusters_zeus.csv')
    qual = pd.read_csv(base / 'zeus' / 'qualidade_k.csv')
    rank_alvo = pd.read_csv(base / 'similaridade' / 'ranking_por_alvo.csv')
    rank_corpo = pd.read_csv(base / 'similaridade' / 'ranking_por_corpo.csv')
    contrib = pd.read_csv(base / 'similaridade' / 'contribuicoes.csv')
    cols = [c for c, *_ in FEATURES_INFO if c in tab.columns]
    df = tab.merge(clus, on='tile_id', validate='one_to_one')
    kcols = [c for c in clus.columns if c.startswith('cluster_k')]
    # k sugerido: maior silhueta entre k = 3..8 (k = 2 só separa "plano × montanhoso")
    q = qual[(qual.k >= 3) & (qual.k <= 8)]
    k_sug = int(q.loc[q.silhueta_embedding.idxmax(), 'k'])

    locais = []
    for s, g in df.groupby('site_id', sort=False):
        locais.append({
            'site_id': s, 'nome': NOMES_EN.get(s, g.site_name.iloc[0]), 'corpo': g.body.iloc[0], 'tipo': g.tipo.iloc[0],
            'lat': round(float(g.lat.mean()), 5), 'lon': round(float(g.lon.mean()), 5),
            'n_recortes': int(len(g)), 'fonte_dem': g.source_dataset.iloc[0],
            'fonte_cobertura': g.cover_source.iloc[0] if 'cover_source' in g else None,
            'media': {c: round(float(g[c].mean()), 4) for c in cols},
            'desvio': {c: round(float(g[c].std(ddof=0)), 4) for c in cols},
            'imagem_relevo': f'relevo/{s}.png',
            **({'geologia': {'classe_predominante': g.lito_classe.value_counts().index[0],
                             'unidades': g.geo_unidade.value_counts().head(3).to_dict(),
                             'fonte': g.geo_fonte.iloc[0]}} if 'lito_classe' in g else {}),
        })
        relevo_png(s, list(g.tile_id), OUT / 'relevo' / f'{s}.png')
    recortes = [{'tile_id': r.tile_id, 'site_id': r.site_id, 'lat': round(r.lat, 5), 'lon': round(r.lon, 5),
                 'features': {c: round(float(getattr(r, c)), 4) for c in cols},
                 'clusters': {k[8:]: int(getattr(r, k)) for k in kcols}} for r in df.itertuples()]

    dist_grupo_cols = [c for c in rank_corpo.columns
                       if c.startswith('dist_') and c not in ('dist_features', 'dist_zeus')]

    def ranking(rk):
        out = {}
        for alvo, g in rk.groupby('alvo', sort=False):
            out[alvo] = [{'site_id': x.site_id, 'posicao': int(x.posicao), 'score': round(x.score, 1),
                          'dist_features': round(x.dist_features, 4),
                          'dist_zeus': round(x.dist_zeus, 4) if hasattr(x, 'dist_zeus') else None,
                          'dist_grupos': {c[5:]: round(float(getattr(x, c)), 4) for c in dist_grupo_cols},
                          'cocluster': {k[8:]: round(getattr(x, f'cocluster_{k[8:]}'), 3) for k in kcols},
                          'recorte_alvo': x.recorte_alvo_mais_parecido,
                          'recorte_terra': x.recorte_terra_mais_parecido} for x in g.itertuples()]
        return out

    contribs = {}
    for r in contrib.itertuples():
        contribs.setdefault(r.alvo, {})[r.site_id] = {c: round(getattr(r, f'dz_{c}'), 3) for c in cols
                                                      if hasattr(r, f'dz_{c}')}
    dados = {
        'meta': {
            'protocolo': a.protocolo, 'gerado_em_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'features': [{'coluna': c, 'nome': n, 'unidade': u, 'grupo': gr} for c, n, u, gr in FEATURES_INFO
                         if c in cols],
            'k_disponiveis': [int(k[9:]) for k in kcols], 'k_sugerido': k_sug,
            'qualidade_k': qual.round(4).to_dict('records'),
            'score': 'score = 100/(1 + d/d50); d = median, over the target tiles, of the distance to the most similar '
                     'tile of the place, with EQUAL WEIGHT PER GROUP (terrain, land cover, temperature, geology): '
                     'd = root mean square of the group distances. Numeric groups: RMS of standardized differences '
                     '(log1p + z-score); geology: 0 same class, 0.5 undefined, 1 different. d50 = median of all '
                     'target→place distances. 50 = typical pair, 100 = identical.',
            'dist_grupos': 'how far each group sets the place apart from the target (0 = equal); explains the score',
            'contribuicao': 'standardized difference (place − target) of each feature in the most similar pair of tiles; '
                            'near 0 = similar in that feature.',
            'coordenadas': 'Earth: WGS84. Moon/Mars: planetocentric in the body spherical CRS. East-positive '
                           'longitude in -180..180.',
            'fontes': FONTES, 'avisos': AVISOS,
            'analogos_publicados': (_sem_nan(pd.read_csv(C.ENTRADA / 'analogos_publicados_v2.csv')
                                             [['site_id', 'corpo', 'nivel_correspondencia', 'fonte']])
                                    if (C.ENTRADA / 'analogos_publicados_v2.csv').is_file() else []),
            'validacao': (_sem_nan(pd.read_csv(base / 'validacao' / 'validacao.csv').round(4))
                          if (base / 'validacao' / 'validacao.csv').is_file() else []),
        },
        'locais': locais, 'recortes': recortes,
        'similaridade': {'por_corpo': ranking(rank_corpo), 'por_alvo': ranking(rank_alvo),
                         'contribuicoes': contribs},
        'clima_marte': clima_marte(base),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'dados_site.json').write_text(json.dumps(dados, ensure_ascii=False, allow_nan=False), encoding='utf-8')
    print(f'OK: {OUT / "dados_site.json"} ({(OUT / "dados_site.json").stat().st_size / 1e6:.2f} MB), '
          f'{len(locais)} locais, {len(recortes)} recortes, k sugerido = {k_sug}')


if __name__ == '__main__':
    main()

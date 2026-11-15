"""Protocolo v1_7 = v1_6 + classe litológica harmonizada por recorte.

Uso:
    python -m src.geologia terra    # Macrostrat API (cache em cache/macrostrat/)
    python -m src.geologia lua      # Unified Geologic Map of the Moon 1:5M (raster; cache/geologia/moon/)
    python -m src.geologia marte    # Geologic Map of Mars, SIM 3292 (cache/geologia/mars/)
    python -m src.geologia montar   # outputs/v1_7/

Por que uma classe harmonizada: as unidades geológicas da Terra, da Lua e de Marte usam nomes e critérios
diferentes. Para comparar, cada unidade é traduzida para um vocabulário comum de 6 classes (LITO_CLASSES). A
tradução é uma INTERPRETAÇÃO documentada (regras abaixo), não um dado medido. No ZEUS entra como one-hot.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request

import pandas as pd

from . import config as C

CACHE = C.BASE / 'cache'
INTER = C.OUTPUTS / 'v1_7' / 'geologia'
LITO_CLASSES = ['vulcanica', 'cristalina', 'sedimentar', 'evaporitica', 'gelo', 'impacto_terras_altas']
MACROSTRAT = 'https://macrostrat.org/api/v2/geologic_units/map?lat={lat}&lng={lon}&scale={scale}'
ESCALAS = ['large', 'medium', 'small', 'tiny']           # da mais detalhada para a mais grossa

# Regras de tradução (ordem importa: a primeira que casar vence). Texto = nome + litologia da unidade.
REGRAS_TERRA = [
    # só unidades que SÃO gelo ("ice", "Phanerozoic ice"); "gravel, sand, ice" é depósito glacial → sedimentar
    ('gelo', r'^(phanerozoic )?ice\b|\| ice$|glacier ice'),
    ('evaporitica', r'evaporit|\bsalt\b|gypsum|halite|playa|salar|saline'),
    ('vulcanica', r'volcan|basalt|lava|andesit|rhyolit|dacit|tuff|ignimbrit|pyroclast|trachyt|extrusive|scoria'),
    ('cristalina', r'granit|intrusive|plutonic|gneiss|schist|metamorph|quartzite|diorit|gabbro|migmatit|'
                   r'granodiorit|crystalline|amphibolit|marble|slate|phyllite|tonalit|serpentin|ultramafic'),
    ('sedimentar', r'sediment|sandstone|shale|clay|silt|conglomerat|alluv|sand\b|gravel|dune|eolian|aeolian|'
                   r'limestone|dolomit|carbonate|mudstone|marl|loess|colluv|till\b|moraine|fluvial|lacustrine|'
                   r'chert|breccia|unconsolidated|surficial|deposit|siliciclastic|clastic|arenite|regolith'),
]


def classificar(texto: str, regras) -> str:
    t = texto.lower()
    for classe, padrao in regras:
        if re.search(padrao, t):
            return classe
    return 'nao_classificado'


def _macrostrat(lat, lon, cache_json):
    if cache_json.is_file():
        return json.loads(cache_json.read_text(encoding='utf-8'))
    resp, falhou = {}, False
    for esc in ESCALAS:
        for tentativa in range(4):
            try:
                url = MACROSTRAT.format(lat=round(lat, 5), lon=round(lon, 5), scale=esc)
                with urllib.request.urlopen(url, timeout=60) as r:
                    resp[esc] = json.loads(r.read())['success']
                break
            except Exception as e:  # noqa: BLE001 — erro do servidor: espera e tenta de novo
                if tentativa == 3:
                    resp[esc] = {'data': [], 'refs': {}, 'erro': f'{type(e).__name__}: {e}'}
                    falhou = True
                time.sleep(2 * (tentativa + 1))
        time.sleep(0.2)
    if not falhou:                                         # só guarda em cache respostas completas
        cache_json.write_text(json.dumps(resp, ensure_ascii=False), encoding='utf-8')
    return resp


def terra():
    """Macrostrat (mapas geológicos compilados; CC-BY 4.0): unidade no centro de cada recorte, na escala mais
    detalhada disponível. Ignora polígonos de água ('inapplicable')."""
    (CACHE / 'macrostrat').mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)
    t = pd.read_csv(C.OUTPUTS / 'v1_6' / 'tabela_completa.csv')
    linhas = []
    for r in t[t.body == 'EARTH'].itertuples():
        resp = _macrostrat(r.lat, r.lon, CACHE / 'macrostrat' / f'{r.tile_id}.json')
        escolha = None
        for esc in ESCALAS:
            for u in resp[esc]['data']:
                txt = f"{u.get('name', '')} {u.get('lith', '')}"
                if u.get('lith', '').lower() in ('', 'inapplicable') and 'ice' not in txt.lower():
                    continue
                escolha = (esc, u, resp[esc]['refs'].get(str(u.get('source_id')), ''))
                break
            if escolha:
                break
        if not escolha:
            linhas.append({'tile_id': r.tile_id, 'site_id': r.site_id, 'status': 'ERRO',
                           'detalhe': 'Macrostrat sem unidade em nenhuma escala'})
            continue
        esc, u, ref = escolha
        txt = f"{u.get('name', '')} | {u.get('lith', '')}"
        linhas.append({'tile_id': r.tile_id, 'site_id': r.site_id, 'status': 'OK',
                       'lito_classe': classificar(txt, REGRAS_TERRA),
                       'geo_unidade': u.get('name') or u.get('lith') or '(sem nome)',
                       'geo_litologia': u.get('lith', ''), 'geo_idade': u.get('best_int_name', ''),
                       'geo_fonte': f'Macrostrat ({esc}): {ref[:120]}'})
    out = pd.DataFrame(linhas)
    out.to_csv(INTER / 'geologia_terra.csv', index=False)
    print(out.status.value_counts().to_dict())
    print(out[out.status == 'OK'].groupby('lito_classe').size().to_dict())
    nc = out[out.lito_classe == 'nao_classificado'] if 'lito_classe' in out else out.iloc[0:0]
    if len(nc):
        print('NÃO CLASSIFICADOS:\n', nc[['tile_id', 'geo_unidade', 'geo_litologia']].to_string(index=False))


MOON_RASTER = (CACHE / 'geologia' / 'moon' / 'Unified_Geologic_Map_of_the_Moon_RASTER' / 'numerical_versions')
MARS_SHP = CACHE / 'geologia' / 'mars' / 'shp' / 'SIM3292_Global_Geology.shp'
# Lua: o mapa unificado agrupa as unidades por origem; crateras e bacias são material de impacto.
REGRAS_LUA = [('impacto_terras_altas', r'crater|basin|terra|plains|massif'), ('vulcanica', r'mare|volcan|dome')]
# Marte, 1º critério: a coluna INTERPRETATION da Descrição das Unidades (DMU) do SIM 3292
# (cache/downloads_manuais/sim3292_dmu.pdf, Tanaka et al. 2014). Regra: o PRIMEIRO tipo de material citado na
# interpretação oficial define a classe. Resumo da interpretação entre parênteses (paráfrase).
DMU_MARTE = {
    'eHt': ('sedimentar', 'movimento de massa, fluvial/lacustre e outros sedimentares; talvez vulcânicas'),
    'HNt': ('impacto_terras_altas', 'brechas de impacto noaquianas, sedimentos e vulcânicas'),
    'Htu': ('sedimentar', 'sedimentos eólicos finos e/ou piroclásticos; sulfatos hidratados'),
    'HNhu': ('sedimentar', 'rochas sedimentares, vulcânicas e de impacto friáveis; sulfatos hidratados'),
    'lNh': ('impacto_terras_altas', 'material de impacto, vulcânico, fluvial e de bacia, indiferenciado'),
    'eHv': ('vulcanica', 'derrames de lava (flood lavas)'),
    'AHi': ('impacto_terras_altas', 'rochas de alvo ejetadas e brechadas; fusão de impacto local'),
}
# 2º critério (unidades fora da tabela): grupo declarado no nome da unidade (UnitDesc).
REGRAS_MARTE = [('vulcanica', r'volcanic'), ('impacto_terras_altas', r'impact|highland'),
                ('gelo', r'polar cap'), ('misto_indefinido', r'.')]


def lua():
    """Unified Geologic Map of the Moon 1:5M (Fortezzo et al. 2020), versão raster numérica 64 px/grau."""
    import rasterio
    INTER.mkdir(parents=True, exist_ok=True)
    lut = pd.read_csv(MOON_RASTER / 'Dn_GeologicUnit_RGBcolor.csv').set_index('DN')
    t = pd.read_csv(C.OUTPUTS / 'v1_6' / 'tabela_completa.csv')
    m = t[t.body == 'MOON']
    with rasterio.open(MOON_RASTER / 'Unified_Geologic_Map_of_the_Moon_64ppd.tif') as d:
        dns = [int(v[0]) for v in d.sample(list(zip(m.lon, m.lat)))]
    linhas = []
    for r, dn in zip(m.itertuples(), dns):
        if dn not in lut.index:
            linhas.append({'tile_id': r.tile_id, 'site_id': r.site_id, 'status': 'ERRO', 'detalhe': f'DN {dn}'})
            continue
        u = lut.loc[dn]
        linhas.append({'tile_id': r.tile_id, 'site_id': r.site_id, 'status': 'OK',
                       'lito_classe': classificar(u.Unit_Name, REGRAS_LUA),
                       'geo_unidade': f'{u.Unit} ({u.Unit_Name})', 'geo_litologia': '', 'geo_idade': u.Unit_Age,
                       'geo_fonte': 'USGS Unified Geologic Map of the Moon 1:5M (Fortezzo et al. 2020)'})
    out = pd.DataFrame(linhas)
    out.to_csv(INTER / 'geologia_lua.csv', index=False)
    print(out.groupby(['lito_classe', 'geo_unidade']).size().to_string())


def marte():
    """Geologic Map of Mars 1:20M (Tanaka et al. 2014, SIM 3292): unidade que contém o centro do recorte."""
    import shapefile
    from shapely.geometry import Point, shape
    from shapely.strtree import STRtree
    INTER.mkdir(parents=True, exist_ok=True)
    rd = shapefile.Reader(str(MARS_SHP))
    geoms, recs = [], []
    for s in rd.iterShapeRecords():
        geoms.append(shape(s.shape.__geo_interface__))
        recs.append(s.record)
    arvore = STRtree(geoms)
    t = pd.read_csv(C.OUTPUTS / 'v1_6' / 'tabela_completa.csv')
    linhas = []
    for r in t[t.body == 'MARS'].itertuples():
        p = Point(r.lon, r.lat)
        hit = [i for i in arvore.query(p) if geoms[i].contains(p)]
        if not hit:
            linhas.append({'tile_id': r.tile_id, 'site_id': r.site_id, 'status': 'ERRO',
                           'detalhe': 'centro fora de qualquer polígono'})
            continue
        rec = recs[hit[0]]
        if rec['Unit'] in DMU_MARTE:
            classe, interp = DMU_MARTE[rec['Unit']]
            criterio = f'interpretação DMU: {interp}'
        else:
            classe, criterio = classificar(rec['UnitDesc'], REGRAS_MARTE), 'grupo no nome da unidade'
        linhas.append({'tile_id': r.tile_id, 'site_id': r.site_id, 'status': 'OK', 'lito_classe': classe,
                       'geo_unidade': f"{rec['Unit']} ({rec['UnitDesc']})", 'geo_litologia': criterio,
                       'geo_idade': '',
                       'geo_fonte': 'USGS Geologic Map of Mars 1:20M, SIM 3292 (Tanaka et al. 2014)'})
    out = pd.DataFrame(linhas)
    out.to_csv(INTER / 'geologia_marte.csv', index=False)
    print(out.groupby(['site_id', 'lito_classe', 'geo_unidade']).size().to_string())


def montar():
    """Junta à v1_6: one-hot das 6 classes (zeus_input) + classe e unidade de origem (tabela completa)."""
    import shutil

    from .esquema import (COMPLETA_COLS_V17, DICIONARIO_COBERTURA, DICIONARIO_GEOLOGIA, DICIONARIO_TEMPERATURA,
                          LITO_ZEUS, ZEUS_COLS_V17, escrever_dicionario, secao_estatisticas, validar)
    out = C.OUTPUTS / 'v1_7'
    t16 = pd.read_csv(C.OUTPUTS / 'v1_6' / 'tabela_completa.csv')
    g = pd.concat([pd.read_csv(INTER / f'geologia_{c}.csv') for c in ('terra', 'lua', 'marte')])
    g = g[g.status == 'OK'].set_index('tile_id')
    linhas, status = [], []
    for _, r in t16.iterrows():
        if r.tile_id not in g.index:
            status.append({'tile_id': r.tile_id, 'site_id': r.site_id, 'status': 'PENDENTE',
                           'detail': 'sem geologia; recorte fora da v1_7', 'protocol': 'v1_7', 'etapa': 'geologia'})
            continue
        x = g.loc[r.tile_id]
        onehot = {f'lito_{c}': float(x.lito_classe == c) for c in LITO_CLASSES}
        linhas.append({**r.to_dict(), **onehot, 'lito_classe': x.lito_classe,
                       'geo_unidade': x.geo_unidade if isinstance(x.geo_unidade, str) else '(sem nome)',
                       'geo_litologia': x.geo_litologia if isinstance(x.geo_litologia, str) else '',
                       'geo_fonte': x.geo_fonte, 'protocol': 'v1_7'})
    completa = pd.DataFrame(linhas)[COMPLETA_COLS_V17]
    zeus = completa[ZEUS_COLS_V17].copy()
    falhas = validar(completa, zeus, COMPLETA_COLS_V17, ZEUS_COLS_V17)
    out.mkdir(parents=True, exist_ok=True)
    completa.to_csv(out / 'tabela_completa.csv', index=False)
    zeus.to_csv(out / 'zeus_input.csv', index=False)
    cl, zl = pd.read_csv(out / 'tabela_completa.csv'), pd.read_csv(out / 'zeus_input.csv')
    falhas += [f'(após releitura) {x}' for x in validar(cl, zl, COMPLETA_COLS_V17, ZEUS_COLS_V17)]
    st = pd.read_csv(C.OUTPUTS / 'v1_6' / 'processing_status.csv')
    if status:
        st = pd.concat([st, pd.DataFrame(status)])
    st.to_csv(out / 'processing_status.csv', index=False)
    notas = [
        'v1_7 = v1_6 (relevo, cobertura, temperatura; valores inalterados) + geologia.',
        'Geologia = classe litológica harmonizada (6 classes) no CENTRO de cada recorte, traduzida de mapas '
        'geológicos de escala regional (Terra ~1:5M ou mais detalhado; Lua 1:5M; Marte 1:20M). É uma '
        'INTERPRETAÇÃO com regras documentadas em src/geologia.py, não uma medida.',
        'No ZEUS entra como one-hot (`lito_*`). Recortes `misto_indefinido` (Marte: unidades de transição/bacia/'
        'planície baixa) ou `nao_classificado` têm todas as colunas `lito_*` = 0: não favorecem nenhum local.',
        'Lua: todas as unidades dos alvos são de cratera ou bacia (impacto); nenhum local da Terra tem essa classe.',
        'Marte: classe pela interpretação oficial da Descrição das Unidades (DMU) do SIM 3292, regra "primeiro '
        'material citado"; unidades fora da tabela usam o grupo declarado no nome.',
    ]
    escrever_dicionario(out / 'dicionario_colunas.md', 'v1_7', notas, ZEUS_COLS_V17,
                        DICIONARIO_COBERTURA + DICIONARIO_TEMPERATURA + DICIONARIO_GEOLOGIA)
    rel = ['# Relatório de qualidade — protocolo `v1_7`', '', '## Validações obrigatórias', '',
           '- ' + ('**OK** — esquema, `zeus_input` numérico sem NaN, mesma contagem e ordem, body/tipo válidos, '
                   '`tile_id` único, lat/lon nos limites.' if not falhas else '**FALHAS:** ' + '; '.join(falhas)),
           f'- Linhas: {len(cl)} (v1_6: {len(t16)}). Por corpo: ' +
           ', '.join(f'{b}={n}' for b, n in cl.body.value_counts().items()) + '.', '',
           '## Classes por corpo (recortes)', '',
           pd.crosstab(cl.lito_classe, cl.body).to_markdown(), '',
           '## Classe predominante por local', '',
           cl.groupby(['body', 'site_name']).agg(classe=('lito_classe', lambda s: s.value_counts().index[0]),
                                                  fracao=('lito_classe', lambda s: s.value_counts().iloc[0] / len(s)),
                                                  unidade=('geo_unidade', lambda s: str(s.fillna('(sem nome)').value_counts().index[0])[:60]))
           .round(2).reset_index().to_markdown(index=False), '']
    rel += secao_estatisticas(cl)
    (out / 'relatorio_qualidade.md').write_text('\n'.join(rel) + '\n', encoding='utf-8')
    if not falhas:
        ent = C.BASE / 'entrega_zeus'
        for nome in ('zeus_input.csv', 'tabela_completa.csv', 'dicionario_colunas.md'):
            shutil.copy2(out / nome, ent / nome)
    print('Linhas:', len(cl), cl.body.value_counts().to_dict(), '| pendentes:', len(status),
          '| validações:', 'OK' if not falhas else falhas)


if __name__ == '__main__':
    {'terra': terra, 'lua': lua, 'marte': marte, 'montar': montar}[sys.argv[1]]()

"""Camada de clima Marte × Terra (contribuição de Luís Gustavo de Oliveira Miranda, integrada em 2026-11-15).

Reimplementa o método de `nasa/final/code/similaridade_marte_terra.py` (pasta Feitos_de_outros_integrantes/):
similaridade de Gower entre cada local da Terra (Meteomatics, 1 ano diário) e células de 2° do modelo climático
global de Marte da NASA Ames (Beta Output Release 1, doi 10.25966/rjgg-r639).

    s_k = 1 - |x_k(Terra) - y_k(Marte)| / R_k     (R_k = amplitude no conjunto Terra (507 pontos) + Marte)
    S   = soma(w_k s_k) / soma(w_k)

Nove grandezas; pressão em log10 e precipitação em log(1+x); pesos 0,5 nas seis térmicas (ar e superfície
contam uma vez cada dimensão física) — a configuração "pesos corrigidos" do relatório do Luís.

Diferenças em relação ao original (decisões nossas, documentadas):
1. Aerossol da Terra = `dust_aod_550nm` (só poeira mineral), não `total_aod_550nm` (inclui poluição/fumaça).
   É a correção que o próprio relatório recomenda. `--aod total` reproduz o original (usado no teste).
2. Em vez dos 3 sítios fixos do original, calculamos para os NOSSOS 6 alvos de Marte (entrada/alvos_v2.csv):
   a célula do modelo mais próxima do centro de cada alvo.
3. Só os 43 locais nomeados vão para o site; a grade global de 5° entra apenas no cálculo das amplitudes R_k
   (para os valores baterem com o original).

Entradas (copiadas dos zips do Luís para cache/clima_luis/ por `--extrair`):
  marte_global_por_ponto.csv, marte_ciclo_diurno_por_ponto.csv, terra_grade_por_local.csv, terra_grade_diario.csv

Saídas em outputs/<protocolo>/clima/:
  clima_marte_por_alvo.csv   alvo × local: similaridade climática, posição, similaridade por grandeza
  clima_marte_resumo.json    validação (AUC análogos × controles), Spearman com o nosso score, teste de reprodução

Uso:
  python -m src.clima_marte --extrair      # uma vez: copia as entradas dos zips
  python -m src.clima_marte                # calcula
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from .config import ALVOS_CSV, BASE, OUTPUTS

CACHE = BASE / 'cache' / 'clima_luis'
PASTA_ZIPS = BASE / 'Feitos_de_outros_integrantes'
ARQS = ['marte_global_por_ponto.csv', 'marte_ciclo_diurno_por_ponto.csv',
        'terra_grade_por_local.csv', 'terra_grade_diario.csv']
REF_ORIGINAL = 'sim_pesos_terra.csv'   # resultado do Luís (pesos corrigidos, AOD total) para o teste

# grandeza -> (rótulo, transformação, peso)
VARS = {
    'temp_ar': ('Temperatura média do ar', None, 0.5),
    'amp_sazonal_ar': ('Variação sazonal do ar', None, 0.5),
    'amp_diurna_ar': ('Amplitude diária do ar', None, 0.5),
    'temp_sup': ('Temperatura média da superfície', None, 0.5),
    'amp_sazonal_sup': ('Variação sazonal da superfície', None, 0.5),
    'amp_diurna_sup': ('Amplitude diária da superfície', None, 0.5),
    'pressao': ('Pressão', np.log10, 1.0),
    'precip': ('Precipitação', np.log1p, 1.0),
    'poeira': ('Poeira na atmosfera', None, 1.0),
}


def extrair():
    CACHE.mkdir(parents=True, exist_ok=True)
    quero = {f'nasa/final/dados_entrada/{a}' for a in ARQS} | {f'nasa/final/similaridade_semPeso/{REF_ORIGINAL}'}
    achados = set()
    for z in sorted(PASTA_ZIPS.glob('nasa-*.zip')):
        with zipfile.ZipFile(z) as f:
            for i in f.infolist():
                if i.filename in quero:
                    (CACHE / Path(i.filename).name).write_bytes(f.read(i))
                    achados.add(Path(i.filename).name)
    faltam = set(ARQS + [REF_ORIGINAL]) - achados
    print('extraídos:', sorted(achados), '| faltam:', sorted(faltam) or 'nada')


def amp_sazonal(diario: pd.DataFrame, col: str) -> pd.Series:
    """Máx − mín, no ano, da média móvel de 5 dias (equivale às médias de 5 sóis de Marte)."""
    d = diario.dropna(subset=[col]).sort_values(['local', 'data'])
    roll = d.groupby('local')[col].transform(lambda s: s.rolling(5, center=True, min_periods=5).mean())
    g = roll.groupby(d['local'])
    return g.max() - g.min()


def carregar_terra(aod: str) -> pd.DataFrame:
    b = pd.read_csv(CACHE / 'terra_grade_por_local.csv')
    dia = pd.read_csv(CACHE / 'terra_grade_diario.csv', usecols=['local', 'data', 't_mean_2m_24h_K', 't_mean_0m_24h_K'])
    E = b[['local', 'tipo', 'lat', 'lon']].copy()
    E['temp_ar'] = b['t_mean_2m_24h_K_mean']
    E['amp_sazonal_ar'] = E['local'].map(amp_sazonal(dia, 't_mean_2m_24h_K'))
    E['amp_diurna_ar'] = b['amplitude_termica_diaria_media']
    E['temp_sup'] = b['t_mean_0m_24h_K_mean']
    E['amp_sazonal_sup'] = E['local'].map(amp_sazonal(dia, 't_mean_0m_24h_K'))
    E['amp_diurna_sup'] = b['amplitude_superficie_diaria_media']
    E['pressao'] = b['sfc_pressure_mean_24h_Pa_mean']
    E['precip'] = b['precip_24h_mm_mean']
    E['poeira'] = b[f'{aod}_aod_550nm_idx_mean']
    return E


def carregar_marte() -> pd.DataFrame:
    m = pd.read_csv(CACHE / 'marte_global_por_ponto.csv')
    d = pd.read_csv(CACHE / 'marte_ciclo_diurno_por_ponto.csv')
    assert len(d) == len(m) and np.allclose(d['lat'], m['lat']) and np.allclose(d['lon_leste'], m['lon_leste'])
    M = m[['lat', 'lon_leste', 'lon_180']].copy()
    M['temp_ar'] = m['temp_ar_K_media']
    M['amp_sazonal_ar'] = m['temp_ar_K_max'] - m['temp_ar_K_min']
    M['amp_diurna_ar'] = d['amp_diurna_temp_ar_K_media']
    M['temp_sup'] = m['temp_superficie_K_media']
    M['amp_sazonal_sup'] = m['temp_superficie_K_max'] - m['temp_superficie_K_min']
    M['amp_diurna_sup'] = d['amp_diurna_temp_superficie_K_media']
    M['pressao'] = m['pressao_Pa_media']
    M['precip'] = 0.0                     # não chove em Marte
    M['poeira'] = m['poeira_opacidade_vis_media']
    return M.dropna().reset_index(drop=True)


def _t(df, v):
    f = VARS[v][1]
    x = df[v].astype(float).to_numpy()
    return f(x) if f else x


def amplitudes(E, M):
    return {v: float(np.ptp(np.concatenate([_t(E, v), _t(M, v)]))) or 1.0 for v in VARS}


def sim_por_grandeza(E, celula: pd.Series, R) -> pd.DataFrame:
    """Similaridade de cada local da Terra com UMA célula de Marte, por grandeza e total."""
    out = pd.DataFrame(index=E.index)
    cel = celula.to_frame().T
    for v in VARS:
        out['s_' + v] = 1.0 - np.abs(_t(E, v) - _t(cel, v)[0]) / R[v]
    w = np.array([VARS[v][2] for v in VARS])
    out['sim_clima'] = out[['s_' + v for v in VARS]].to_numpy() @ w / w.sum()
    return out


def celula_mais_proxima(M, lat, lon):
    lon_e = lon % 360
    dlon = np.abs(((M['lon_leste'].to_numpy() - lon_e) + 180) % 360 - 180)
    # distância angular aproximada (célula de 2°: suficiente para achar a vizinha)
    d = np.hypot(M['lat'].to_numpy() - lat, dlon * np.cos(np.deg2rad(lat)))
    return int(np.argmin(d))


def melhor_celula(E, M, R):
    """Para cada local: maior S entre todas as células de Marte (indicador 'Marte em geral' do relatório)."""
    w = {v: VARS[v][2] for v in VARS}
    num = np.zeros((len(E), len(M)), dtype=np.float32)
    for v in VARS:
        num += (w[v] * (1.0 - np.abs(_t(E, v)[:, None] - _t(M, v)[None, :]) / R[v])).astype(np.float32)
    return num.max(axis=1) / sum(w.values())


def teste_reproducao():
    """Com AOD total e os 3 sítios do original, os valores têm de bater com sim_pesos_terra.csv do Luís."""
    ref_p = CACHE / REF_ORIGINAL
    if not ref_p.is_file():
        return {'executado': False, 'motivo': 'arquivo de referência ausente'}
    E, M = carregar_terra('total'), carregar_marte()
    R = amplitudes(E, M)
    ref = pd.read_csv(ref_p).set_index('local')
    sitios = {'Jezero': (19, 77), 'Gale': (-5, 137), 'Elysium': (5, 135)}  # células citadas no relatório
    dif = {}
    for nome, (la, lo) in sitios.items():
        j = np.flatnonzero((M['lat'].round() == la) & (M['lon_leste'].round() == lo))
        if not j.size:
            dif[nome] = None
            continue
        s = sim_por_grandeza(E, M.iloc[j[0]], R)['sim_clima']
        s.index = E['local']
        dif[nome] = float(np.nanmax(np.abs(s - ref['sim_' + nome].reindex(s.index))))
    return {'executado': True, 'max_dif_abs_por_sitio': dif}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--extrair', action='store_true')
    ap.add_argument('--aod', choices=['dust', 'total'], default='dust')
    ap.add_argument('--protocolo', default='v1_7')
    a = ap.parse_args()
    if a.extrair:
        extrair()
        return
    faltam = [x for x in ARQS if not (CACHE / x).is_file()]
    if faltam:
        raise SystemExit(f'faltam entradas em {CACHE}: {faltam}. Rode: python -m src.clima_marte --extrair')

    E, M = carregar_terra(a.aod), carregar_marte()
    R = amplitudes(E, M)
    nomeados = E['tipo'] != 'grade'
    geral = pd.Series(melhor_celula(E, M, R), index=E.index)

    rank = pd.read_csv(OUTPUTS / a.protocolo / 'similaridade' / 'ranking_por_alvo.csv')
    nome_id = rank.drop_duplicates('site_name').set_index('site_name')['site_id']
    alvos = pd.read_csv(ALVOS_CSV)
    alvos = alvos[alvos['corpo'] == 'MARS']

    linhas, celulas = [], {}
    for _, al in alvos.iterrows():
        j = celula_mais_proxima(M, al['lat_centro'], al['lon_centro'])
        c = M.iloc[j]
        celulas[al['id']] = {'lat': float(c['lat']), 'lon_leste': float(c['lon_leste']),
                             **{v: round(float(c[v]), 4) for v in VARS}}
        s = sim_por_grandeza(E, c, R)
        s['posicao_global'] = s['sim_clima'].rank(ascending=False, method='min').astype(int)  # entre os 507
        brutos = E[list(VARS)].add_prefix('x_')            # valores físicos da Terra (sem transformação)
        d = pd.concat([E[['local', 'tipo', 'lat', 'lon']], s, brutos], axis=1)[nomeados].copy()
        d['posicao'] = d['sim_clima'].rank(ascending=False, method='min').astype(int)          # entre os 43
        d.insert(0, 'alvo', al['id'])
        linhas.append(d)
    T = pd.concat(linhas, ignore_index=True)
    T['site_id'] = T['local'].map(nome_id)
    T['sim_clima_marte_geral'] = T['local'].map(pd.Series(geral[nomeados].values, index=E.loc[nomeados, 'local']))
    sem_id = sorted(T.loc[T['site_id'].isna(), 'local'].unique())

    # validação
    from scipy.stats import spearmanr
    from sklearn.metrics import roc_auc_score
    val = {}
    for alvo, d in T.groupby('alvo'):
        y = (d['tipo'] == 'analogo').astype(int)
        m = d.merge(rank[rank['alvo'] == alvo][['site_id', 'score']], on='site_id')
        cand = m[m['tipo'] != 'controle']
        val[alvo] = {'auc_analogo_x_controle': round(float(roc_auc_score(y, d['sim_clima'])), 3),
                     'spearman_com_score_v1_7': round(float(spearmanr(m['score'], m['sim_clima'])[0]), 3),
                     'spearman_so_candidatos': round(float(spearmanr(cand['score'], cand['sim_clima'])[0]), 3),
                     'top5': d.nsmallest(5, 'posicao')['local'].tolist()}
    resumo = {
        'fonte': 'Luís Gustavo de Oliveira Miranda — Análogos climáticos de Marte na Terra (2026-11-14)',
        'metodo': 'Gower, 9 grandezas, pesos 0,5 nas 6 térmicas; pressão log10; precipitação log(1+x)',
        'aerossol_terra': f'{a.aod}_aod_550nm', 'n_terra_total': int(len(E)), 'n_nomeados': int(nomeados.sum()),
        'n_celulas_marte': int(len(M)), 'amplitudes_R': {k: round(v, 4) for k, v in R.items()},
        'celula_por_alvo': celulas, 'validacao': val, 'locais_sem_site_id': sem_id,
        'teste_reproducao_aod_total': teste_reproducao(),
    }
    out = OUTPUTS / a.protocolo / 'clima'
    out.mkdir(parents=True, exist_ok=True)
    T.round(4).to_csv(out / 'clima_marte_por_alvo.csv', index=False)
    (out / 'clima_marte_resumo.json').write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: resumo[k] for k in ('validacao', 'locais_sem_site_id', 'teste_reproducao_aod_total')},
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()

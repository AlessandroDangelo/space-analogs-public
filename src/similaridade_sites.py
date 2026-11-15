"""Similaridade entre locais da Terra e alvos da Lua/Marte (para ranking e para o site).

Uso:  python -m src.similaridade_sites [--protocolo v1_5]
Gera outputs/<protocolo>/similaridade/:
    ranking_por_alvo.csv    cada alvo (Lua/Marte) × cada local da Terra: distâncias, score, posição, co-cluster ZEUS
    ranking_por_corpo.csv   o mesmo agregando todos os alvos de um corpo (MOON, MARS)
    contribuicoes.csv       por par alvo×local: diferença padronizada de cada feature no par de recortes mais parecido
    resumo.md               top 10 por corpo e por alvo, e checagem com os locais de controle

Método (explicável):
1. Distância entre dois recortes com PESO IGUAL POR GRUPO (relevo, cobertura, temperatura, geologia):
   - grupos numéricos: log1p → z-score sobre todas as linhas; distância do grupo = RMS das diferenças
     padronizadas (em "desvios-padrão");
   - geologia (one-hot): diferença direta, sem z-score (para classes raras não pesarem mais):
     0 = mesma classe, 0,5 = uma das duas indefinida, 1 = classes diferentes;
   - distância total = raiz da média dos quadrados das distâncias dos grupos presentes (cada grupo pesa 1/n).
   Assim, ter 6 colunas de geologia não dá à geologia mais peso que às 2 de temperatura.
2. Distância alvo→local: para cada recorte do alvo, a distância ao recorte MAIS parecido do local; depois a mediana
   sobre os recortes do alvo. (Um local é análogo se tem algum terreno parecido com cada parte do alvo.)
3. Score 0–100: 100 / (1 + d / d50), onde d50 é a mediana de todas as distâncias alvo→local da Terra. Score 50 =
   parecido como um par típico; 100 = idêntico. É uma escala de leitura, não uma probabilidade.
4. Complementar: mesma agregação no embedding do ZEUS (`dist_zeus`) e fração dos recortes do alvo que caem num
   cluster ZEUS que contém algum recorte do local (`cocluster_k*`).
Os controles (cidades/floresta) entram no ranking de propósito: se aparecerem no topo, as features não bastam.
"""
from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

from . import config as C
from .esquema import COBERTURA_ZEUS, LITO_ZEUS, TEMP_ZEUS, ZEUS_COLS

GRUPOS = [('terreno', ZEUS_COLS), ('cobertura', COBERTURA_ZEUS), ('temperatura', TEMP_ZEUS),
          ('geologia', LITO_ZEUS)]


def zscore_log(M: np.ndarray) -> np.ndarray:
    X = np.log1p(M)
    sd = X.std(axis=0)
    sd[sd == 0] = 1.0
    return (X - X.mean(axis=0)) / sd


def espaco_features(z: pd.DataFrame):
    """Retorna (X para contribuições por feature, lista de grupos [(nome, colunas, matriz, é_categórico)])."""
    grupos = []
    for nome, cols in GRUPOS:
        presentes = [c for c in cols if c in z.columns]
        if not presentes:
            continue
        cat = nome == 'geologia'
        M = z[presentes].to_numpy(float) if cat else zscore_log(z[presentes].to_numpy(float))
        grupos.append((nome, presentes, M, cat))
    X = np.hstack([g[2] for g in grupos])
    return X, grupos


def dist_alvo_local(grupos, ia, ie):
    """Distância alvo→local com peso igual por grupo. Retorna (d, par mais parecido, {grupo: distância})."""
    Dg = {}
    for nome, _cols, M, cat in grupos:
        if cat:
            Dg[nome] = cdist(M[ia], M[ie], 'cityblock') / 2.0
        else:
            Dg[nome] = cdist(M[ia], M[ie]) / np.sqrt(M.shape[1])
    D = np.sqrt(np.mean([d ** 2 for d in Dg.values()], axis=0))
    melhor = D.argmin(axis=1)                              # recorte do local mais parecido com cada recorte do alvo
    linhas = np.arange(len(ia))
    por_grupo = {g: float(np.median(d[linhas, melhor])) for g, d in Dg.items()}
    return float(np.median(D[linhas, melhor])), np.unravel_index(np.argmin(D), D.shape), por_grupo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--protocolo', default='v1_7')
    a = ap.parse_args()
    base = C.OUTPUTS / a.protocolo
    out = base / 'similaridade'
    out.mkdir(parents=True, exist_ok=True)
    tab = pd.read_csv(base / 'tabela_completa.csv')
    z = pd.read_csv(base / 'zeus_input.csv')
    X, grupos = espaco_features(z)
    cols = [c for g in grupos for c in g[1]]
    zdir = base / 'zeus'
    emb = pd.read_csv(zdir / 'embeddings_zeus.csv') if (zdir / 'embeddings_zeus.csv').is_file() else None
    clus = pd.read_csv(zdir / 'clusters_zeus.csv') if (zdir / 'clusters_zeus.csv').is_file() else None
    if emb is not None:
        assert (emb.tile_id.values == tab.tile_id.values).all()
        E = emb.drop(columns='tile_id').to_numpy(float)
    if clus is not None:
        assert (clus.tile_id.values == tab.tile_id.values).all()
    kcols = [c for c in clus.columns if c.startswith('cluster_k')] if clus is not None else []

    idx = {s: g.index.to_numpy() for s, g in tab.groupby('site_id', sort=False)}
    info = tab.groupby('site_id', sort=False).agg(site_name=('site_name', 'first'), body=('body', 'first'),
                                                  tipo=('tipo', 'first'))
    terra = [s for s in idx if info.loc[s, 'body'] == 'EARTH']
    alvos = [s for s in idx if info.loc[s, 'body'] != 'EARTH']

    def pares(grupos_alvo):
        linhas, contrib = [], []
        for nome_alvo, ia in grupos_alvo:
            for s in terra:
                ie = idx[s]
                d, (pa, pe), por_grupo = dist_alvo_local(grupos, ia, ie)
                lin = {'alvo': nome_alvo, 'site_id': s, 'site_name': info.loc[s, 'site_name'],
                       'tipo': info.loc[s, 'tipo'], 'dist_features': d,
                       **{f'dist_{g}': v for g, v in por_grupo.items()},
                       'recorte_alvo_mais_parecido': tab.tile_id[ia[pa]],
                       'recorte_terra_mais_parecido': tab.tile_id[ie[pe]]}
                if emb is not None:
                    lin['dist_zeus'] = float(np.median(cdist(E[ia], E[ie]).min(axis=1)))
                for kc in kcols:
                    ce = set(clus.loc[ie, kc])
                    lin[f'cocluster_{kc[8:]}'] = float(np.mean([c in ce for c in clus.loc[ia, kc]]))
                linhas.append(lin)
                dz = X[ia[pa]] - X[ie[pe]]
                contrib.append({'alvo': nome_alvo, 'site_id': s, **{f'dz_{c}': float(v) for c, v in zip(cols, dz)}})
        return pd.DataFrame(linhas), pd.DataFrame(contrib)

    por_alvo, contrib = pares([(s, idx[s]) for s in alvos])
    por_corpo, _ = pares([(b, np.concatenate([idx[s] for s in alvos if info.loc[s, 'body'] == b]))
                          for b in ('MOON', 'MARS')])
    d50 = por_alvo.dist_features.median()
    ordem_alvo = {a_: i for i, a_ in enumerate(dict.fromkeys(list(por_alvo.alvo) + list(por_corpo.alvo)))}

    def ordenar(df):
        df = df.assign(score=100.0 / (1.0 + df.dist_features / d50), _o=df.alvo.map(ordem_alvo))
        df = df.sort_values(['_o', 'dist_features']).drop(columns='_o').reset_index(drop=True)
        df['posicao'] = df.groupby('alvo').cumcount() + 1
        m = df.tipo != 'controle'
        df['posicao_sem_controles'] = np.nan
        df.loc[m, 'posicao_sem_controles'] = df[m].groupby('alvo').cumcount() + 1
        return df

    por_alvo, por_corpo = ordenar(por_alvo), ordenar(por_corpo)

    # Versão alternativa (peso igual por COLUNA, todas com log1p+z-score), só para o teste de robustez.
    Xc = zscore_log(z.to_numpy(float))
    alt = []
    for b in ('MOON', 'MARS'):
        ia = np.concatenate([idx[s] for s in alvos if info.loc[s, 'body'] == b])
        for s in terra:
            D = cdist(Xc[ia], Xc[idx[s]]) / np.sqrt(Xc.shape[1])
            alt.append({'alvo': b, 'site_id': s, 'tipo': info.loc[s, 'tipo'],
                        'dist_features': float(np.median(D.min(axis=1)))})
    pd.DataFrame(alt).to_csv(out / 'ranking_por_corpo_peso_por_coluna.csv', index=False, float_format='%.4f')
    por_alvo.to_csv(out / 'ranking_por_alvo.csv', index=False, float_format='%.4f')
    por_corpo.to_csv(out / 'ranking_por_corpo.csv', index=False, float_format='%.4f')
    contrib.to_csv(out / 'contribuicoes.csv', index=False, float_format='%.4f')

    # ---------------- resumo legível
    cols_dg = [f'dist_{g[0]}' for g in grupos]
    cols_show = ['posicao', 'site_name', 'tipo', 'score', 'dist_features'] + cols_dg + \
                (['dist_zeus'] if emb is not None else [])
    r = [f'# Similaridade Terra × Lua/Marte — protocolo `{a.protocolo}`', '',
         f'Grupos (peso igual): ' + '; '.join(f'**{g[0]}** ({", ".join(g[1])})' for g in grupos) + '.', '',
         f'Distância total = √(média dos quadrados das distâncias dos grupos); d50 = {d50:.3f}; '
         'score = 100/(1 + d/d50). `dist_<grupo>`: quanto cada grupo afasta o local do alvo (0 = igual).', '']
    for corpo in ('MOON', 'MARS'):
        g = por_corpo[por_corpo.alvo == corpo]
        r += [f'## {corpo}: 10 locais da Terra mais parecidos (todos os alvos do corpo juntos)', '',
              g.head(10)[cols_show].round(3).to_markdown(index=False), '']
        ctrl = g[g.tipo == 'controle']
        r += [f'Controles (cidades/floresta) neste ranking: posições {", ".join(map(str, ctrl.posicao))} '
              f'de {len(g)}.', '']
    r += ['## Top 3 por alvo', '']
    for alvo, g in por_alvo.groupby('alvo', sort=False):
        top = ', '.join(f'{x.site_name} ({x.score:.0f})' for x in g.head(3).itertuples())
        r += [f'- **{info.loc[alvo, "site_name"]}** ({info.loc[alvo, "body"]}): {top}']
    r += ['', '## Limitações', '',
          '- Similaridade usa relevo, cobertura, temperatura da superfície e geologia (classe harmonizada).',
          '- Peso igual por grupo (relevo, cobertura, temperatura, geologia). O ZEUS (clusters, dist_zeus) continua '
          'recebendo todas as colunas sem peso: é um modelo pré-treinado.',
          '- Geologia só diferencia alvos com classe existente na Terra (em Marte, só Gusev, vulcânico).',
          '- Piso de ruído do NASADEM: locais planos da Terra parecem mais inclinados/rugosos do que são.',
          '- O score é uma escala relativa a este conjunto de locais; muda se os locais mudarem.']
    (out / 'resumo.md').write_text('\n'.join(r) + '\n', encoding='utf-8')
    print((out / 'resumo.md').read_text(encoding='utf-8')[:3000])


if __name__ == '__main__':
    main()

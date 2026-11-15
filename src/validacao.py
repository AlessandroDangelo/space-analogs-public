"""Validação do ranking de similaridade.

Uso:  python -m src.validacao [--protocolo v1_7]
Gera outputs/<protocolo>/validacao/validacao.md e .csv

Testes
1. Candidatos × controles (interno): probabilidade de um local candidato ter score maior que um controle
   (cidade/floresta), por corpo. É a AUC (0,5 = acaso; 1 = separa sempre).
2. Lista publicada (externo): posição, no ranking de cada corpo, dos locais citados como análogos daquele corpo em
   `entrada/analogos_publicados.csv` (cada linha cita a fonte). AUC publicados × demais candidatos.
   Com poucos locais publicados, o teste é indicativo, não estatisticamente forte.
3. Robustez: correlação de Spearman entre o ranking atual (peso igual por grupo) e (a) o ranking com peso igual
   por coluna, (b) o ranking pela distância no embedding do ZEUS. Correlação alta = conclusão não depende da
   escolha de pesos/método.
"""
from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

from . import config as C


def auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) == 0 or len(neg) == 0:
        return np.nan, np.nan
    u, p = mannwhitneyu(pos, neg, alternative='greater')
    return u / (len(pos) * len(neg)), p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--protocolo', default='v1_7')
    a = ap.parse_args()
    sim = C.OUTPUTS / a.protocolo / 'similaridade'
    out = C.OUTPUTS / a.protocolo / 'validacao'
    out.mkdir(parents=True, exist_ok=True)
    rk = pd.read_csv(sim / 'ranking_por_corpo.csv')
    pub_path = C.ENTRADA / 'analogos_publicados_v2.csv'
    if not pub_path.is_file():
        pub_path = C.ENTRADA / 'analogos_publicados.csv'
    pub = pd.read_csv(pub_path).drop_duplicates(['site_id', 'corpo']) if pub_path.is_file() else pd.DataFrame(columns=['site_id', 'corpo'])

    linhas, r = [], [f'# Validação do ranking — protocolo `{a.protocolo}`', '']
    r += ['## 1. Candidatos × controles', '',
          'AUC = probabilidade de um candidato ter score maior que um controle (0,5 = acaso, 1 = perfeito).', '',
          '| corpo | candidatos | controles | AUC | p (Mann-Whitney, unilateral) | posições dos controles |',
          '|---|---|---|---|---|---|']
    for corpo in ('MOON', 'MARS'):
        g = rk[rk.alvo == corpo]
        cand, ctrl = g[g.tipo == 'candidato'], g[g.tipo == 'controle']
        v, p = auc(cand.score, ctrl.score)
        linhas.append({'teste': 'candidatos_vs_controles', 'corpo': corpo, 'auc': v, 'p': p})
        r += [f'| {corpo} | {len(cand)} | {len(ctrl)} | {v:.3f} | {p:.4f} | {sorted(ctrl.posicao.tolist())} |']

    r += ['', '## 2. Análogos publicados', '',
          f'Fonte: `{pub_path.relative_to(C.BASE)}` ({len(pub)} pares local×corpo). Cada linha cita a publicação.', '']
    for corpo in ('MOON', 'MARS'):
        g = rk[(rk.alvo == corpo) & (rk.tipo == 'candidato')]
        ids = set(pub[pub.corpo == corpo].site_id)
        pos = g[g.site_id.isin(ids)]
        if pos.empty:
            r += [f'- **{corpo}:** nenhuma entrada publicada verificada ainda; teste não realizado.']
            continue
        v, p = auc(pos.score, g[~g.site_id.isin(ids)].score)
        linhas.append({'teste': 'publicados_vs_demais', 'corpo': corpo, 'auc': v, 'p': p, 'n': len(pos)})
        lista = ', '.join(f'{x.site_name} ({int(x.posicao_sem_controles)}º de {len(g)})' for x in pos.itertuples())
        r += [f'- **{corpo}:** {lista}. AUC publicados × demais candidatos = {v:.3f} (p = {p:.3f}, n = {len(pos)}).']
    r += ['', 'Estar fora da lista não significa não ser análogo (o catálogo tem 30 locais). Locais do catálogo '
          'citados por astrobiologia ou mineralogia não são capturados pelas nossas features. A lista de candidatos '
          'já é feita de análogos conhecidos (viés de seleção), então o teste mede a ORDEM dentro dela.', '']

    r += ['## 3. Robustez à escolha de pesos e de método', '',
          '| corpo | comparação | Spearman ρ | top 10 em comum |', '|---|---|---|---|']
    alt = sim / 'ranking_por_corpo_peso_por_coluna.csv'
    for corpo in ('MOON', 'MARS'):
        g = rk[rk.alvo == corpo].set_index('site_id')
        comps = []
        if alt.is_file():
            h = pd.read_csv(alt)
            comps.append(('peso por grupo × peso por coluna', h[h.alvo == corpo].set_index('site_id').dist_features))
        if 'dist_zeus' in g:
            comps.append(('distância nas features × distância no ZEUS', g.dist_zeus))
        for nome, outra in comps:
            comum = g.index.intersection(outra.index)
            rho = spearmanr(g.loc[comum, 'dist_features'], outra.loc[comum]).statistic
            top_a = set(g.loc[comum].sort_values('dist_features').head(10).index)
            top_b = set(outra.loc[comum].sort_values().head(10).index)
            linhas.append({'teste': nome, 'corpo': corpo, 'spearman': rho, 'top10_comum': len(top_a & top_b)})
            r += [f'| {corpo} | {nome} | {rho:.3f} | {len(top_a & top_b)}/10 |']
    r += ['', '## Leitura', '',
          '- Teste 1 mostra se as features separam análogos de lugares comuns (cidades, floresta).',
          '- Teste 2 é a comparação com a literatura; hoje limitado pelo acesso às listas publicadas.',
          '- Teste 3 mostra se a conclusão depende de decisões nossas (pesos) ou do método (features × ZEUS).']
    pd.DataFrame(linhas).to_csv(out / 'validacao.csv', index=False)
    (out / 'validacao.md').write_text('\n'.join(r) + '\n', encoding='utf-8')
    print('\n'.join(r))


if __name__ == '__main__':
    main()

"""Analisa clusters_zeus.csv junto com tabela_completa.csv.

Uso (de dentro da pasta entrega_zeus/):
    python analisar_clusters.py

Gera:
    analise_clusters.md        relatório legível (composição por corpo, análogos, sanidade)
    analogos_por_k.csv         para cada k, cada recorte da Terra que divide cluster com Lua/Marte
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

AQUI = Path(__file__).resolve().parent


def md(df: pd.DataFrame, index=True) -> str:
    try:
        return df.to_markdown(index=index)
    except ImportError:  # tabulate ausente
        return '```\n' + df.to_string(index=index) + '\n```'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--clusters', default=AQUI / 'clusters_zeus.csv', type=Path)
    ap.add_argument('--tabela', default=AQUI / 'tabela_completa.csv', type=Path)
    ap.add_argument('--qualidade', default=AQUI / 'qualidade_k.csv', type=Path)
    ap.add_argument('--saida', default=AQUI / 'analise_clusters.md', type=Path)
    a = ap.parse_args()

    cl = pd.read_csv(a.clusters)
    tab = pd.read_csv(a.tabela)
    if len(cl) != len(tab) or not (cl.tile_id.values == tab.tile_id.values).all():
        raise SystemExit('clusters_zeus.csv e tabela_completa.csv não têm os mesmos tile_id na mesma ordem.')
    df = tab.merge(cl, on='tile_id', validate='one_to_one')
    kcols = [c for c in cl.columns if c.startswith('cluster_k')]
    multi = df.site_id.duplicated(keep=False).any()

    out = ['# Análise dos clusters ZEUS', '',
           f'{len(df)} recortes: ' + ', '.join(f'{b}={n}' for b, n in df.body.value_counts().items()) +
           f' | protocolo: {", ".join(sorted(df.protocol.unique()))}', '']
    if a.qualidade.is_file():
        out += ['## Qualidade por k', '',
                '`silhueta_embedding`: separação dos clusters no espaço do ZEUS (-1 a 1, maior = melhor). '
                '`ari_medio_entre_sementes`: 1 = o K-Means dá o mesmo resultado com sementes diferentes.', '',
                md(pd.read_csv(a.qualidade), index=False), '']

    # Sanidade: recortes do mesmo local devem cair juntos.
    out += ['## Checagem de sanidade: recortes do mesmo local', '']
    if not multi:
        out += ['Cada local tem só 1 recorte nesta tabela, então a checagem por `site_id` não se aplica '
                '(ARI com `site_id` é ~0 por construção). Ela passa a valer com a grade 3×3 da V1.4.', '']
    else:
        linhas = []
        for c in kcols:
            ari = adjusted_rand_score(df.site_id, df[c])
            juntos = df.groupby('site_id')[c].nunique().eq(1)
            linhas.append({'k': int(c[9:]), 'ARI_vs_site_id': round(ari, 3),
                           'locais_com_todos_recortes_no_mesmo_cluster': f'{juntos.sum()}/{len(juntos)}'})
        out += ['ARI entre cluster e `site_id`. Com k pequeno e muitos locais o ARI é naturalmente baixo; '
                'a coluna de locais "inteiros" é a leitura mais direta.', '',
                md(pd.DataFrame(linhas), index=False), '']

    analogos = []
    for c in kcols:
        k = int(c[9:])
        out += [f'## k = {k}', '']
        comp = pd.crosstab(df[c], df.body).rename_axis(index='cluster', columns=None)
        out += ['Composição por corpo:', '', md(comp), '']
        for cid in sorted(df[c].unique()):
            g = df[df[c] == cid]
            alvos = g[g.body != 'EARTH']
            if alvos.empty:
                continue
            terra = g[g.body == 'EARTH']
            for _, t in terra.iterrows():
                analogos.append({'k': k, 'cluster': cid, 'tile_id': t.tile_id, 'site_id': t.site_id,
                                 'site_name': t.site_name, 'tipo': t.tipo,
                                 'divide_com_MOON': ';'.join(alvos[alvos.body == 'MOON'].tile_id),
                                 'divide_com_MARS': ';'.join(alvos[alvos.body == 'MARS'].tile_id)})
            locais = terra.groupby(['site_name', 'tipo']).size().reset_index(name='recortes')
            corpos = ', '.join(f'{b} ({n})' for b, n in alvos.body.value_counts().items())
            nomes = ', '.join(f'{r.site_name}{" [CONTROLE]" if r.tipo == "controle" else ""}'
                              f'{f" ×{r.recortes}" if r.recortes > 1 else ""}' for r in locais.itertuples())
            out += [f'- **Cluster {cid}** — alvos: {corpos}; Terra ({len(terra)} recortes): {nomes or "nenhum"}']
        out += ['']

    pd.DataFrame(analogos).to_csv(a.saida.with_name('analogos_por_k.csv'), index=False)
    out += ['---', 'Locais marcados [CONTROLE] (cidades/florestas) caindo junto com Lua/Marte indicam que o '
            'cluster é grosseiro demais para aquele k.']
    a.saida.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'OK: {a.saida.name} e analogos_por_k.csv')


if __name__ == '__main__':
    main()

"""Ranking de similaridade exploratório do V1.3.1 (tolerâncias NÃO validadas)."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .config import METODOS


def analisar_similarity(df):
    terra = df.loc[df.body == 'EARTH']
    targets = df.loc[df.body.isin(['MARS', 'MOON'])]
    rows = []
    for method, (cols, tau) in METODOS.items():
        for _, t in targets.iterrows():
            for _, e in terra.iterrows():
                scores = {f'{c}_score': 100 * math.exp(-abs(float(t[c]) - float(e[c])) / float(v))
                          for c, v in zip(cols, tau)}
                rows.append({'feature_set': method, 'earth_id': e.region_id,
                             'earth_name': e.region_name, 'earth_tipo': e.tipo,
                             'target_id': t.region_id, 'target_name': t.region_name,
                             'target_body': t.body, 'final_score': float(np.mean(list(scores.values()))),
                             **scores})
    if not rows:
        return pd.DataFrame()
    rank = pd.DataFrame(rows).sort_values(['feature_set', 'target_body', 'final_score'],
                                          ascending=[True, True, False])
    rank['rank_all'] = rank.groupby(['feature_set', 'target_id']).cumcount() + 1
    # Os controles permanecem no ranking completo para avaliar falsos análogos.
    rank['rank_candidates'] = np.nan
    for (_, _), grupo in rank[rank.earth_tipo != 'controle'].groupby(['feature_set', 'target_id']):
        rank.loc[grupo.index, 'rank_candidates'] = np.arange(1, len(grupo) + 1)
    return rank

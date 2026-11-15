"""Pipeline V1.3.1 (conversão do notebook DadosTerra.ipynb).

Uso:
    python -m src.pipeline_v1_3_1 executar   [--sem-planetas] [--out PASTA]
    python -m src.pipeline_v1_3_1 recuperar  --zip-v13 ARQUIVO.zip [--out PASTA]

`executar` processa os 43 locais + 2 alvos do zero (NASADEM exige login Earthdata
já feito via netrc). `recuperar` reproduz a célula de recuperação incremental
(reaproveita o ZIP V1.3 e só processa locais pendentes). As células de upload/download
do Colab não foram convertidas.
"""
from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from . import config as C
from .features import calcular_features
from .fontes_terra import dem_terra, escolher_fonte
from .planetas import dem_planeta, procurar_planeta
from .similaridade import analisar_similarity
from .util import ler_csv, salvar_tif


def exportar(OUT, features, status, df_catalogo, stats):
    OUT.mkdir(parents=True, exist_ok=True)
    df_feat = pd.DataFrame(features)
    df_status = pd.DataFrame(status)
    df_feat.to_csv(OUT / 'terrain_features_v1_3_1.csv', index=False)
    df_status.to_csv(OUT / 'processing_status.csv', index=False)
    df_catalogo.to_csv(OUT / 'earth_candidates_climate_original.csv', index=False)
    if not df_feat.empty:
        earth = df_feat[df_feat.body == 'EARTH'].copy()
        targets = df_feat[df_feat.body.isin(['MARS', 'MOON'])].copy()
        earth.to_csv(OUT / 'cluster_input_earth_8features.csv', index=False)
        targets.to_csv(OUT / 'cluster_input_targets_8features.csv', index=False)
        essentials = ['region_id', 'region_name', 'body', 'tipo', 'center_lat', 'center_lon',
                      'source_dataset'] + C.FEATURES_CLUSTER
        earth[essentials].to_csv(OUT / 'cluster_input_earth_3features.csv', index=False)
        targets[essentials].to_csv(OUT / 'cluster_input_targets_3features.csv', index=False)
        rank = analisar_similarity(df_feat)
        rank.to_csv(OUT / 'similarity_rankings_exploratory.csv', index=False)
        if not rank.empty:
            rank[rank.earth_tipo != 'controle'].to_csv(OUT / 'similarity_rankings_candidates.csv', index=False)
    else:
        rank = pd.DataFrame()
    completo = (len(df_feat[df_feat.body == 'EARTH']) == len(df_catalogo) and
                len(df_feat[df_feat.body.isin(['MARS', 'MOON'])]) == 2)
    metadata = {
        'protocol': 'v1_3_1_40m_9km', 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'expected_earth_sites': len(df_catalogo), 'earth_sites_ok': sum(d['body'] == 'EARTH' for d in features),
        'targets_ok': sum(d['body'] in ('MARS', 'MOON') for d in features),
        'complete_for_team_delivery': bool(completo),
        'analysis_grid_m': C.RES_M, 'aoi_size_m': C.N * C.RES_M,
        'source_native_resolution': {'NASADEM': '~30m', 'ArcticDEM': '32m', 'REMA': '32m',
                                     'Mars_CTX': '20m', 'Moon_LOLA': '5m'},
        'algorithm': {'gaussian_sigma_px': C.SIGMA_PX, 'roughness_window_px': C.RUGOSIDADE_JANELA,
                      'edge_exclusion_px': C.BORDA_PX, 'nodata_neighborhood_exclusion_px': C.RAIO_EXCLUSAO_NODATA,
                      'min_valid_coverage_pct': C.MIN_VALID_PCT, 'slope': 'np.gradient on Gaussian-filtered DEM',
                      'roughness': 'local standard deviation on Gaussian-filtered mean-centered DEM',
                      'robust_relief': 'DEM percentile95 minus percentile5'},
        'experimental_rank_formula': '100*exp(-abs(x-y)/tolerance), equal weights',
        'experimental_methods': C.METODOS,
        'limitations': [
            '40m V1.3.1: não comparar scores numericamente com a versão V1.2 de 30m.',
            'A mesma grade de 40m não implica mesma resolução efetiva/incerteza dos DEMs.',
            'ArcticDEM/REMA são modelos de superfície (DSM), podendo incluir vegetação e estruturas.',
            'NASA DEM/DEM polar têm origens e períodos distintos; documentar diferenças.',
            'Recortes planetários centrais são testes, não áreas selecionadas para missões.',
            'Métodos e tolerâncias de similaridade são exploratórios e não demonstram habitabilidade.',
            'Cada local terrestre representado por um recorte de 9x9 km ao redor de ponto informado.',
            'Clima do CSV não entrou na comparação topográfica; procedência temporal não confirmada.',
            'Uma única posição pode não representar regiões naturais extensas.',
            'Até 0,1% de pixels NoData: vizinho próximo só para filtros; zona de 7 px excluída das métricas locais.',
            'Percentis e extremos são calculados somente com elevações originalmente válidas.',
        ],
        'source_links': {
            'NASADEM': 'https://search.earthdata.nasa.gov/',
            'PGC_STAC': 'https://stac.pgc.umn.edu/api/v1/',
            'PGC_DOCS': 'https://www.pgc.umn.edu/guides/stereo-derived-elevation-models/pgc-dem-products-arcticdem-rema-and-earthdem/',
        },
        'runtime': stats,
    }
    (OUT / 'processing_metadata.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
    (OUT / 'LEIA_ME.txt').write_text(
        'SPACE ANALOGS — EXPORTAÇÃO V1.3.1\n'
        'As features são valores físicos SEM normalização.\n'
        'cluster_input_earth_3features.csv: locais terrestres para clustering.\n'
        'cluster_input_targets_3features.csv: referências Marte/Lua (não usar como treino\n'
        'de K-Means caso o objetivo seja agrupar apenas regiões terrestres).\n'
        'terrain_features_v1_3_1.csv: todas as 8 features por região.\n'
        'processing_status.csv: conferência de regiões faltantes/erro.\n'
        'processing_metadata.json: parâmetros, fontes e alerta de completude.\n'
        'dem_crops/*.tif: recortes numéricos georreferenciados (NoData originais preservados).\n'
        'similarity_rankings_exploratory.csv: ranks experimentais, não probabilidades.\n'
        'ATENÇÃO: somente enviar à equipe como base completa se earth_sites_ok=43 e targets_ok=2.\n',
        encoding='utf-8'
    )
    return df_feat, df_status, rank, completo


def _processar_planetas(output_dir, features, status):
    for ident, nome, corpo, pattern, source in C.PLANETA_CFG:
        print(f'[ALVO] {nome}', flush=True)
        try:
            path = procurar_planeta(pattern)
            if path is None:
                raise FileNotFoundError(f'GeoTIFF {pattern} não encontrado em {C.ENTRADA}')
            dem, tf, crs, meta = dem_planeta(path)
            feat = calcular_features(dem)
            features.append({'region_id': ident, 'region_name': nome, 'body': corpo,
                             'tipo': 'alvo', **meta, 'source_dataset': source, **feat})
            if C.SALVAR_RECORTE_TIF:
                salvar_tif(output_dir / 'dem_crops' / f'{ident}.tif', dem, tf, crs)
            status.append({'region_id': ident, 'name': nome, 'source': source, 'status': 'OK', 'detail': ''})
            print('   OK', flush=True)
        except Exception as e:
            status.append({'region_id': ident, 'name': nome, 'source': source,
                           'status': 'ERRO', 'detail': f'{type(e).__name__}: {e}'})
            print('   ERRO', e, flush=True)


def executar(csv_path=C.CSV_LOCAIS, output_dir=C.OUT, planetas=True, relatorio=True):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Evita distribuir recortes antigos quando uma nova execução falhar.
    crops_dir = output_dir / 'dem_crops'
    if crops_dir.is_dir():
        for antigo in crops_dir.glob('*.tif'):
            antigo.unlink()
    df_catalogo = ler_csv(csv_path)
    print(f'CSV: {len(df_catalogo)} locais; planejado: ' +
          ', '.join(f'{k}={sum(escolher_fonte(r.lat, r.lon)[0] == k for _, r in df_catalogo.iterrows())}'
                    for k in ('NASADEM', 'ArcticDEM', 'REMA')))
    features = []
    status = []
    for n, (_, registro) in enumerate(df_catalogo.iterrows(), 1):
        ident = registro.region_id
        nome = registro.local
        fonte, _ = escolher_fonte(float(registro.lat), float(registro.lon))
        print(f'[{n:02d}/{len(df_catalogo):02d}] {nome} ({fonte})', flush=True)
        try:
            dem, tf, crs, meta = dem_terra(float(registro.lat), float(registro.lon))
            feat = calcular_features(dem)
            features.append({'region_id': ident, 'region_name': nome, 'body': 'EARTH',
                             'tipo': registro.tipo, **meta, **feat})
            if C.SALVAR_RECORTE_TIF:
                salvar_tif(output_dir / 'dem_crops' / f'{ident}.tif', dem, tf, crs)
            status.append({'region_id': ident, 'name': nome, 'source': fonte, 'status': 'OK',
                           'detail': (f"AVISO: {feat['nodata_pixels']} pixels NoData; "
                                      f"cobertura={feat['valid_coverage_pct']:.4f}%; zona excluída dos filtros")
                           if feat['nodata_pixels'] else ''})
            print(f"   OK inclinação={feat['mean_slope_deg']:.2f}° "
                  f"rugosidade={feat['roughness_m']:.2f}m", flush=True)
        except Exception as e:
            status.append({'region_id': ident, 'name': nome, 'source': fonte,
                           'status': 'ERRO', 'detail': f'{type(e).__name__}: {e}'})
            print('   ERRO:', type(e).__name__, str(e)[:220], flush=True)
        # Checkpoint a cada local: interrupções não apagam resultados parciais.
        pd.DataFrame(features).to_csv(output_dir / 'terrain_features_checkpoint.csv', index=False)
        pd.DataFrame(status).to_csv(output_dir / 'processing_status_checkpoint.csv', index=False)
    if planetas:
        _processar_planetas(output_dir, features, status)
    stats = {'processed': len(status), 'ok': sum(s['status'] == 'OK' for s in status),
             'errors': sum(s['status'] == 'ERRO' for s in status)}
    df_feat, df_status, rank, completo = exportar(output_dir, features, status, df_catalogo, stats)
    arquivo_zip = shutil.make_archive(str(output_dir), 'zip', str(output_dir))
    print('\n' + '=' * 55)
    print(f'RESULTADO: {sum(df_feat.body == "EARTH")}/{len(df_catalogo)} locais terrestres; '
          f'{sum(df_feat.body.isin(["MARS", "MOON"]))}/2 alvos planetários')
    print('PACOTE COMPLETO PARA EQUIPE:', 'SIM' if completo else 'NÃO — conferir processing_status.csv')
    print('ARQUIVOS:', output_dir)
    print('ZIP:', arquivo_zip)
    if relatorio:
        print('\nSTATUS COM ERROS:')
        print(df_status[df_status.status == 'ERRO'].to_string(index=False))
        if not rank.empty:
            print('\nTOP 5 (conjunto medianas_robusto, incluindo controles para diagnóstico):')
            print(rank[rank.feature_set == 'medianas_robusto'].groupby('target_body').head(5)[
                ['target_body', 'earth_name', 'earth_tipo', 'final_score']].to_string(index=False))
    return df_feat, df_status, rank, arquivo_zip


# ===================== RECUPERAÇÃO INCREMENTAL V1.3.1 =====================
def recuperar_v131(zip_entrada, pasta_saida=C.OUT):
    zip_entrada = Path(zip_entrada)
    pasta_saida = Path(pasta_saida)
    if not zip_entrada.exists():
        raise FileNotFoundError(f'Não encontrei {zip_entrada}. Forneça o ZIP V1.3 primeiro.')

    with zipfile.ZipFile(zip_entrada) as z:
        if z.testzip() is not None:
            raise ValueError('O arquivo ZIP original está corrompido.')
        obrigatorios = {
            'terrain_features_v1_3.csv', 'processing_status.csv',
            'earth_candidates_climate_original.csv', 'processing_metadata.json',
        }
        faltam = obrigatorios - set(z.namelist())
        if faltam:
            raise ValueError(f'ZIP original não contém: {sorted(faltam)}')
        if any(Path(n).is_absolute() or '..' in Path(n).parts for n in z.namelist()):
            raise ValueError('ZIP contém caminho não permitido.')
        if pasta_saida.exists():
            shutil.rmtree(pasta_saida)
        pasta_saida.mkdir(parents=True)
        z.extractall(pasta_saida)

    catalogo = ler_csv(pasta_saida / 'earth_candidates_climate_original.csv')
    feat_orig = pd.read_csv(pasta_saida / 'terrain_features_v1_3.csv')
    status_orig = pd.read_csv(pasta_saida / 'processing_status.csv')
    if feat_orig.region_id.duplicated().any():
        raise ValueError('IDs de features duplicados no ZIP de entrada.')

    # Completa novos campos de auditoria dos 42 recortes originais (100% válidos).
    area_interior = (C.N - 2 * C.BORDA_PX) ** 2 / (C.N * C.N) * 100
    feat_orig['nodata_pixels'] = 0
    feat_orig['local_metrics_coverage_pct'] = area_interior
    feat_orig['nodata_treatment'] = 'none'
    features = feat_orig.to_dict('records')
    status = status_orig.to_dict('records')
    ids_ok = set(feat_orig.region_id)
    pendentes = catalogo.loc[~catalogo.region_id.isin(ids_ok)]
    print(f'ZIP original: {len(ids_ok)} regiões/alvos já processados.')
    print(f'PENDENTES: {len(pendentes)} — ' + ', '.join(pendentes.local.astype(str)))

    for _, reg in pendentes.iterrows():
        ident = reg.region_id
        print(f'Processando somente: {reg.local}', flush=True)
        fonte, _ = escolher_fonte(float(reg.lat), float(reg.lon))
        try:
            dem, tf, crs, meta = dem_terra(float(reg.lat), float(reg.lon))
            feat = calcular_features(dem)
            features.append({'region_id': ident, 'region_name': reg.local,
                             'body': 'EARTH', 'tipo': reg.tipo, **meta, **feat})
            if C.SALVAR_RECORTE_TIF:
                salvar_tif(pasta_saida / 'dem_crops' / f'{ident}.tif', dem, tf, crs)
            status = [s for s in status if s['region_id'] != ident]
            detalhe = (f"AVISO: {feat['nodata_pixels']} pixels NoData; "
                       f"cobertura={feat['valid_coverage_pct']:.4f}%; zona excluída das métricas locais")
            status.append({'region_id': ident, 'name': reg.local, 'source': fonte,
                           'status': 'OK', 'detail': detalhe})
            print('  OK', detalhe, flush=True)
        except Exception as e:
            status = [s for s in status if s['region_id'] != ident]
            status.append({'region_id': ident, 'name': reg.local, 'source': fonte,
                           'status': 'ERRO', 'detail': f'{type(e).__name__}: {e}'})
            print('  ERRO:', e, flush=True)

    ordem = {r.region_id: i for i, r in catalogo.iterrows()}
    features.sort(key=lambda d: ordem.get(d['region_id'], 10_000))
    status.sort(key=lambda d: ordem.get(d['region_id'], 10_000))
    pd.DataFrame(features).to_csv(pasta_saida / 'terrain_features_checkpoint.csv', index=False)
    pd.DataFrame(status).to_csv(pasta_saida / 'processing_status_checkpoint.csv', index=False)

    stats = {'processed': len(status), 'ok': sum(s['status'] == 'OK' for s in status),
             'errors': sum(s['status'] == 'ERRO' for s in status)}
    df_feat, df_status, rank, completo = exportar(pasta_saida, features, status, catalogo, stats)
    arquivo_zip = shutil.make_archive(str(pasta_saida), 'zip', str(pasta_saida))
    n_terra = int((df_feat.body == 'EARTH').sum())
    n_target = int(df_feat.body.isin(['MARS', 'MOON']).sum())
    print(f'\nRESULTADO: {n_terra}/43 regiões terrestres; {n_target}/2 alvos.')
    print('Pronto para entrega dos dados físicos:', 'SIM' if completo else 'AINDA NÃO')
    print('ZIP final:', arquivo_zip)
    return df_feat, df_status, rank, arquivo_zip


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('executar')
    e.add_argument('--out', default=str(C.OUT))
    e.add_argument('--sem-planetas', action='store_true')
    r = sub.add_parser('recuperar')
    r.add_argument('--zip-v13', required=True)
    r.add_argument('--out', default=str(C.OUT))
    a = ap.parse_args()
    if a.cmd == 'executar':
        executar(output_dir=a.out, planetas=not a.sem_planetas)
    else:
        recuperar_v131(a.zip_v13, a.out)


if __name__ == '__main__':
    main()

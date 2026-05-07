import pandas as pd

from cache.csv import get_cached_csv, save_csv_cache
from utils.logger import displayLog


def extractCsv(path: str) -> pd.DataFrame:
    """
    Função que extratai dataframe  de csv(s).\n
    Apenas informe o caminho do arquivo em string
     """
    cached_dataframe = get_cached_csv(path)
    if cached_dataframe is not None:
        return cached_dataframe

    # Variavel para limitar a busca de linhas do csv, porque o tamanho é muito grande
    limitRows = 570000
    size = 80000
    chunks = []
    total = 0

    displayLog('Iniciando extração do csv')

    for chunk in pd.read_csv(path, sep=';', encoding='iso-8859-1', chunksize=size, low_memory=False):
        if total >= limitRows:
            break

        chunk = chunk[chunk['NO_REGIAO'].notna()]
        chunks.append(chunk)
        total +=len(chunk)

        

    displayLog(f'Total de linhas extráidas: {total}')
    df = pd.concat(chunks).reset_index()
    save_csv_cache(path, df)
    return df






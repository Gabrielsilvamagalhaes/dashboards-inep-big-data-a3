import pandas as pd


def extractCsv(path):
    # Variavel para limitar a busca de linhas do csv, o tamanho é muito grande
    limitRows = 1000

    df = pd.read_csv(path, sep=";",encoding='iso-8859-1', low_memory=False, nrows=limitRows)
    return df

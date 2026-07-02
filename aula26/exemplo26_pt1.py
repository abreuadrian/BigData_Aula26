import polars as pl
import matplotlib.pyplot as plt 
from datetime import datetime 
import numpy as np 
import os 

os.system('cls')

try:
    print('Lendo arquivo...')
    DADOS = r'./../dados/'
    inicio = datetime.now()

    df_plano_execucao = (
        pl.scan_parquet(DADOS + 'bolsa_familia.parquet')
            #Delimitar as Séries
            .select(['NOME MUNICÍPIO','VALOR PARCELA'])
            #---- Técnica
            .with_columns([
                #Cria uma tabela de números, substituindo os nomes das cidades
                pl.col('NOME MUNICÍPIO').cast(pl.Categorical)
            ])
            #Agrupar 
            .group_by('NOME MUNICÍPIO')
            #Soma
            .agg(pl.col('VALOR PARCELA').sum())
            #Ordenar 
            .sort('VALOR PARCELA', descending=True)
        )
    
    print('\nPlano de Execução')
    print(df_plano_execucao)
    
    df_bolsa_familia = df_plano_execucao.collect()
    print(df_bolsa_familia.head(10))
    final = datetime.now()
    print(f'Tempo: {final - inicio}')

    # df_filtrado = df_bolsa_familia.filter(pl.col('VALOR PARCELA') > 3000)
    # print(df_filtrado)

    # print(df_bolsa_familia.sort('VALOR PARCELA', descending=True).head(5)

except Exception as e:
    print(f'Erro ao obter dados: {e}')
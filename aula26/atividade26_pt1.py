import polars as pl
import os 

try:
    DADOS = r'./../dados/auxilio_br/'

    lista_arquivos = []
    df_auxilio_brasil = None

    lista_arquivos_dir = os.listdir(DADOS)

    for i in lista_arquivos_dir:
        if i.endswith('.csv'):
            lista_arquivos.append(i)

except Exception as e:
    print(f'Erro ao obter dados: {e}')
    

try:
    for arquivo in lista_arquivos:
        df = pl.read_csv(DADOS + arquivo, separator=';', encoding='iso-8859-1')

        if df_auxilio_brasil is None:
            df_auxilio_brasil = df
        else:
            df_auxilio_brasil = pl.concat([df_auxilio_brasil, df])

        del df

        print(f'\nArquivo {arquivo} procesado!')
    
except Exception as e:
    print(f'Erro 2º try: {e}')


try:
    df_auxilio_brasil = df_auxilio_brasil.with_columns(
        pl.col('VALOR PARCELA')
        .str.replace(',', '.')
        .cast(pl.Float64))

    print('\nIniciando a Gravação do Arquivo Parquet')
    df_auxilio_brasil.write_parquet(DADOS + 'auxilio_brasil.parquet')
    
    print('Arquivo Salvo')

except Exception as e:
    print(f'Erro 3º try: {e}')


try:
    plano_execucao = (pl.scan_parquet(DADOS + 'auxilio_brasil.parquet')
                      .select(['NOME MUNICÍPIO', 'VALOR PARCELA'])
                      .with_columns([pl.col('NOME MUNICÍPIO').cast(pl.Categorical)])
                      .group_by('NOME MUNICÍPIO')
                      .agg(pl.col('VALOR PARCELA').sum())
                      .sort('VALOR PARCELA', descending=True))
    
    df_auxilio_brasil = plano_execucao.collect()
    print(df_auxilio_brasil.head(10))

except Exception as e:
    print(f'Erro na leitura do parquet: {e}')

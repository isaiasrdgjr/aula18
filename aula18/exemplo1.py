import pandas as pd 
import numpy as np 

try:
    print('Obtendo dados...')
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencia = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencia.head(2))

    df_estelionato = df_ocorrencia.groupby('munic').sum(['estelionato']).reset_index()
    # print(df_estelionato[['munic', 'estelionato']])

except Exception as e:
    print(f"Erro: {e}")
    exit()

try:
    print('Obtendo iformações sobre padrões de estelionatos...')
    array_estelionato = np.array(df_estelionato['estelionato'])
    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)
    distancia = abs((media_estelionato - mediana_estelionato) / mediana_estelionato)

    print(array_estelionato)
    print(80*"=")
    print("MEDIDAS DE TENDÊNCIA CENTRAL\n")
    print(f'Média de estelionatos {media_estelionato:.2f}')
    print(f'Mediana de estelionatos {mediana_estelionato:.2f}')
    print(f'A distância entre média e mediana {distancia:.2f}')
    print(80*"=")
    
    q1 = np.quantile(array_estelionato, 0.25, method='weibull')
    q2 = np.quantile(array_estelionato, 0.50, method='weibull')
    q3 = np.quantile(array_estelionato, 0.75, method='weibull')

    df_estelionato_menores = df_estelionato[df_estelionato['estelionato'] < q1]
    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato'] > q3]

    print("\nMEDIDAS DE ESTELIONATOS POR CIDADE:")
    print(30*"=", "Cidades com menores índices de roubo: ", 30*"=")
    print(f"\n{df_estelionato_menores[['munic', 'estelionato']].sort_values('estelionato', ascending=True)}")
    print("\n", 30*"=", "Cidades com maiores índices de roubo: ", 30*"=")
    print(f"\n{df_estelionato_maiores[['munic', 'estelionato']].sort_values('estelionato', ascending=False)}")
    print(80*"=")

    iqr = q3-q1

    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    df_estelionato_outliers_superiores = df_estelionato[df_estelionato['estelionato'] > limite_superior]
    df_estelionato_outliers_inferiores = df_estelionato[df_estelionato['estelionato'] < limite_inferior]

    print('Outliers inferiores:')
    if len(df_estelionato_outliers_inferiores) == 0:
        print('Não há outliers inferiores')
    else:
        print(f"\n{df_estelionato_outliers_inferiores.sort_values('estelionato', ascending=True)}")
        print(80*'=')

    print('\nOutliers superiores')
    if len(df_estelionato_outliers_superiores) == 0:
        print('Não há outliers superiores:')
    else:
        print(f"\n{df_estelionato_outliers_superiores.sort_values('estelionato', ascending=False)}")
        print(80*'=')

except Exception as e:
    print(f"Erro: {e}")
    exit()

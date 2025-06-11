import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

try:
    print('Obtendo dados...')
    
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencia = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    df_ocorrencia = df_ocorrencia[['munic', 'roubo_veiculo']]
    df_roubo = df_ocorrencia.groupby('munic').sum(['roubo_veiculo']).reset_index()
   
except Exception as e:
    print(f"Erro: {e}")
    exit()
# iniciando análise

try:
    print('Obtendo iformações sobre padrão de roubos de veículos...')
    array_roubo_veiculo = np.array(df_roubo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)

    mediana_roubo_veiculo = np.median(array_roubo_veiculo)

    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo)

    print("MEDIDAS DE TENDÊNCIA CENTRAL")
    print(30*"=")
    print(f'Média de roubos {media_roubo_veiculo:.2f}')
    print(f'Mediana de roubos {mediana_roubo_veiculo:.2f}')
    print(f'A distância entre média e mediana {distancia:.2f}')

    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull')
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull')
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull')

    print("\nMEDIDAS DE POSIÇÃO")
    print(30*"=")
    print(f"Q1: {q1}, \nQ2: {q2}, \nQ3: {q3}")


    print("\nMEDIDAS DE DISPERÇÃO")
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude_total = maximo - minimo

    df_roubo_veiculo_menores = df_roubo[df_roubo['roubo_veiculo'] < q1]
    df_roubo_veiculo_maiores = df_roubo[df_roubo['roubo_veiculo'] > q3]

    print("\nMEDIDAS DE ROUBOS POR CIDADE")
    print(30*"=")
    print(f"Cidades com menores índices de roubo: \n{df_roubo_veiculo_menores.sort_values('roubo_veiculo', ascending=True)}")
    print(f"\nCidades com maiores índices de roubo: \n{df_roubo_veiculo_maiores.sort_values('roubo_veiculo', ascending=False)}")

    # Interquartil
    iqr = q3 - q1

    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    print(80*"=")
    print("\nMEDIDAS")
    print(f"Limite inferior: {limite_inferior}")
    print(f"MENOR VALOR: {minimo}")
    print(f"Q1: {q1}")
    print(f"Q2: {q2}")
    print(f"Q3: {q3}")
    print(f"IQR: {iqr}")
    print(f"Limite inferior: {limite_superior}")
    print(f"MAIOR VALOR: {maximo}")
    print(f"MÉDIA: {media_roubo_veiculo}") 
    print(f"MEDIANA: {mediana_roubo_veiculo}")
    print(f"DISTANCIA ENTRE MEDIA E MEDIANA: {distancia}")
    print(80*"=")

    df_roubo_veiculo_outliers_superiores = df_roubo[df_roubo['roubo_veiculo'] > limite_superior]
    df_roubo_veiculo_outliers_inferiores = df_roubo[df_roubo['roubo_veiculo'] < limite_inferior]

    print('Outliers inferiores')
    print(30*'=')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não há outliers inferiores')
    else:
        print(f"\n{df_roubo_veiculo_outliers_inferiores.sort_values('roubo_veiculo', ascending=True)}")

    print('\nOutliers superiores')
    print(30*'=')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não há outliers superiores')
    else:
        print(f"\n{df_roubo_veiculo_outliers_superiores.sort_values('roubo_veiculo', ascending=False)}")

except Exception as e:
    print(f'Erro: {e}')

try:
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    if not df_roubo_veiculo_outliers_inferiores.empty:
        dados_inferiores = df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True)
        
        ax[0].barh(dados_inferiores['munic'], dados_inferiores['roubo_veiculo'])
    else:
        ax[0].text(0.5, 0.5, 'Sem outliers', ha='center', va='center', fontsize=10)
        ax[0].set_title('Outliers inferiores')

    if not df_roubo_veiculo_outliers_superiores.empty:
        dados_superiores = df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=True)
        
        ax[0].barh(dados_superiores['munic'], dados_superiores['roubo_veiculo'])
    else:
        ax[0].text(0.5, 0.5, 'Sem outliers', ha='center', va='center', fontsize=10)
        ax[0].set_title('Outliers superiores')

    plt.show()
    
except Exception as e:
    print(f'Erro: {e}')
    
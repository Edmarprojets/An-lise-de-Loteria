from sqlalchemy import create_engine
import pandas as pd
from random import randint,choice


def conectar_banco():
    #cria o motor usado para conectar ao BD
    motor=create_engine(f'postgresql+psycopg2://postgres:postgres@localhost:5432/loterias', echo=True)
    return motor

def obter_dados(motor, sql_str):
    #inicia uma conexão e realiza um select
    with motor.connect() as con:
        df_retorno=pd.read_sql(sql_str,con=con)
    return df_retorno

def formar_apostas(numeros,quantidade_de_apostas,quantidade_numero_concurso,limite_de_par_impar):
    #recebem uma lista de numero e monta apostar aleatorias onde cada aposta contém um total de numeros conforme o limite e a quantidade é o numero de apostas a serem realizadas
    lista_total=[]
    for x in range(0,quantidade_de_apostas):
        aposta=[]
        loop=0
        par=0
        impar=0
        numeros_a_escolher= list(numeros)
        while quantidade_numero_concurso != loop:
         #inicia um loop que garante uma aposta sem repetições com um total de numeros = a variável limite e uma combinação de par e impar onde nenhum dos 2 ultrapasse 4 ou seja até 4 pares e 2 impares ou 4 impares e 2 pares.
            numero=choice(numeros_a_escolher)
            if numero not in aposta:
                if (numero % 2) == 0:
                    if par < limite_de_par_impar:
                        aposta.append(numero)
                        loop +=int(1)
                        par +=int(1)
                else:
                    if impar < limite_de_par_impar:
                        aposta.append(numero)
                        loop +=int(1)
                        impar +=int(1)
            numeros_a_escolher.remove(numero)
        aposta.sort()
        if aposta not in lista_total:
            lista_total.append(aposta)
    return pd.DataFrame(data=lista_total)
    
def aposta_melhores_numeros_mega():
    #realiza um select filtrando os 40 melhores numeros por frequência e excluíndo os que não sai as mais de 15 concurso.
    motor=conectar_banco()
    df_dados= obter_dados(motor,'select id_num_sort from mega_freq_num_sort where nao_sai_a <15 order by frequencia desc limit(40)')
    valores=df_dados['id_num_sort'].tolist()
    df_apostas=formar_apostas(valores,10,6,4)
    print(df_apostas.to_string(index=False, header=False))


aposta_melhores_numeros_mega()
#soma=df_dados['heranca'].str.contains(' 03 ',case=True).sum()



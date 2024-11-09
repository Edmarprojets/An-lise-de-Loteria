import psycopg2


class Analise():
#analiza individualmente cada concurso e obtem sua soma total, o numero de pares e de impares.

    def __init__(self,resultado_concurso,total_num_sorteado,prefixo,total_por_concurso):
        self.resultado_concurso=resultado_concurso
        self.total_num_sorteado=total_num_sorteado
        self.prefixo_tabela=prefixo
        self.total_por_concurso=total_por_concurso

      
        #pares e impares por concurso
        self.numeros_pares=0
        self.numeros_impares=0
        #armazena a soma de todos os numeros sorteados em um determinado concurso
        self.total_concurso=0

          

    def par_impar(self):
    #analisa individualmente cada concurso e obtem o total de numeros pares e impares

        inicio=0
        fim=0
        total = 3* int(self.total_num_sorteado) 
        total_numero=0 

        while fim < total:

        #percore a string que contem o resultado, separando numero a numero(3 em 3).
            inicio=int(fim)
            fim +=3
            numero=self.resultado_concurso[inicio:fim]
            total_numero += int(numero)

            #compara se o resto é igual a zero
            if (int(numero) % 2) == 0:
                self.numeros_pares +=1
            else:
                self.numeros_impares +=1

        self.total_concurso=total_numero 


    def nao_sai_a(self,prefixo_tabela):

        #percorre os 300 ultimos resultados analisando a ultima vez que cada numero saiu
        #from PGinicial import atualizebd
        
        con=psycopg2.connect(dbname='loterias',user='postgres',password='postgres')
        cur=con.cursor() 

        for numero in range(1,self.total_por_concurso +1):
        #consulta cada um dos possiveis numeros a ser sorteado
            
            nao_sai_a=0

            for concurso in self.resultado_concurso:
            #percorre uma lista de 300 concurso manipulando individualmente um a um
                inicio=0
                fim=0
                total = 3* int(self.total_num_sorteado) 
                lista_resultado_int=[]
                concurso=concurso[0]

                while fim < total:
                #percorre o concurso transformando em uma lista de inteiros
                    inicio=int(fim)
                    fim +=3
                    numeral=concurso[inicio:fim]
                    numeral=int(numeral)
                    lista_resultado_int.append(numeral)
                
                if numero not in lista_resultado_int:
                    nao_sai_a +=1
                elif numero in lista_resultado_int:
                    break

            #executar update  
            
            update="update " + prefixo_tabela + "freq_num_sort"
            cur.execute(update + " set nao_sai_a=%s where id_num_sort=%s ",(nao_sai_a,numero)) 
            con.commit()
            '''
            print(numero,nao_sai_a)
            atualizebd.conectarbd()
            atualizebd.cur.execute(update + " set nao_sai_a=%s where id_num_sort=%s ",(nao_sai_a,numero)) 
            atualizebd.con.commit()'''

        con.close()




import psycopg2

class Loteria():
#percorre um arquivo txt populando a tabela de resultados conforme o tipo de jogo
    
    def __init__(self,tipo_jogo,caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.ultimo_concurso = 0
        self.tipo_jogo = tipo_jogo
        self.total_num_sorteado = 0
        self.prefixo_tabela=""
        self.concurso=''


    def contar_linhas(self):
    #lê o txt obtendo o total de linhas e quantas vezes deve percorrer para apurar o arquivo inteiro
        lista=[]
        vezes_percorrer=0
        try:
            with open(r''+self.caminho_arquivo,'r')as arquivo:
                lista=arquivo.readlines()
                numero_linhas =len(lista)
                vezes_percorrer = int(numero_linhas) / 3

        except Exception as e:
            print("ocorreu um erro no metodo contar_linhas")
        return vezes_percorrer
        

    def modo_jogo(self):
    #cria as regras do tipo de jogo selecionado e sua devida instrução sql(tabela correta)
        
        if self.tipo_jogo == "Lotofacil":
            self.total_num_sorteado = 15
            self.prefixo_tabela = "ltfacil_"

        elif self.tipo_jogo == "Mega-Sena":
            self.total_num_sorteado = 6
            self.prefixo_tabela = "mega_"
        
        elif self.tipo_jogo == "Lotomania":
           self.total_num_sorteado = 20
           self.prefixo_tabela = "ltmania_"


    def obter_resultado(self):
    #percorre o arquivo organizando os resultados e inserindo no banco
        
        #define modo de jogo
        self.modo_jogo()

        #obtem o total de vezes a percorrer o arquivo
        total_vezes = self.contar_linhas()
      

        #conectar com o banco
        try:
            conectar=psycopg2.connect(dbname='loterias',user='postgres',password='postgres')
            cur=conectar.cursor()
        except Exception as e:
            print("erro ao conectar ao banco")


        #leitura do arquivo
        with open(self.caminho_arquivo,'r') as arquivo:
            vezes=0
            concurso_anterior=''
            
            while vezes < total_vezes :

                #pega 3 linhas do arquivo
                linha_concurso=arquivo.readline()
                linha_resultado=arquivo.readline()
                linha_vazia=arquivo.readline()
                
                #limpando a linha concurso
                linha_concurso=linha_concurso.replace('Concurso', '')
                linha_concurso=linha_concurso.strip()
                linha_concurso=linha_concurso.split()
                
                self.concurso=linha_concurso[0]
                

                #conpara se ouve repetição
                if self.concurso != concurso_anterior:
                
                    str_resultado=""
                    inicio_leitura=0
                    
                    #organiza o resultado conforme cada modo de jogo
                    if self.tipo_jogo == "Lotofacil" or self.tipo_jogo == "Mega-Sena" :
                        #percorre a linha que contém o resultado
                        for x in range(self.total_num_sorteado + 1):

                            #percorre a string de 2 em 2 posições
                            final_leitura= inicio_leitura + 2
                            numero=linha_resultado[inicio_leitura : final_leitura]
                            str_resultado +=' ' + numero
                            inicio_leitura+=2
                    else:
                        str_resultado=' ' + linha_resultado.strip()

                    
                    sql="insert into "+ self.prefixo_tabela     

                    sql_comparacao="select id_concurso from "+ self.prefixo_tabela +"resultados order by id_concurso desc limit(1)"
                    cur.execute(sql_comparacao)
                    comparacao=cur.fetchall()

                    if len(comparacao) ==0:
                        self.ultimo_concurso=1

                    elif len(comparacao) !=0:
                        comparacao=comparacao[0]
                        self.ultimo_concurso=int(comparacao[0])
                        self.ultimo_concurso+=1

                        
                    if self.ultimo_concurso == int(self.concurso):
                    #insert no banco
                        cur.execute(sql+"resultados(id_concurso,resultado) values(%s,%s);",(self.ultimo_concurso,str_resultado))
                        conectar.commit()
                    else:
                        arquivo_correcao=open('Log_'+ str(self.prefixo_tabela)+'.txt','a')
                        arquivo_correcao.write(''+ str(self.concurso) +' é diferente do esperado: '+ str(self.ultimo_concurso) + '\n')
                else:
                    #escreve no arquivo caso concurso esteja repetido
                    arquivo_correcao=open('Log_'+ str(self.prefixo_tabela) + '.txt','a')
                    arquivo_correcao.write(str(self.concurso) +'repetiu \n')
                    arquivo_correcao.close()
                vezes +=1
                concurso_anterior=self.concurso
        cur.close()

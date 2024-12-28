import analise_concursos
import psycopg2

class Atualizarbd():

    def __init__(self, tipo_jogo):
        self.plpgsql="apurar_frequencia"
        self.tipo_jogo=tipo_jogo
        #self.ultimo_concurso=ultimo_concurso
        self.prefixo_tabela=''
        self.total_num_sorteado=0
        self.total_num=0
        self.con=''
        self.cur=''


    def conectarbd(self):
        self.con=psycopg2.connect(dbname='loterias',user='postgres',password='postgres')
        self.cur=self.con.cursor() 


    def modo_jogo(self):
    #cria as regras do tipo de jogo selecionado e sua devida instrução sql(tabela correta)
        
        if self.tipo_jogo == "Lotofacil":
            self.total_num_sorteado = 15
            self.prefixo_tabela = "ltfacil_"
            self.total_num= 25


        elif self.tipo_jogo == "Mega-Sena":
            self.total_num_sorteado = 6
            self.prefixo_tabela = "mega_"
            self.total_num=60
        
        elif self.tipo_jogo == "Lotomania":
           self.total_num_sorteado = 20
           self.prefixo_tabela = "ltmania_"
           self.total_num=100


    def analise_individual(self):
    #percore toda a lista obtida pela instrução SQL e instancia cada concurso como objeto obtendo sua analise
    #popula tabela estatisticas

        self.conectarbd()
        sql="select id_concurso, resultado from "+ self.prefixo_tabela
        self.cur.execute(sql+"resultados order by id_concurso;")
        dados=self.cur.fetchall()

        sql_comparacao="select id_concurso from "+ self.prefixo_tabela +"estatisticas order by id_concurso desc limit(1)"
        self.cur.execute(sql_comparacao)
        comparacao=self.cur.fetchall()
        if len(comparacao) ==0:
            comparacao=1

        elif len(comparacao) !=0:
            comparacao=comparacao[0]
            comparacao=int(comparacao[0])

             

        for concurso, resultado in dados:
            #instancia a classe e usa o metodo par_impar
            concurso=int(concurso)

            if concurso > comparacao:
                analise=analise_concursos.Analise(resultado, self.total_num_sorteado, self.prefixo_tabela,self.total_num)
                analise.par_impar()

                #acessa as propriedades da classe e armazena em variáveis
                pares=analise.numeros_pares
                impares=analise.numeros_impares
                soma_total=analise.total_concurso

                sql="insert into "+ self.prefixo_tabela
                self.cur.execute(sql+"estatisticas(id_concurso,quant_par,quant_impar,soma_total) values(%s,%s,%s,%s)",(concurso, pares, impares, soma_total))
                self.con.commit()
        self.con.close()


    def quantoTempoNaoSai(self):
        self.conectarbd()
        sql_consulta="select resultado from " + self.prefixo_tabela
        self.cur.execute(sql_consulta +'resultados order by id_concurso desc limit(300)')
        dados=self.cur.fetchall()
                
        instancia=analise_concursos.Analise(dados, self.total_num_sorteado, self.prefixo_tabela,self.total_num)
        instancia.nao_sai_a(self.prefixo_tabela)

        self.con.close()       

            
    def analise_geral_freq(self):
        #Analisa qual numero mais sai por concurso, e usa a funcao apurar_frequencia para dar update no bd

        self.conectarbd()
        
              

        #popula freq_num_sort
        for numero in range(1,self.total_num +1):
            
            tabela_consulta= str(self.prefixo_tabela +'resultados')
            tabela_update=str(self.prefixo_tabela +'freq_num_sort')
            if numero in (1,2,3,4,5,6,7,8,9):
                numero ="0"+ str(numero)                
                self.cur.callproc(self.plpgsql,[numero,tabela_consulta,tabela_update])
                self.con.commit()
            else:
                numero =str(numero)
                self.cur.callproc(self.plpgsql,[numero,tabela_consulta,tabela_update])
                self.con.commit()
        self.con.close()


    def analise_geral_par_impar(self):
        #obtem a frequencia das combinações de par e impar que mais saem
        #popula a tabela freq_par_impar
        
        self.conectarbd()
        sql="select quant_par,quant_impar from " + self.prefixo_tabela +"estatisticas order by quant_par"
        self.cur.execute(sql)
        dados=self.cur.fetchall()

        sql_comparacao="select id_quant_par,id_quant_impar from " + self.prefixo_tabela +"freq_par_impar order by id_quant_par"
        self.cur.execute(sql_comparacao)
        lista_comparacao=self.cur.fetchall()

        insert="insert into "+ self.prefixo_tabela
        update="update " + self.prefixo_tabela

        lista_freq=[]
        ant_repeticao=[]

        
        for par,impar in dados:
            #percorre o select obtido organizando os dados 
            par=int(par)
            impar=int(impar)
            lista_freq.append((par,impar))

        for x,y in lista_freq:
        #percorre cada tupla analisando sua frequencia armazenando em ant_repeticao para evitar repetições

            if (x,y) not in ant_repeticao:
                frequencia=lista_freq.count((x,y))
                if (x,y) not in lista_comparacao:
                    self.cur.execute(insert +'freq_par_impar(id_quant_par,id_quant_impar,frequencia) values(%s,%s,%s)',(x,y,frequencia))
                    self.con.commit() 
                elif (x,y) in lista_comparacao:
                    self.cur.execute(update+'freq_par_impar set frequencia=%s where id_quant_par=%s and id_quant_impar=%s',(frequencia,x,y))
                    self.con.commit() 
                else:
                    print("nenhum procedimento foi realizado!,verifique seu código")
                ant_repeticao.append((x,y))
        
        self.con.close()
                


    def analise_geral_soma_total(self):
        #obtem a frequencia da soma total de cada concurso verificando assim qual a soma total que mais sai
        #popula a tabela freq_soma_total

        self.conectarbd()
        sql="select soma_total from "+ self.prefixo_tabela + 'estatisticas order by soma_total'
        self.cur.execute(sql)
        dados=self.cur.fetchall()

        sql_comparacao="select Id_soma_total from " + self.prefixo_tabela +"freq_soma_total order by id_soma_total"
        self.cur.execute(sql_comparacao)
        comparacao=self.cur.fetchall()

        lista_soma_total=[]
        lista_comparacao=[]
        ant_repeticao=[]

        for numero in dados:
            #percorre o select organizando em uma lista
            numero=int(numero[0])
            lista_soma_total.append(numero)

        for numero_comp in comparacao:
            #percorre o select de comparacao organizando em uma lista
            numero_comp=int(numero_comp[0])
            lista_comparacao.append(numero_comp)

        for numero in lista_soma_total:
        #para cada soma total insere ou atualiza sua frequencia
            if numero not in ant_repeticao:
                frequencia=lista_soma_total.count(numero)
                if numero not in lista_comparacao:
                    self.cur.execute("insert into " + self.prefixo_tabela + "freq_soma_total(id_soma_total,frequencia) values(%s,%s)",(numero,frequencia))
                    self.con.commit()
                elif numero in lista_comparacao:
                    self.cur.execute("update " + self.prefixo_tabela + "freq_soma_total set frequencia=%s where id_soma_total=%s",(frequencia,numero))
                else:
                    print("nenhum procedimento foi realizado!,verifique seu código")
                ant_repeticao.append(numero)
        self.con.close()

    
    def atualizado_em(self):
        self.conectarbd()
        self.cur.execute('select id_concurso from ' + self.prefixo_tabela + 'resultados order by id_concurso desc limit(1)')
        ultimo_concurso= self.cur.fetchall()

        self.cur.execute('update '+ self.prefixo_tabela + 'freq_par_impar set ultimo_concurso=%s',(ultimo_concurso))
        self.cur.execute('update '+ self.prefixo_tabela + 'freq_num_sort set ultimo_concurso=%s',(ultimo_concurso))
        self.cur.execute('update '+ self.prefixo_tabela + 'freq_soma_total set ultimo_concurso=%s',(ultimo_concurso))

        self.con.commit()
        self.con.close()

    def numeros_herdados(self):
        self.conectarbd()
        sql="select id_concurso, resultado from " + self.prefixo_tabela +"resultados where heranca is null and id_concurso <> 1 order by id_concurso asc "
        self.cur.execute(sql)
        resultado=self.cur.fetchall()
        sql_comparativo="select resultado from " + self.prefixo_tabela + "resultados where id_concurso=%s"
        classe_analise=analise_concursos.Analise(0, self.total_num_sorteado, self.prefixo_tabela,self.total_num)
        if len(resultado) != 0:
            for results in resultado:
                str_numeros=' '
                str_posicoes=' '
                numero=results[0]
                resultado_a_ser_comparado=results[1]
                self.cur.execute(sql_comparativo,(str(numero-1),))
                resultado_comparativo=self.cur.fetchall()
                #obtendo as posições da lista até virar apenas uma string
                resultado_comparativo=resultado_comparativo[0]
                resultado_comparativo=resultado_comparativo[0]
                #converte os resultados em uma lista de inteiros 
                comparado=classe_analise.converter_str_int(resultado_a_ser_comparado)
                comparativo=classe_analise.converter_str_int(resultado_comparativo)
                for num in comparado:
                    #verifica se o numero tbm saiu no concurso anterior e obtem sua posição
                    if comparativo.count(num) != 0:
                        posicao=comparativo.index(num) + 1
                        #converte a posiçao em str
                        if posicao in (0,1,2,3,4,5,6,7,8,9):
                            str_posicoes +='0'+ str(posicao) +' '
                        else:
                            str_posicoes +=str(posicao) +' '
                        #converte o numero em str
                        if num in (0,1,2,3,4,5,6,7,8,9):
                            str_numeros +='0'+ str(num) +' '
                        else:
                            str_numeros += str(num) + ' '
                #executar update no banco
                if str_numeros == ' ':
                    self.cur.execute('update ' +self.prefixo_tabela + 'resultados set heranca=null,posicao=null  where id_concurso=%s', (numero,))
                else:   
                    self.cur.execute('update ' +self.prefixo_tabela + 'resultados set heranca=%s,posicao=%s  where id_concurso=%s', (str_numeros,str_posicoes,numero))
                self.con.commit()
        self.cur.close()

             
    
#instancia_atualizar_concurso=Atualizarbd("Mega-Sena")
#instancia_atualizar_concurso.modo_jogo()
#instancia_atualizar_concurso.numeros_herdados()


from atualizar_estatisticas import Atualizarbd 
import analise_concursos
import psycopg2

class Aposta(Atualizarbd):

    def __init__(self,tipo_jogo):
        super().__init__(tipo_jogo)

        
    
    def gera_ultimas_apostas(self, num_concurso):
        #gera uma aposta contendo os ultimos 3 resultados
        self.modo_jogo()
        self.conectarbd()   
        sql_ultimo="select id_concurso, resultados from "+ self.prefixo_tabela +"resultados order by id_concurso desc limit(1)"
        sql_intervalo="select resultados from " + self.prefixo_tabela + "resultados where id_concurso between %s and %s"
            
        #classe_analise=analise_concursos.Analise(0, self.total_num_sorteado, self.prefixo_tabela,self.total_num)



        sql="insert into "+ self.prefixo_tabela     

        sql_comparacao="select id_concurso from "+ self.prefixo_tabela +"resultados order by id_concurso desc limit(1)"
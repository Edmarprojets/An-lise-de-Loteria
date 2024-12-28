import flet as ft
import psycopg2 as pg

def home(page:ft.Page):
    conectar=pg.connect(dbname='loterias',user='postgres',password='postgres')
    cur=conectar.cursor()
    cur.execute("select * from ltmania_resultados order by id_concurso desc limit(10)")
    dados=cur.fetchall()
    cabecalho = [
        ["Concurso", "Resultado", "herança","Posições"],
    ]

    # Criar a tabela
    tabela = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in cabecalho[0]],  # Cabeçalho da tabela
        rows=[ft.DataRow([ft.DataCell(ft.Text(str(cell))) for cell in row]) for row in dados[0:]]  # Dados
    )

    # Adicionar a tabela à página
    page.add(tabela)

# Iniciar a aplicação Flet
ft.app(target=home)
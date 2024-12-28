import flet as ft
from extracao import Extracao
from datetime import datetime
from apurar_concurso import Loteria
def pagina_extracao(pagina: ft.Page):

    def fechar_janela(e):
        mensagem.open=False
        pagina.update()

    mensagem=ft.AlertDialog(
        modal=True,
        title=ft.Text(value='Notificações'),
        content='',
        actions=[
            ft.TextButton(text= "Fechar", on_click= fechar_janela),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        ) 

    def iniciar_extracao(e):
    #valida os dados, instancia a classe e executa seus metodos
        #regras para obrigar digitar intervalos
        if not txtf_concurso_inicio.value or not txtf_concurso_final.value:
            if not txtf_concurso_inicio.value:
                txtf_concurso_inicio.error_text='Este campo é obrigátorio'  
                txtf_concurso_inicio.update()
            else:
                txtf_concurso_inicio.error_text=None
                txtf_concurso_inicio.update()
            if not txtf_concurso_final.value:
                txtf_concurso_final.error_text= 'Este campo é obrigátorio'
                txtf_concurso_final.update()
            else:
                txtf_concurso_final.error_text=None
                txtf_concurso_final.update()
        else:
            txtf_concurso_final.error_text=None
            txtf_concurso_final.update()
            txtf_concurso_inicio.error_text=None
            txtf_concurso_inicio.update()

            jogo=dp_modo_jogo.value
            inicio=int(txtf_concurso_inicio.value)
            final=int(txtf_concurso_final.value)

            txt_status_extracao.value="EXTRAÇÃO INICIADA"
            txt_status_extracao.color="red"
            txt_status_extracao.visible=True
            btn_iniciar_extracao.disabled=True
            pagina.add(txt_status_extracao)
            pagina.update()
            horario=datetime.now()
            hora_formatada=horario.strftime("%d-%m-%y-%H_%M_%S")
            instancia_extrair=Extracao(hora_formatada)
            instancia_extrair.definir_navegador(jogo)
            #for concurso in range(inicio,final+1):
            instancia_extrair.busca_alternativa(inicio, final)
            
            txt_status_extracao.value="Realizando apuração do arquivo..."
            txt_status_extracao.color="green"
            pagina.update()
            nome_arquivo=instancia_extrair.modo_jogo +'_' +  instancia_extrair.hr_inicio + '.txt'
            instancia_apurar=Loteria(dp_modo_jogo.value,nome_arquivo)
            instancia_apurar.obter_resultado()
            btn_iniciar_extracao.disabled=False
            txt_status_extracao.value="EXTRAÇÃO E ANALISE FINALIZADA COM SUCESSO!"
            pagina.update()

#-------------------------------Elementos da pagina---------------------------------------------------
    dp_modo_jogo=ft.Dropdown(
        label="modo de jogo",
        options=[
            ft.dropdown.Option("Lotofacil"),
            ft.dropdown.Option("Mega-Sena"),
            ft.dropdown.Option("Lotomania")],
            value='Lotofacil')

    txtf_concurso_inicio=ft.TextField(
        input_filter=ft.NumbersOnlyInputFilter(),
        label="buscar a partir de:",
        hint_text="Em qual concurso devo iniciar",
        text_align=ft.TextAlign.CENTER,        
        )
    txtf_concurso_final=ft.TextField(
        input_filter=ft.NumbersOnlyInputFilter(),
        label="buscar até:",hint_text="Até qual concurso devo consultar", 
        text_align=ft.TextAlign.CENTER)
    btn_iniciar_extracao= ft.ElevatedButton("Iniciar Extração", on_click=iniciar_extracao)
    txt_status_extracao=ft.Text(value="",color="red", text_align=ft.TextAlign.CENTER, visible=False)
#-------------------------------------Construção da página--------------------------------------------------
    
    layout_extracao=ft.Column(
        expand=True,
        controls=[
            dp_modo_jogo,
            txtf_concurso_inicio,
            txtf_concurso_final,
            btn_iniciar_extracao,
            txt_status_extracao

        ]
    )
    return layout_extracao





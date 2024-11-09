import flet as ft
from interface_extracao import pagina_extracao
from interface_estatisticas import pagina_estatisticas

def main (page:ft.Page):
    def apresentar(e):

        if e.control.selected_index != e.control.data:
        #if para evitar duplicidade  
            if len(layout.controls) > 2:
                   layout.controls.pop(-1) 
                   layout.update() 

            if e.control.selected_index == 1:
                layout.controls.append(pagina_extracao(page))
                e.control.data=1
                layout.update()

            if e.control.selected_index == 2:
                layout.controls.append(pagina_estatisticas(page))
                e.control.data=2
                layout.update()

            if e.control.selected_index == 0:
                e.control.data=0
                layout.update()

    barra_navegacao=ft.NavigationRail(
        data=int(0),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME,
                label='Início',
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.DATA_EXPLORATION_SHARP, 
                label="Extração"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.GRAPHIC_EQ,
                label='Estatísticas'
            )
        ],
        on_change=apresentar
    )

    layout=ft.Row(
        expand=True,
        controls=[
            barra_navegacao,
            ft.VerticalDivider(width=1),
        ]
    )

    page.add(layout)

if __name__ == "__main__":
    ft.app(target=main)

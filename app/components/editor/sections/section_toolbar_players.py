import flet as ft

def section_toolbar_players():
    return ft.Row(
        [
            ft.FilledButton("Novo Jogador", icon=ft.Icons.ADD),
            ft.OutlinedButton("Editar", icon=ft.Icons.EDIT),
            ft.OutlinedButton("Excluir", icon=ft.Icons.DELETE_OUTLINE),
            ft.Dropdown(hint_text="Clube", options=[ft.dropdown.Option("Todos")], width=180),
            ft.Container(expand=True),
            ft.TextField(hint_text="Buscar por nome", width=240, prefix_icon=ft.Icons.SEARCH),
        ],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
import flet as ft
from app.components.editor.open_create_club import open_create_club

def section_toolbar_clubs(page: ft.Page):
    return ft.Row(
        [
            ft.FilledButton("Novo Clube", icon=ft.Icons.ADD, on_click=lambda e: page.open(open_create_club(page))),
            ft.OutlinedButton("Editar", icon=ft.Icons.EDIT),
            ft.OutlinedButton("Excluir", icon=ft.Icons.DELETE_OUTLINE),
            ft.Dropdown(
                hint_text="Filtrar por liga",
                options=[ft.dropdown.Option("Todas")],
                width=220,
            ),
            ft.Container(expand=True),
            ft.TextField(hint_text="Buscar clube", width=240, prefix_icon=ft.Icons.SEARCH),
        ],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
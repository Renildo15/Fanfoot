import flet as ft

from app.components.editor.open_create_league_dialog import \
    open_create_league_dialog


def section_toolbar_leagues(page: ft.Page):
    return ft.Row(
        [
            ft.FilledButton(
                "Nova Liga",
                icon=ft.Icons.ADD,
                on_click=lambda e: page.open(open_create_league_dialog(page)),
            ),
            ft.OutlinedButton("Editar", icon=ft.Icons.EDIT),
            ft.OutlinedButton("Excluir", icon=ft.Icons.DELETE_OUTLINE),
            ft.Container(expand=True),
            ft.TextField(
                hint_text="Buscar por nome/país", width=280, prefix_icon=ft.Icons.SEARCH
            ),
        ],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

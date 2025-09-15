import flet as ft


def section_toolbar_stats():
    return ft.Row(
        [
            ft.OutlinedButton("Importar / Atualizar"),
            ft.OutlinedButton("Resetar temporada"),
            ft.Container(expand=True),
            ft.Dropdown(
                hint_text="Temporada", options=[ft.dropdown.Option("2025")], width=140
            ),
        ],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

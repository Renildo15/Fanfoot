import flet as ft


def header(page: ft.Page):
    return ft.Container(
        padding=ft.padding.symmetric(20, 12),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.TUNE, size=20),
                        ft.Text("Editor", size=22, weight=ft.FontWeight.W_700),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(expand=True),
                ft.Row(
                    [
                        ft.OutlinedButton(
                            "Voltar",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: page.go("/"),
                        ),                    ],
                    spacing=10,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

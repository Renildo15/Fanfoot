import flet as ft


def btn(
    text,
    icon,
    page: ft.Page,
    on_click=None,
):
    return ft.FilledTonalButton(
        content=ft.Row(
            [
                ft.Icon(icon, size=18),
                ft.Text(text, size=14, weight=ft.FontWeight.W_600),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        height=44,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.padding.symmetric(14, 10),
        ),
        on_click=on_click
        or (lambda e: page.snack_bar.open() if page.snack_bar else None),
    )

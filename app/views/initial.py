import flet as ft

from app.utils.caption import \
    caption  # se sua função caption está em app/utils/caption.py
# Se estiver em outro lugar, troque a importação conforme sua estrutura.
from app.utils.constants import APP_VERSION, ROUTES


def view(page: ft.Page) -> ft.Control:
    # Top bar
    top_bar = ft.Row(
        [
            caption(APP_VERSION, size=12, color=ft.Colors.WHITE70),
            ft.Container(expand=True),
            ft.Container(width=24),
            ft.TextButton(
                "Sair",
                style=ft.ButtonStyle(color=ft.Colors.WHITE),
                on_click=lambda e: page.window.close(),
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    # Watermark central
    title_watermark = ft.Text(
        "FANFOOT",
        size=92,
        weight=ft.FontWeight.W_900,
        color=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
        text_align=ft.TextAlign.CENTER,
        expand=True,
    )

    # Botões principais
    main_buttons = ft.Row(
        controls=[
            ft.FilledTonalButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.SPORTS_SOCCER, size=18),
                        ft.Text("Novo Jogo", size=14, weight=ft.FontWeight.W_600),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                height=44,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=ft.padding.symmetric(14, 10),
                ),
                on_click=lambda e: page.snack_bar.open() if page.snack_bar else None,
            ),
            ft.FilledTonalButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.DOWNLOAD, size=18),
                        ft.Text("Carregar", size=14, weight=ft.FontWeight.W_600),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                height=44,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=ft.padding.symmetric(14, 10),
                ),
            ),
            ft.FilledTonalButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.BRUSH, size=18),
                        ft.Text("Editor", size=14, weight=ft.FontWeight.W_600),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                height=44,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=ft.padding.symmetric(14, 10),
                ),
                on_click=lambda e: e.page.go(ROUTES["editor"]),
            ),
        ],
        spacing=12,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Rodapé à direita
    footer_right = ft.Column(
        [
            ft.Row(
                [
                    ft.Icon(ft.Icons.ALTERNATE_EMAIL, size=16),
                    ft.Text("@Footfantasy", size=12, weight=ft.FontWeight.W_600),
                ],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.Icon(ft.Icons.LINK, size=14),
                    ft.Text("links & comunidade", size=11, color=ft.Colors.WHITE70),
                ],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        spacing=4,
        horizontal_alignment=ft.CrossAxisAlignment.END,
    )

    bottom_bar = ft.Row(
        [main_buttons, ft.Container(expand=True), footer_right],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    # Overlay com gradiente
    glass_overlay = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=8),
                top_bar,
                ft.Container(
                    expand=True, alignment=ft.alignment.center, content=title_watermark
                ),
                bottom_bar,
                ft.Container(height=8),
            ],
            spacing=0,
            expand=True,
        ),
        padding=ft.padding.all(20),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                ft.Colors.with_opacity(0.60, ft.Colors.BLACK),
                ft.Colors.with_opacity(0.20, ft.Colors.BLACK),
                ft.Colors.with_opacity(0.70, ft.Colors.BLACK),
            ],
        ),
    )

    # Fundo (coloque assets/bg.png se quiser imagem)
    background = ft.Stack(
        controls=[
            ft.Image(
                src="assets/bg.png",
                fit=ft.ImageFit.FILL,
                expand=True,
            ),
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.CYAN_900),
            ),
        ],
        expand=True,
    )

    # SnackBar opcional
    page.snack_bar = ft.SnackBar(ft.Text("Ação de exemplo — vamos conectar depois."))

    return ft.Stack([background, glass_overlay], expand=True)


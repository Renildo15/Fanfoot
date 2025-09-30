# app/views/editor.py
import flet as ft

from app.components.editor.header import header
from app.components.editor.sections.section_toolbar_clubs import \
    section_toolbar_clubs
from app.components.editor.sections.section_toolbar_leagues import \
    section_toolbar_leagues
from app.components.editor.sections.section_toolbar_players import \
    section_toolbar_players
from app.components.editor.sections.section_toolbar_stats import \
    section_toolbar_stats
from app.components.editor.tables.clubs_table import clubs_table
from app.components.editor.tables.leagues_table import leagues_table
from app.components.editor.tables.players_table import players_table
from app.components.editor.tables.stats_table import stats_table
from app.services.club_service import list_clubs

SECTIONS = [
    ("Ligas", ft.Icons.EVENT_AVAILABLE_OUTLINED),
    ("Clubes", ft.Icons.STADIUM_OUTLINED),
    ("Jogadores", ft.Icons.PERSON_2_OUTLINED),
    ("Estatísticas", ft.Icons.BAR_CHART_OUTLINED),
]


def view(page: ft.Page) -> ft.Control:
    current = {"name": "Ligas"}  # estado simples
    clubs, total = list_clubs()
    clubs_table_ref = ft.Ref[ft.DataTable]()
    # ---------- Conteúdo da área principal ----------
    content_container = ft.Container(expand=True)

    def refresh_clubs():
        clubs, total = list_clubs()
        # Atualiza a tabela
        clubs_table_ref.current = clubs_table(clubs)
        page.update()

    def build_section_content(name: str) -> ft.Control:
        if name == "Ligas":
            return ft.Column(
                [
                    section_toolbar_leagues(page),
                    ft.Divider(opacity=0.2),
                    leagues_table(),
                ],
                spacing=12,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        if name == "Clubes":
            return ft.Row(
                [
                    # Coluna da esquerda
                    ft.Column(
                        [
                            section_toolbar_clubs(page, refresh_callback=refresh_clubs),
                            ft.Divider(opacity=0.2),
                            clubs_table(clubs),
                        ],
                        spacing=12,
                        expand=2,  # ocupa mais espaço
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    # Coluna da direita
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Image(
                                            src="/assets/placeholder_club.png",
                                            width=64,
                                            height=64,
                                            fit=ft.ImageFit.CONTAIN,
                                        ),
                                        width=80,
                                        height=80,
                                        border=ft.border.all(1, ft.Colors.GREY_300),
                                        border_radius=8,
                                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "Nome do Clube", size=20, weight="bold"
                                            ),
                                            ft.Text(
                                                "Sigla do Clube",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                        ]
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "Reputação: 0", size=20, weight="bold"
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Row(
                                                        [
                                                            ft.Text(
                                                                "Cor Primária: ",
                                                                size=14,
                                                                color=ft.Colors.GREY_600,
                                                            ),
                                                            ft.Container(
                                                                width=20,
                                                                height=20,
                                                                bgcolor=ft.Colors.BLUE,
                                                                border_radius=4,
                                                            ),
                                                        ]
                                                    ),
                                                    ft.Row(
                                                        [
                                                            ft.Text(
                                                                "Cor Secundária: ",
                                                                size=14,
                                                                color=ft.Colors.GREY_600,
                                                            ),
                                                            ft.Container(
                                                                width=20,
                                                                height=20,
                                                                bgcolor=ft.Colors.RED,
                                                                border_radius=4,
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.Container(
                                                content=ft.Image(
                                                    src="/assets/placeholder_country.png",
                                                    #here is flag´s country width and height
                                                    width=192,
                                                    height=128,
                                                    fit=ft.ImageFit.CONTAIN,
                                                ),
                                                border=ft.border.all(1, ft.Colors.GREY_300),
                                                border_radius=8,
                                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                            ),
                                            ft.Column([
                                                ft.IconButton(
                                                    icon=ft.Icons.EDIT_OUTLINED,
                                                    tooltip="Editar Clube",
                                                    on_click=lambda e: print(
                                                        "Editar Clube"
                                                    ),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.Icons.DELETE_OUTLINED,
                                                    tooltip="Excluir Clube",
                                                    on_click=lambda e: print(
                                                        "Excluir Clube"
                                                    ),
                                                ),
                                            ])
                                        ]
                                    ),
                                ]
                            ),
                            ft.Divider(opacity=0.2),
                            ft.Text(
                                "Aqui você pode renderizar jogadores, técnico, etc."
                            ),
                        ],
                        spacing=12,
                        expand=2,  # ocupa menos espaço
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
                expand=True,
                spacing=10,  # espaço entre colunas
                alignment=ft.MainAxisAlignment.START,
            )
        if name == "Jogadores":
            return ft.Column(
                [section_toolbar_players(), ft.Divider(opacity=0.2), players_table()],
                spacing=12,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        return ft.Column(
            [section_toolbar_stats(), ft.Divider(opacity=0.2), stats_table()],
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    # ---------- Sidebar ----------
    sidebar_col = ft.Column(spacing=6)

    def rebuild_sidebar():
        sidebar_col.controls.clear()
        for name, icon in SECTIONS:
            is_active = name == current["name"]
            sidebar_col.controls.append(
                ft.Container(
                    content=ft.TextButton(
                        content=ft.Row(
                            [ft.Icon(icon, size=18), ft.Text(name, size=14)],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            overlay_color=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
                            bgcolor=ft.Colors.with_opacity(
                                0.12 if is_active else 0.04, ft.Colors.WHITE
                            ),
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=ft.padding.symmetric(12, 10),
                        ),
                        on_click=lambda e, n=name: switch_section(n),
                    ),
                )
            )

    def switch_section(name: str):
        current["name"] = name
        content_container.content = build_section_content(name)
        rebuild_sidebar()
        page.update()

    # inicial
    rebuild_sidebar()
    content_container.content = build_section_content(current["name"])

    # ---------- Layout raiz ----------
    return ft.Column(
        [
            header(page),
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Row(
                    [
                        ft.Container(
                            width=230,
                            padding=10,
                            border=ft.border.all(
                                1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)
                            ),
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                            content=sidebar_col,
                        ),
                        ft.Container(width=16),
                        ft.Container(
                            expand=True,
                            padding=16,
                            border=ft.border.all(
                                1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)
                            ),
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
                            content=content_container,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    alignment=ft.MainAxisAlignment.START,
                ),
            ),
        ],
        expand=True,
        spacing=0,
    )

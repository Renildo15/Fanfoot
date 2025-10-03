import flet as ft
from app.db.models import Club
from app.services.country_service import get_country
from app.services.coach_service import get_coach

def club_info(club: Club):
    if club is None:
        return ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Selecione um clube para ver as informações",
                        size=16,
                        color=ft.Colors.GREY_500,
                    ),
                    padding=20,
                    alignment=ft.alignment.center,
                )
            ]
        )
    
    country = get_country(club.country_id)
    flag = ft.Image(
        src=country.flag if country.flag else "/assets/placeholder_club.png",
        width=192,
        height=128,
        fit=ft.ImageFit.CONTAIN,
        border_radius=8,
    )
    coach_text = ft.Text(f"Técnico: {club.coach.full_name}", size=14) if club.coach else ft.Text("Técnico: Não definido", size=14)
    
    return ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Image(
                            src=club.crest_path if club.crest_path else "/assets/placeholder_club.png",
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
                            ft.Text(club.name, size=20, weight="bold"),
                            ft.Text(
                                club.short_name if club.short_name else "Sem sigla",
                                size=14,
                                color=ft.Colors.GREY_600,
                            ),
                        ]
                    ),
                    ft.Column(
                        [
                            ft.Text(f"Reputacao: {club.reputation}", size=20, weight="bold"),
                            ft.Row(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "Cor Primaria: ",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Container(
                                                width=20,
                                                height=20,
                                                bgcolor=club.primary_color,  # Você pode adicionar cores ao modelo Club
                                                border_radius=4,
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "Cor Secundaria: ",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Container(
                                                width=20,
                                                height=20,
                                                bgcolor=club.secondary_color,  # Você pode adicionar cores ao modelo Club
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
                                content= flag,
                                border=ft.border.all(1, ft.Colors.GREY_300),
                                border_radius=8,
                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            ),
                            ft.Column(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        tooltip="Editar Clube",
                                        on_click=lambda e: print(f"Editar Clube: {club.name}"),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINED,
                                        tooltip="Excluir Clube",
                                        on_click=lambda e: print(f"Excluir Clube: {club.name}"),
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            ft.Row(
                [
                    ft.Text(f"Estadio: {club.stadium if club.stadium else 'Não definido'}", size=14),
                    coach_text
                ]
            ),
            ft.Divider(opacity=0.2),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Jogador")),
                    ft.DataColumn(ft.Text("Posicao")),
                    ft.DataColumn(ft.Text("Pais")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("Nome do Jogador")),
                            ft.DataCell(ft.Text("Posicao")),
                            ft.DataCell(ft.Text("Pais")),
                        ]
                    ),
                ],
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            ),
        ],
    )
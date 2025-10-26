from typing import List

import flet as ft

from app.components.editor.modals.content_csv_modal.club_content import \
    club_content
from app.components.editor.modals.content_csv_modal.competition_content import \
    competition_content
from app.components.editor.tables.players_table import players_table
from app.db.models import Club, Competition, Player
from app.utils.data_imports import ImportData


def open_csv_modal(
    page: ft.Page,
    clubs: List[Club] = [],
    competitions: List[Competition] =[],
    players: List[Player] = [],
    on_save_callback=None,
):
    def import_competitions(e):
        ImportData.data_import_competitions(competitions, page, on_save_callback)

    def import_clubs(e):
        ImportData.data_import_clubs(clubs, page, on_save_callback)

    def import_players(e):
        ImportData.data_import_players(players, page, on_save_callback)

    c_club = club_content(clubs) if clubs else ft.Text("Nenhum clube para importar.")
    c_competition = (
        competition_content(competitions)
        if competitions
        else ft.Text("Nenhuma competição para importar.")
    )

    p_player = players_table(players, is_from_csv=True) if players else ft.Text("Nenhum jogador para importar.")

    content = None

    if clubs:
        content = c_club
    elif competitions:
        content = c_competition
    elif players:
        content = p_player
    else:
        content = ft.Text("Nada para importar.")


    btn_actions = []
    title = "Importar dados CSV"
    if clubs:
        btn_actions.append(ft.TextButton("Importar clubes", on_click=import_clubs))
    if competitions:
        btn_actions.append(
            ft.TextButton("Importar competições", on_click=import_competitions)
        )
    if players:
        btn_actions.append(
            ft.TextButton("Importar jogadores", on_click=import_players)
        )

    btn_actions.append(ft.TextButton("Cancelar", on_click=lambda e: page.close(modal)))

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=content,
        scrollable=True,
        actions=[
            ft.Row(
                btn_actions,
                alignment=ft.MainAxisAlignment.END,
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return modal

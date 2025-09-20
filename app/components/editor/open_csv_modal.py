
from typing import List

import flet as ft

from app.db.models import Club, Competition
from app.utils.data_imports import ImportData
from app.components.editor.content_csv_modal.club_content import club_content
from app.components.editor.content_csv_modal.competition_content import competition_content


def open_csv_modal(page: ft.Page, clubs: List[Club]=None, competitions: List[Competition]=None, on_save_callback=None):
    def import_competitions(e):
        ImportData.data_import_competitions(competitions, page, on_save_callback)

    def import_clubs(e):
        ImportData.data_import_clubs(clubs, page, on_save_callback)

    c_club = club_content(clubs) if clubs else ft.Text("Nenhum clube para importar.")
    c_competition = competition_content(competitions) if competitions else ft.Text("Nenhuma competição para importar.")

    content = c_club if clubs else c_competition

    btn_actions = []
    if clubs:
        btn_actions.append(ft.TextButton("Importar clubes", on_click=import_clubs))
    if competitions:
        btn_actions.append(ft.TextButton("Importar competições", on_click=import_competitions))

    btn_actions.append(ft.TextButton("Cancelar", on_click=lambda e: page.close(modal)))

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Importar Clubes do CSV"),
        content=content,
        actions=[
            ft.Row(
                btn_actions,
                alignment=ft.MainAxisAlignment.END,
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return modal

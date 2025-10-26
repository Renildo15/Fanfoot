import flet as ft
from app.db.models import Player
from app.services.club_service import get_club
from typing import List
from app.utils.get_position import get_position


def players_table(players: List[Player]):
    rows = []
    for player in players:

        if player.current_club_id:
            club = get_club(player.current_club_id)
            club_name = club.name
        else:
            club_name = "Livre"

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(player.full_name)),
                    ft.DataCell(ft.Text(str(player.age))),
                    ft.DataCell(ft.Text(get_position(player.position.value))),
                    ft.DataCell(ft.Text(str(player.overall))),
                    ft.DataCell(ft.Text(str(player.potential))),
                    ft.DataCell(ft.Text(club_name)),
                ]
            )
        )

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Idade")),
            ft.DataColumn(ft.Text("Posição")),
            ft.DataColumn(ft.Text("Overall")),
            ft.DataColumn(ft.Text("Potencial")),
            ft.DataColumn(ft.Text("Clube")),
        ],
        rows=rows,
    )

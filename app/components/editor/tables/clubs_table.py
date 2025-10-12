import flet as ft

from app.db.models import Club
from app.services.club_service import list_clubs
from app.services.country_service import get_country


def clubs_table(clubs: Club, rebuild_club_info_callback: callable):
    rows = []

    for club in clubs:
        emblem = (
            ft.Image(
                src=(
                    club.crest_path
                    if club.crest_path
                    else "/assets/placeholder_club.png"
                ),
                width=32,
                height=32,
                fit=ft.ImageFit.CONTAIN,
                border_radius=8,
            )
            if club.crest_path
            else ft.Icon(ft.Icons.IMAGE, size=32)
        )

        country = get_country(club.country_id)
        flag = ft.Image(
            src=country.flag if country.flag else "/assets/placeholder_club.png",
            width=32,
            height=32,
            fit=ft.ImageFit.CONTAIN,
            border_radius=8,
        )

        btn_info_club = ft.TextButton(
            content=ft.Text(club.name),
            on_click=lambda e, club_id=club.id: rebuild_club_info_callback(club_id),
        )

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(emblem),
                    ft.DataCell(btn_info_club),
                    ft.DataCell(flag),
                    ft.DataCell(ft.Text(club.reputation)),
                ]
            )
        )

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Emblema")),
            ft.DataColumn(ft.Text("Clube")),
            ft.DataColumn(ft.Text("País")),
            ft.DataColumn(ft.Text("Reputação")),
        ],
        rows=rows,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
    )

from typing import List

import flet as ft

from app.db.models import Club
from app.services.country_service import get_country


def csv_preview_table(clubs_data: List[Club]):
    if not clubs_data:
        return ft.Text("Nenhum dado para exibir", italic=True)

    rows = []
    for club in clubs_data:
        emblem = (
            ft.Image(
                src=(
                    club.get("crest_path", "")
                    if club.get("crest_path")
                    else "/assets/placeholder_club.png"
                ),
                width=32,
                height=32,
                fit=ft.ImageFit.CONTAIN,
                border_radius=8,
            )
            if club.get("crest_path")
            else ft.Icon(ft.Icons.IMAGE, size=32)
        )
        country_flag = ft.Icon(ft.Icons.FLAG, size=32, color=ft.Colors.GREY_400)
        country_id = club.get("country_id") or club.get("country") or ""

        if country_id:
            try:
                country = get_country(str(country_id).upper())
                if country and country.flag:
                    country_flag = ft.Image(
                        src=country.flag,
                        width=32,
                        height=32,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=8,
                    )
            except:
                pass

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(emblem),
                    ft.DataCell(ft.Text(club.get("name", "N/A"))),
                    ft.DataCell(ft.Text(club.get("short_name", "N/A"))),
                    ft.DataCell(country_flag),
                    ft.DataCell(ft.Text(str(club.get("reputation", "N/A")))),
                ]
            )
        )

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Emblema")),
            ft.DataColumn(ft.Text("Clube")),
            ft.DataColumn(ft.Text("Sigla")),
            ft.DataColumn(ft.Text("País")),
            ft.DataColumn(ft.Text("Reputação")),
        ],
        rows=rows,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        heading_row_height=40,
        data_row_min_height=50,
    )

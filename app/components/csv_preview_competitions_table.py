from typing import List

import flet as ft

from app.db.models import Competition
from app.services.country_service import get_country


def csv_preview_competitions_table(competitions_data: List[Competition]):
    if not competitions_data:
        return ft.Text("Nenhum dado para exibir", italic=True)

    rows = []
    for competition in competitions_data:
        country_flag = ft.Icon(ft.Icons.FLAG, size=32, color=ft.Colors.GREY_400)
        country_id = competition.get("country_id") or competition.get("country") or ""

        if country_id:
            try:
                country = get_country(country_id)
                if country and country.flag:
                    country_flag = ft.Image(
                        src=country.flag,
                        width=32,
                        height=32,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=8,
                    )
            except Exception as ex:
                print(f"Erro ao obter bandeira do país {country_id}: {ex}")

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(competition.get("name", "N/A"))),
                    ft.DataCell(ft.Text(competition.get("type", "N/A"))),
                    ft.DataCell(ft.Text(str(competition.get("level", "N/A")))),
                    ft.DataCell(country_flag),
                    ft.DataCell(ft.Text(str(competition.get("max_teams", "N/A")))),
                ]
            )
        )

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Nível")),
            ft.DataColumn(ft.Text("País")),
            ft.DataColumn(ft.Text("Núm. Times")),
        ],
        rows=rows,
    )

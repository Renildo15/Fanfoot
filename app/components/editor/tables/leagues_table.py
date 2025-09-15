import flet as ft

from app.services.league_service import Competition, list_leagues
from app.utils.get_country_display import get_country_display
from app.utils.get_type_value import get_type_value


def leagues_table():

    competitions, total_count = list_leagues()

    def get_level_display(competition: Competition):
        if competition.type == "LEAGUE":
            match competition.level:
                case 1:
                    return f"{competition.level}° divisão"
                case 2:
                    return f"{competition.level}° divisão"
                case 3:
                    return f"{competition.level}° divisão"
                case 4:
                    return f"{competition.level}° divisão"
                case 5:
                    return f"{competition.level}° divisão"
                case 6:
                    return f"{competition.level}° divisão"
                case 7:
                    return f"{competition.level}° divisão"
                case 8:
                    return f"{competition.level}° divisão"
        return str(competition.level)

    rows = []
    for competition in competitions:
        primary_color_display = ft.Container(
            width=20,
            height=20,
            border_radius=10,
            bgcolor=competition.primary_color or "#000000",
            tooltip=competition.primary_color or "N/A",
        )

        secondary_color_display = ft.Container(
            width=20,
            height=20,
            border_radius=10,
            bgcolor=competition.secondary_color or "#FFFFFF",
            tooltip=competition.secondary_color or "N/A",
        )

        logo_display = (
            ft.Image(
                src=(
                    competition.logo_path
                    if competition.logo_path
                    else "/assets/placeholder_league.png"
                ),
                width=32,
                height=32,
                fit=ft.ImageFit.CONTAIN,
                border_radius=8,
            )
            if competition.logo_path
            else ft.Icon(ft.Icons.IMAGE, size=32)
        )
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(logo_display),
                    ft.DataCell(ft.Text(competition.name)),
                    ft.DataCell(ft.Text(get_country_display(competition.country_id))),
                    ft.DataCell(ft.Text(get_type_value(competition.type.value))),
                    ft.DataCell(ft.Text(get_level_display(competition))),
                    ft.DataCell(ft.Text(str(competition.max_teams))),
                    ft.DataCell(primary_color_display),
                    ft.DataCell(secondary_color_display),
                ]
            )
        )
        if not competitions:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Nenhuma competição encontrada")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Logo")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("País")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Nível")),
            ft.DataColumn(ft.Text("Times máx.")),
            ft.DataColumn(ft.Text("Cor Primária")),
            ft.DataColumn(ft.Text("Cor Secundária")),
        ],
        rows=rows,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
    )

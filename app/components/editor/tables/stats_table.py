import flet as ft


def stats_table():
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Jogador")),
            ft.DataColumn(ft.Text("Temporada")),
            ft.DataColumn(ft.Text("PJ")),
            ft.DataColumn(ft.Text("Gols")),
            ft.DataColumn(ft.Text("Assist.")),
            ft.DataColumn(ft.Text("Amarelos")),
            ft.DataColumn(ft.Text("Vermelhos")),
            ft.DataColumn(ft.Text("Nota média")),
        ],
        rows=[],
    )

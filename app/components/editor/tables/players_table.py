import flet as ft

def players_table():
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Idade")),
            ft.DataColumn(ft.Text("Posição")),
            ft.DataColumn(ft.Text("Overall")),
            ft.DataColumn(ft.Text("Potencial")),
            ft.DataColumn(ft.Text("Clube")),
        ],
        rows=[],
    )
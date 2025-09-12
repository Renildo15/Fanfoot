import flet as ft

def clubs_table():
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Clube")),
            ft.DataColumn(ft.Text("Sigla")),
            ft.DataColumn(ft.Text("País")),
            ft.DataColumn(ft.Text("Reputação")),
            ft.DataColumn(ft.Text("Orçamento")),
            ft.DataColumn(ft.Text("Liga")),
        ],
        rows=[],
    )
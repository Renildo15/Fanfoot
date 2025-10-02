import flet as ft


def club_info():
    return ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Image(
                            src="/assets/placeholder_club.png",
                            width=64,
                            height=64,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        width=80,
                        height=80,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    ),
                    ft.Column(
                        [
                            ft.Text("Nome do Clube", size=20, weight="bold"),
                            ft.Text(
                                "Sigla do Clube",
                                size=14,
                                color=ft.Colors.GREY_600,
                            ),
                        ]
                    ),
                    ft.Column(
                        [
                            ft.Text("Reputação: 0", size=20, weight="bold"),
                            ft.Row(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "Cor Primária: ",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Container(
                                                width=20,
                                                height=20,
                                                bgcolor=ft.Colors.BLUE,
                                                border_radius=4,
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "Cor Secundária: ",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Container(
                                                width=20,
                                                height=20,
                                                bgcolor=ft.Colors.RED,
                                                border_radius=4,
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Image(
                                    src="/assets/placeholder_country.png",
                                    # here is flag´s country width and height
                                    width=192,
                                    height=128,
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                border=ft.border.all(1, ft.Colors.GREY_300),
                                border_radius=8,
                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            ),
                            ft.Column(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        tooltip="Editar Clube",
                                        on_click=lambda e: print("Editar Clube"),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINED,
                                        tooltip="Excluir Clube",
                                        on_click=lambda e: print("Excluir Clube"),
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            ft.Row(
                [
                    ft.Text("Estádio: Nome do Estádio", size=14),
                    ft.Text("Tecnico: Nome do Técnico", size=14),
                ]
            ),
            ft.Divider(opacity=0.2),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Jogador")),
                    ft.DataColumn(ft.Text("Posição")),
                    ft.DataColumn(ft.Text("País")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("Nome do Jogador")),
                            ft.DataCell(ft.Text("Posição")),
                            ft.DataCell(ft.Text("País")),
                        ]
                    ),
                ],
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            ),
        ],
    )

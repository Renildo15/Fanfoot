import flet as ft
from app.components.csv_preview_table import csv_preview_table
from app.db.models import Club
from typing import List

def club_content(clubs: List[Club]):
    return ft.Column(
        [
            ft.Text(
                f"Pré-visualização - {len(clubs)} clubes encontrados",
                size=16,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Divider(),
            ft.Container(
                csv_preview_table(clubs),
                border=ft.border.all(1, ft.Colors.GREY_200),
                border_radius=8,
                padding=10,
            ),
            ft.Text(
                "Verifique os dados antes de importar",
                size=12,
                color=ft.Colors.GREY_600,
            ),
        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        height=500,
        width=850,
    )
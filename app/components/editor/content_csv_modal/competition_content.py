import flet as ft
from app.components.csv_preview_competitions_table import csv_preview_competitions_table
from app.db.models import Competition
from typing import List

def competition_content(competitionns: List[Competition]):
    return ft.Column(
        [
            ft.Text(
                f"Pré-visualização - {len(competitionns)} competições encontradas",
                size=16,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Divider(),
            ft.Container(
                content=csv_preview_competitions_table(competitionns),
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
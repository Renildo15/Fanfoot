import flet as ft
import re
from app.services.club_service import create_club
from app.services.country_service import get_country
from app.db.models import Club
from typing import List
from app.components.csv_preview_table import csv_preview_table

def open_csv_modal(page:ft.Page, clubs:List[Club], on_save_callback=None):

    def import_clubs(e):
        pattern = re.compile(r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$')
        for club in clubs:
            if not pattern.match(club.get('primary_color')) or not pattern.match(club.get('secondary_color')):
                page.open(ft.SnackBar(ft.Text(f"Adicione uma hexadecimal válido.")))
                page.update()
                return
            
            if not club.get("name") or not club.get("short_name"):
                page.open(ft.SnackBar(ft.Text(f"Preencha Nome e Abreviação.")))
                page.update()
                return
            
            if int(club.get("reputation")) == 0:
                page.open(ft.SnackBar(ft.Text(f"Preencha a Reputação.")))
                page.update()
                return

            if int(club.get("budget")) == 0 or int(club.get("wage_budget")) == 0:
                page.open(ft.SnackBar(ft.Text(f"Preencha os orçamentos.")))
                page.update()
                return
            
            if not club.get("federation"):
                page.open(ft.SnackBar(ft.Text(f"Preencha a Federação.")))
                page.update()
                return

            try:
                country_obj = None
                if club.get("country_id"):
                    country_obj = get_country(club.get("country_id"))
                
                league_obj = None

                payload = {
                    "name":club.get("name").strip(),
                    "short_name": club.get("short_name").strip(),
                    "reputation": int(club.get("reputation")),
                    "budget": float(club.get("budget")),
                    "wage_budget": float(club.get("wage_budget")),
                    "federation": club.get("federation"),
                    "crest_path": club.get("crest_path"),
                    "primary_color": club.get('primary_color'),
                    "secondary_color": club.get('secondary_color'),
                    "country": country_obj,
                    "league": league_obj,
                }

                create_club(payload)
                if on_save_callback:
                    on_save_callback()

                page.open(ft.SnackBar(ft.Text(f"{len(clubs)} clubes importados com sucesso!")))
            except Exception as ex:
                page.open(ft.SnackBar(ft.Text(f"Valores inválidos: {ex}")))
                print(ex)
                page.update()
                return
        page.update()
        page.close(modal)
        page.open(ft.SnackBar(ft.Text(f"{len(clubs)} clubes importados!")))

    content = ft.Column(
        [
            ft.Text(f"Pré-visualização - {len(clubs)} clubes encontrados", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Container(
                csv_preview_table(clubs),
                border=ft.border.all(1, ft.Colors.GREY_200),
                border_radius=8,
                padding=10,
            ),
            ft.Text("Verifique os dados antes de importar", size=12, color=ft.Colors.GREY_600),
        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        height=500,
        width=850,
    )

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Importar Clubes do CSV"),
        content=content,
        actions=[
            ft.TextButton("Importar clubes", on_click=import_clubs),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return modal
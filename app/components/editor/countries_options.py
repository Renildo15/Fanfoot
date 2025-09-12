import flet as ft
from app.db.models import Country
from typing import List

def countries_options(all_countries:List[Country]):
    return[
        ft.dropdown.Option(
            key=c.id,
            text=c.name,
            content=ft.Row([
                ft.Image(src=c.flag, width=24, height=16, fit=ft.ImageFit.CONTAIN),
                ft.Text(c.name),
            ])
        ) for c in all_countries
    ]
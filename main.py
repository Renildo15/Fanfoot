import flet as ft
from app.utils import constants
from app.views.initial import view as initial_view  # Importe aqui fora
from app.views.editor import view as editor_view
from app.db.db import init_db

def _build_view(page: ft.Page):
    routes = {
        constants.ROUTES["home"]: initial_view,
        constants.ROUTES["editor"]: editor_view,
    }
    return routes.get(page.route, initial_view)(page)

def on_route_change(e: ft.RouteChangeEvent):
    page = e.page
    page.clean()
    page.add(_build_view(page))
    page.update()

def main(page: ft.Page):

    # init_db()

    page.title = constants.APP_NAME
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0
    page.horizontal_alignment = "stretch"
    page.vertical_alignment = "stretch"

    page.on_route_change = on_route_change
    
    # Adicione um fallback direto para testar
    try:
        page.go(page.route or "/")
    except:
        # Se houver erro, adicione a view diretamente
        page.add(initial_view(page))
        page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
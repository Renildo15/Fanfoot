import flet as ft
from app.db.models import Position, PlayerPreferredFoot
from app.services.country_service import get_countries, get_country
from app.components.editor.countries_options import countries_options

def open_create_player(page: ft.Page):
    all_countries = get_countries()

    full_name = ft.TextField(label="Nome", autofocus=True, width=360)
    surname = ft.TextField(label="Apelido", width=360)
    age = ft.TextField(
        label="Idade",
        width=360,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="16",
    )
    position = ft.Dropdown(
        label="Posição",
        width=170,
        options=[ft.dropdown.Option(t.value) for t in Position],
        value=Position.GK.value,
    )
    secondary_position = ft.Dropdown(
        label="Segunda posição",
        width=170,
        options=[ft.dropdown.Option(t.value) for t in Position],
        value=Position.GK.value,
    )

    preferred_foot = ft.Dropdown(
        label="Pé dominante",
        width=170,
        options=[ft.dropdown.Option(t.value) for t in PlayerPreferredFoot],
        value=PlayerPreferredFoot.B.value,
    )
   
    overall = ft.TextField(
        label="Geral",
        width=360,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="50",
    )
   
    shirt_number = ft.TextField(
        label="Número da camisa",
        width=170,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="1",
    )

    country = ft.Dropdown(
        label="País",
        width=170,
        options=countries_options(all_countries),
    )


    form = ft.Column(
        [
            # bloco: identificação (nome + apelido + idade)
            ft.Row(
                [
                    ft.Column(
                        [ft.Text("Identificação", weight=ft.FontWeight.W_600), full_name],
                        expand=True,
                    ),
                    ft.Column(
                        [ft.Text("Dados rápidos", weight=ft.FontWeight.W_600), ft.Row([surname, age], spacing=12)],
                        width=360,
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),

            # bloco: nacionalidade e posições
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Nacionalidade & Clube", weight=ft.FontWeight.W_600),
                            ft.Row([country, shirt_number], spacing=12),
                        ],
                        expand=True,
                    ),
                    ft.Column(
                        [
                            ft.Text("Posições", weight=ft.FontWeight.W_600),
                            ft.Row([position, secondary_position, preferred_foot], spacing=12),
                        ],
                        width=540,
                    ),
                ],
                spacing=20,
            ),

            # bloco: atributos físicos e técnicos
            ft.Row(
                [
                    ft.Column(
                        [ft.Text("Atributos", weight=ft.FontWeight.W_600), ft.Row([overall], spacing=12)],
                        expand=True,
                    ),
                ],
                spacing=20,
            ),

            ft.Divider(opacity=0.2),

        ],
        spacing=16,
        width=820,
        scroll=ft.ScrollMode.AUTO,
    )

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Novo jogador"),
        content=form,
        actions=[
            ft.TextButton("Salvar", on_click=lambda e: print("opa")),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return modal
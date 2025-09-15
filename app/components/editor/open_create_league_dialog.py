import re

import flet as ft

from app.components.editor.countries_options import countries_options
from app.db.models import CompetitionType
from app.services.country_service import get_countries, get_country
from app.services.league_service import create_league
from app.utils.get_type_value import get_type_value


def open_create_league_dialog(page: ft.Page):
    all_countries = get_countries()

    def get_league_type(value):
        match value:
            case "Liga":
                return CompetitionType.LEAGUE.value
            case "Copa":
                return CompetitionType.CUP.value

    name = ft.TextField(label="Nome do campeonato", autofocus=True, width=360)

    search_field = ft.TextField(
        label="Buscar país", on_change=lambda e: filter_countries(e), width=300
    )

    country = ft.Dropdown(
        label="País",
        width=300,
        options=countries_options,
    )
    type_dd = ft.Dropdown(
        label="Tipo",
        width=220,
        options=[ft.dropdown.Option(get_type_value(t.value)) for t in CompetitionType],
        value=CompetitionType.LEAGUE.value,
    )
    level = ft.TextField(
        label="Nível", width=120, keyboard_type=ft.KeyboardType.NUMBER, value="1"
    )
    max_teams = ft.TextField(
        label="Times máx.", width=120, keyboard_type=ft.KeyboardType.NUMBER, value="20"
    )
    primary_color = ft.TextField(label="Cor primária", width=150, max_length=7)
    secondary_color = ft.TextField(label="Cor secundaria", width=150, max_length=7)
    logo_preview = ft.Image(
        src="assets/placeholder_league.png",
        width=64,
        height=64,
        fit=ft.ImageFit.CONTAIN,
    )
    chosen_logo = {"path": None}

    def filter_countries(e):
        search_text = search_field.value.lower()

        if search_field:
            filtered_countries = [
                c for c in all_countries if search_text in c.name.lower()
            ]
        else:
            filtered_countries = all_countries

        country.options = [
            ft.dropdown.Option(
                key=c.id,
                text=c.id,
                content=ft.Row(
                    [
                        ft.Image(
                            src=c.flag, width=24, height=16, fit=ft.ImageFit.CONTAIN
                        ),
                        ft.Text(c.name),
                    ]
                ),
            )
            for c in filtered_countries
        ]
        country.update()

    # ---- file picker (desktop) ----
    picker = ft.FilePicker()
    page.overlay.append(picker)

    def on_logo_picked(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        f = e.files[0]
        # Em desktop: f.path disponível; em web não há path local.
        if not f.path:
            page.snack_bar = ft.SnackBar(
                ft.Text("Neste modo não há caminho local disponível.")
            )
            page.snack_bar.open()
            page.update()
            return
        chosen_logo["path"] = f.path
        logo_preview.src = f.path
        page.update()

    picker.on_result = on_logo_picked

    def choose_logo(_):
        picker.pick_files(
            allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg", "webp"]
        )

    error_text = ft.Text("", color=ft.Colors.RED_300, size=12)

    #  ---- ações ----
    def submit(e):

        pattern = re.compile(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")

        if not pattern.match(primary_color.value) or not pattern.match(
            secondary_color.value
        ):
            error_text.value = "Adicione uma hexadecimal válido."
            page.update()
            return

        # validação mínima
        if not name.value or not type_dd.value:
            error_text.value = "Preencha Nome e Tipo."
            page.update()
            return

        # montar payload simples (sem ORM)
        try:

            country_obj = None
            if country.value:
                country_obj = get_country(country.value)

            payload = {
                "name": name.value.strip(),
                "country": country_obj,
                "type": get_league_type(type_dd.value),
                "level": int(level.value or 1),
                "max_teams": int(max_teams.value or 0),
                "logo_path": chosen_logo["path"],
                "primary_color": primary_color.value or "#000000",
                "secondary_color": secondary_color.value or "#FFFFFF",
            }

            create_league(payload)

        except Exception as ex:
            error_text.value = f"Valores inválidos: {ex}"
            print(ex)
            page.update()
            return
        page.update()
        page.close(dlg_modal)

    form = ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            name,
                            ft.Row([country, type_dd], spacing=10),
                            ft.Row(
                                [level, max_teams, primary_color, secondary_color],
                                spacing=10,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(width=20),
                    ft.Column(
                        [
                            ft.Text("Logo (opcional)", weight=ft.FontWeight.W_600),
                            logo_preview,
                            ft.OutlinedButton(
                                "Escolher arquivo",
                                icon=ft.Icons.IMAGE,
                                on_click=choose_logo,
                            ),
                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            error_text,
        ],
        tight=True,
        spacing=12,
        width=760,
    )
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Adicionar nova competição"),
        content=form,
        actions=[
            ft.TextButton("Salvar", on_click=lambda e: submit(e)),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    return dlg_modal

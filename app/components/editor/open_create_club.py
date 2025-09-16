import csv
import json
import re

import flet as ft

from app.components.editor.countries_options import countries_options
from app.db.models import ClubFederation
from app.services.club_service import create_club
from app.services.coach_service import get_coach, list_coachs
from app.services.country_service import get_countries, get_country
from app.services.file_service import FileService


def open_create_club(page: ft.Page, on_save_callback=None):
    all_countries = get_countries()
    all_coachs = list_coachs()
    file_service = FileService()
    coachs_options = [
        ft.dropdown.Option(key=c.id, text=c.full_name, content=ft.Text(c.full_name))
        for c in all_coachs
    ]
    name = ft.TextField(label="Nome do clube", autofocus=True, width=360)
    short_name = ft.TextField(label="Abreviação", width=360, max_length=3)
    reputation = ft.TextField(
        label="Força", width=170, keyboard_type=ft.KeyboardType.NUMBER, value="10"
    )
    budget = ft.TextField(
        label="Orçamento", width=170, keyboard_type=ft.KeyboardType.NUMBER, value="0.0"
    )
    wage_budget = ft.TextField(
        label="Orçamento Salários",
        width=170,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="0.0",
    )

    federation = ft.Dropdown(
        label="Federação",
        width=170,
        options=[ft.dropdown.Option(t.value) for t in ClubFederation],
        value=ClubFederation.FHV.value,
    )

    logo_preview = ft.Image(
        src="assets/placeholder_club.png", width=64, height=64, fit=ft.ImageFit.CONTAIN
    )

    country = ft.Dropdown(
        label="País",
        width=170,
        options=countries_options(all_countries),
    )

    coach = ft.Dropdown(label="Técnico", width=170, options=coachs_options)

    stadium = ft.TextField(label="Estádio", width=170)

    primary_color = ft.TextField(
        label="Cor primária", width=170, max_length=7, value="#000000"
    )
    secondary_color = ft.TextField(
        label="Cor secundária", width=170, max_length=7, value="#FFFFFF"
    )

    chosen_logo = {"path": None}

    picker = ft.FilePicker()
    page.overlay.append(picker)

    def on_logo_picked(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        f = e.files[0]
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
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg", "webp"],
        )

    error_text = ft.Text("", color=ft.Colors.RED_300, size=12)

    picker_file = ft.FilePicker()
    page.overlay.append(picker_file)

    def import_file(e):
        picker_file.pick_files(
            allow_multiple=False,
            allowed_extensions=["json", "csv"],
            dialog_title="Selecionar arquivo de dados",
            file_type=ft.FilePickerFileType.CUSTOM,
            initial_directory="/home/habby-valle/Documentos/projects/games/fantasyfoot/data",
        )

    def fill_form_from_data(data):
        if "name" in data:
            name.value = str(data["name"])
        if "short_name" in data:
            short_name.value = str(data["short_name"])
        if "reputation" in data:
            reputation.value = str(data["reputation"])
        if "budget" in data:
            budget.value = str(data["budget"])
        if "wage_budget" in data:
            wage_budget.value = str(data["wage_budget"])
        if "federation" in data:
            federation.value = str(data["federation"])
        if "primary_color" in data:
            primary_color.value = str(data["primary_color"])
        if "secondary_color" in data:
            secondary_color.value = str(data["secondary_color"])
        if "stadium" in data:
            stadium.value = str(data["stadium"])
        if "crest_path" in data and data["crest_path"]:
            chosen_logo["path"] = data["crest_path"]
            logo_preview.src = data["crest_path"]
        if "country_id" in data and data["country_id"]:
            country_id = get_country(int(data["country_id"]))
            country.value = country_id.id
        if "coach_id" in data and data["coach_id"]:
            coach_id = get_coach(int(data["coach_id"]))
            coach.value = coach_id.id
        page.update()

    def on_file_picker(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        file = e.files[0]
        print(f"Arquivo selecionado para importação: {file}")

        try:
            if file.name.endswith(".json"):
                page.open(
                    ft.SnackBar(ft.Text("Arquivo JSON selecionado. Processando..."))
                )
                if hasattr(file, "path") and file.path:
                    json_data = file_service.get_json(file.path)
                    fill_form_from_data(json_data)
                    page.open(
                        ft.SnackBar(ft.Text("Arquivo JSON selecionado processando."))
                    )
                else:
                    page.open(
                        ft.SnackBar(ft.SnackBar(ft.Text("Formato não suportado")))
                    )
            elif file.name.endswith(".csv"):
                page.open(
                    ft.SnackBar(ft.Text("Arquivo CSV selecionado. Processando..."))
                )
                if hasattr(file, "path") and file.path:
                    csv_data = file_service.get_csv(file.path)
                    if csv_data:
                        fill_form_from_data(csv_data[0])
                    page.open(ft.SnackBar(ft.Text("Dados CSV carregados!")))
                else:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Modo web: upload não implementado")
                    )
            else:
                page.open(ft.SnackBar(ft.SnackBar(ft.Text("Formato não suportado"))))
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro na importação: {ex}"))

        page.update()

    picker_file.on_result = on_file_picker

    def submit(e):
        pattern = re.compile(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")

        if not pattern.match(primary_color.value) or not pattern.match(
            secondary_color.value
        ):
            error_text.value = "Adicione uma hexadecimal válido."
            page.update()
            return

        if not name.value or not short_name.value:
            error_text.value = "Preencha Nome e Abreviação."
            page.update()
            return

        if int(reputation.value) == 0:
            error_text.value = "Preencha a Reputação."
            page.update()
            return

        if int(budget.value) == 0 or int(wage_budget.value) == 0:
            error_text.value = "Preencha os orçamentos."
            page.update()
            return

        if not federation.value:
            error_text.value = "Preencha a Federação."
            page.update()
            return

        try:
            country_obj = None
            if country.value:
                country_obj = get_country(country.value)

            coach_obj = None
            if coach.value:
                coach_obj = get_coach(coach.value)

            payload = {
                "name": name.value.strip(),
                "short_name": short_name.value.strip(),
                "reputation": int(reputation.value),
                "budget": float(budget.value),
                "wage_budget": float(wage_budget.value),
                "federation": federation.value,
                "crest_path": chosen_logo["path"],
                "primary_color": primary_color.value,
                "secondary_color": secondary_color.value,
                "country": country_obj,
                "coach": coach_obj,
                "stadium": stadium.value
            }

            create_club(payload)
            if on_save_callback:
                on_save_callback()
            page.open(ft.SnackBar(ft.Text(f"Clube criado com sucesso!")))

        except Exception as ex:
            error_text.value = f"Valores inválidos: {ex}"
            print(ex)
            page.update()
            return
        page.update()
        page.close(modal)

    form = ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "Escudo do Clube", weight=ft.FontWeight.W_600, size=16
                            ),
                            logo_preview,
                            ft.OutlinedButton(
                                "Escolher arquivo",
                                icon=ft.Icons.IMAGE,
                                on_click=choose_logo,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Row(
                [
                    name,
                    short_name,
                ],
                spacing=20,
            ),
            ft.Row(
                [
                    reputation,
                    budget,
                    wage_budget,
                ],
                spacing=20,
            ),
            ft.Row(
                [federation, country],
                spacing=20,
            ),
             ft.Row(
                [coach, stadium],
                spacing=20,
            ),
            ft.Row(
                [
                    primary_color,
                    secondary_color,
                ],
                spacing=20,
            ),
            error_text,
        ],
        spacing=15,
        width=760,
        scroll=ft.ScrollMode.AUTO,
    )

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Adicionar novo clube"),
        content=form,
        actions=[
            ft.TextButton("Salvar", on_click=submit),
            ft.TextButton("Importar dados", on_click=import_file),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return modal

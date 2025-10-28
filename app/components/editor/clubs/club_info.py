import csv

import flet as ft

from app.components.editor.modals.open_create_player import open_create_player
from app.components.editor.modals.open_csv_modal import open_csv_modal
from app.db.models import Club
from app.services.country_service import get_country
from app.utils.get_position import get_position_abbr_ptbr
from app.components.editor.modals.open_modal_delete import open_modal_delete


def club_info(page: ft.Page, club: Club, refresh_callback=None):
    if club is None:
        return ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Selecione um clube para ver as informações",
                        size=16,
                        color=ft.Colors.GREY_500,
                    ),
                    padding=20,
                    alignment=ft.alignment.center,
                )
            ]
        )
    picker_file = ft.FilePicker()
    page.overlay.append(picker_file)
    has_players = len(club.players) > 0
    btn_edit_ref = ft.Ref[ft.FilledButton]()
    btn_remove_ref = ft.Ref[ft.FilledButton]()
    selected_player_ref = ft.Ref[int]()

    def select_player(player_id: int):
        selected_player_ref.current = player_id

        btn_edit_ref.current.disabled = False
        btn_remove_ref.current.disabled = False

        page.update()

    def import_file(e):
        picker_file.pick_files(
            allow_multiple=False,
            allowed_extensions=["csv"],
            dialog_title="Selecionar arquivo de dados",
            file_type=ft.FilePickerFileType.CUSTOM,
            initial_directory="/home/habby-valle/Documentos/projects/games/fantasyfoot/data",
        )

    def on_file_picker(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        file = e.files[0]
        print(f"Arquivo selecionado para importação: {file}")

        try:
            if file.name.endswith(".csv"):
                page.open(
                    ft.SnackBar(ft.Text("Arquivo CSV selecionado. Processando..."))
                )
                if hasattr(file, "path") and file.path:
                    with open(file.path, "r", encoding="utf-8") as f:
                        csv_reader = csv.DictReader(f)
                        csv_data = list(csv_reader)
                        page.open(
                            open_csv_modal(
                                page,
                                players=csv_data,
                                club_id=club.id,
                                on_save_callback=refresh_callback,
                            )
                        )
                        page.open(ft.SnackBar(ft.Text("Dados CSV carregados!")))
                else:
                    page.open(ft.SnackBar(ft.Text("Modo web: upload não implementado")))
            else:
                page.open(ft.SnackBar(ft.SnackBar(ft.Text("Formato não suportado"))))
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro na importação: {ex}")))

        page.update()

    picker_file.on_result = on_file_picker
    table = None
    rows = []

    if len(club.players) == 0:
        table = ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Nenhum jogador registrado",
                        size=16,
                        color=ft.Colors.GREY_500,
                    ),
                    padding=20,
                    alignment=ft.alignment.center,
                )
            ]
        )
    else:

        for player in club.players:
            country_flag = ft.Icon(ft.Icons.FLAG, size=24, color=ft.Colors.GREY_400)
            if player.country_id:
                try:
                    country = get_country(player.country_id)
                    if country and country.flag:
                        country_flag = ft.Image(
                            src=country.flag,
                            width=24,
                            height=16,
                            fit=ft.ImageFit.CONTAIN,
                        )
                except Exception as ex:
                    print(f"Erro ao obter bandeira do país {player.country_id}: {ex}")
            btn_player = ft.TextButton(
                content=ft.Text(player.surname),
                on_click=lambda e, player_id=player.id: select_player(player_id),
            )
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(get_position_abbr_ptbr(player.position.value))
                        ),
                        ft.DataCell(btn_player),
                        ft.DataCell(country_flag),
                    ]
                )
            )

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Posição")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Pais")),
            ],
            rows=rows,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        )

    country = get_country(club.country_id if club.country_id else 0)
    flag = ft.Image(
        src=country.flag if country.flag else "/assets/placeholder_club.png",
        width=192,
        height=128,
        fit=ft.ImageFit.CONTAIN,
        border_radius=8,
    )
    coach_text = (
        ft.Text(f"Técnico: {club.coach.full_name}", size=14)
        if club.coach
        else ft.Text("Técnico: Não definido", size=14)
    )

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Image(
                            src=(
                                club.crest_path
                                if club.crest_path
                                else "/assets/placeholder_club.png"
                            ),
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
                            ft.Text(club.name, size=20, weight="bold"),
                            ft.Text(
                                club.short_name if club.short_name else "Sem sigla",
                                size=14,
                                color=ft.Colors.GREY_600,
                            ),
                        ]
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"Reputacao: {club.reputation}", size=20, weight="bold"
                            ),
                            ft.Row(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "Cor Primaria: ",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Container(
                                                width=20,
                                                height=20,
                                                bgcolor=club.primary_color,  # Você pode adicionar cores ao modelo Club
                                                border_radius=4,
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "Cor Secundaria: ",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Container(
                                                width=20,
                                                height=20,
                                                bgcolor=club.secondary_color,  # Você pode adicionar cores ao modelo Club
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
                                content=flag,
                                border=ft.border.all(1, ft.Colors.GREY_300),
                                border_radius=8,
                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            ),
                            ft.Column(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        tooltip="Editar Clube",
                                        on_click=lambda e: print(
                                            f"Editar Clube: {club.name}"
                                        ),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINED,
                                        tooltip="Excluir Clube",
                                        on_click=lambda e: print(
                                            f"Excluir Clube: {club.name}"
                                        ),
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
                    ft.Text(
                        f"Estadio: {club.stadium if club.stadium else 'Não definido'}",
                        size=14,
                    ),
                    coach_text,
                ]
            ),
            ft.Divider(opacity=0.2),
            table,
            ft.Divider(opacity=0.2),
            ft.Row(
                [
                    ft.FilledButton(
                        "Adicionar",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: page.open(open_create_player(page, club)),
                    ),
                    ft.FilledButton(
                        "Importar csv",
                        icon=ft.Icons.FILE_UPLOAD,
                        on_click=import_file,
                        disabled=has_players
                    ),
                    ft.FilledButton(
                        "Editar",
                        ref=btn_edit_ref,
                        icon=ft.Icons.EDIT,
                        on_click=lambda e: print(""),
                        disabled=True
                    ),
                    ft.FilledButton(
                        "Remover",
                        ref=btn_remove_ref,
                        icon=ft.Icons.DELETE, 
                        on_click=lambda e: page.open(open_modal_delete(page,selected_player_ref.current, refresh_callback)),
                        disabled=True
                    ),
                    # ft.FilledButton(
                    #     "Transferencia",
                    #     icon=ft.Icons.CHANGE_CIRCLE,
                    #     on_click=lambda e: print(""),
                    # ),
                ]
            ),
        ],
    )

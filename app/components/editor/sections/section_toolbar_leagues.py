import flet as ft
from app.components.editor.open_csv_modal import open_csv_modal
from app.services.file_service import FileService
from app.components.editor.open_create_league_dialog import \
    open_create_league_dialog


def section_toolbar_leagues(page: ft.Page, refresh_callback=None):
    picker_file = ft.FilePicker()
    page.overlay.append(picker_file)
    file_service = FileService()

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
                    csv_data = file_service.get_csv(file.path)
                    page.open(
                        open_csv_modal(
                            page, competitions=csv_data, on_save_callback=refresh_callback
                        )
                    )
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
    return ft.Row(
        [
            ft.FilledButton(
                "Nova Liga",
                icon=ft.Icons.ADD,
                on_click=lambda e: page.open(open_create_league_dialog(page)),
            ),
            ft.FilledButton(
                "Importar csv", icon=ft.Icons.FILE_UPLOAD, on_click=import_file
            ),
            ft.OutlinedButton("Editar", icon=ft.Icons.EDIT),
            ft.OutlinedButton("Excluir", icon=ft.Icons.DELETE_OUTLINE),
            ft.Container(expand=True),
            ft.TextField(
                hint_text="Buscar por nome/país", width=280, prefix_icon=ft.Icons.SEARCH
            ),
        ],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

import flet as ft
from app.services.player_service import delete_player

def open_modal_delete(page: ft.Page, obj_id:int, refresh_callback=None):
    def handle_delete(e):
        try:
            delete_player(obj_id)
            page.open(ft.SnackBar(ft.Text("Jogador deletado com sucesso!")))
            if refresh_callback:
                refresh_callback()
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro ao deletar jogador: {ex}")))
        finally:
            page.close(modal)
            page.update()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Deletar jogador"),
        content=ft.Column(
            [
                ft.Text(
                    "Tem certeza que deseja excluir este jogador? "
                    "Esta ação não poderá ser desfeita.",
                    color=ft.Colors.RED_400,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Text(f"ID do jogador: {obj_id}", size=12, color=ft.Colors.GREY),
            ],
            tight=True,
        ),
        actions=[
            ft.TextButton("Deletar", on_click=lambda e: handle_delete(e)),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return modal
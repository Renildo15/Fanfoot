import flet as ft
import flet.canvas as cv
from app.db.models import Position, PlayerPreferredFoot
from app.services.country_service import get_countries, get_country
from app.components.editor.countries_options import countries_options
from app.services.player_engine_stats_service import PlayerEngineStatsService
from app.db.models import Club

def open_create_player(page: ft.Page, club: Club):

    all_countries = get_countries()
    player_engine = PlayerEngineStatsService()
    full_name = ft.TextField(label="Nome", autofocus=True, width=360)
    surname = ft.TextField(label="Apelido", width=360, max_length=11, value="Jogador")
    age = ft.TextField(
        label="Idade",
        width=360,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="16",
        max_length=2
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
        value="Sem segunda posição",
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
        max_length=2
    )

    shirt_number = ft.TextField(
        label="Número da camisa",
        width=170,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="1",
        max_length=2
    )

    country = ft.Dropdown(
        label="País",
        width=170,
        options=countries_options(all_countries),
    )

   

    # Criar uma variável para armazenar o texto atual
    current_shirt_number = ft.Ref[ft.Text]()
    current_name = ft.Ref[ft.Text]()

    # Canvas com Stack (abordagem mais simples)
    circle_with_text = ft.Stack(
        [
            cv.Canvas(
                [
                    cv.Rect(
                        x=50.5,
                        y=29.5,
                        height=141,
                        width=99,
                        paint=ft.Paint(
                            stroke_width=2,
                            style=ft.PaintingStyle.FILL,
                            color=club.primary_color,
                        ),
                    ),
                    cv.Rect(
                        x=82,
                        y=22,
                        width=36,
                        height=8,
                        paint=ft.Paint(
                            style=ft.PaintingStyle.FILL,
                            color=club.secondary_color
                        ),
                    ),
                    cv.Path(
                        [
                            # ponto superior esquerdo da manga (ligado à camisa)
                            cv.Path.MoveTo(50.5 - 50, 40),  
                            # ponto superior direito da manga (fim da largura da manga)
                            cv.Path.LineTo(50.5, 30),  
                            # ponto inferior direito da manga (fim da altura da manga)
                            cv.Path.LineTo(50.5, 70),  
                            # ponto inferior esquerdo da manga (começo da altura da manga)
                            cv.Path.LineTo(50.5 - 50, 80),  
                            # fecha o caminho
                            cv.Path.Close(),
                        ],
                        paint=ft.Paint(
                            stroke_width=2,
                            style=ft.PaintingStyle.FILL,
                            color=club.secondary_color
                        ),
                    ),
                    cv.Path(
                        [
                            # ponto superior esquerdo da manga direita (ligado à camisa)
                            cv.Path.MoveTo(148.5 + 50, 40),  
                            # ponto superior direito da manga direita
                            cv.Path.LineTo(149, 30),  
                            # ponto inferior direito da manga direita
                            cv.Path.LineTo(149, 70),  
                            # ponto inferior esquerdo da manga direita
                            cv.Path.LineTo(148.5 + 50, 80),  
                            # fecha o caminho
                            cv.Path.Close(),
                        ],
                        paint=ft.Paint(
                            stroke_width=2,
                            style=ft.PaintingStyle.FILL,
                            color=club.secondary_color
                        ),
                    )
                ],
                width=200,
                height=200,
            ),
           ft.Container(
                content=ft.Text(
                    ref=current_name,
                    value=(surname.value or "").upper(),
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE,
                    font_family="Thailandesa"
                ),
                width=200,
                height=40,
                alignment=ft.Alignment(0, -5)
                
            ),

            ft.Container(
                content=ft.Text(
                    ref=current_shirt_number,
                    value=shirt_number.value,
                    size=64,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.WHITE,
                    font_family="Thailandesa"
                ),
                width=200,
                height=120,
               alignment=ft.Alignment(0, 0)
            ),
        ],
        width=400,
        height=200,
        alignment=ft.alignment.center
    )

    def update_shirtnumber(e=None):
        # Atualizar o texto com o valor atual do shirt_number
        if current_shirt_number.current:
            current_shirt_number.current.value = shirt_number.value
            current_shirt_number.current.update()

    def update_surname(e=None):
        if current_name.current:
            current_name.current.value = surname.value
            current_name.current.update()
    

    # Configurar o evento on_change
    shirt_number.on_change = update_shirtnumber
    surname.on_change = update_surname

    error_text = ft.Text("", color=ft.Colors.RED_300, size=12)

    def submit(e):
        if not full_name.value:
            error_text.value = "Adicione o nome do jogador."
            page.update()
            return
        
        if int(age.value) < 16 or int(age.value) > 40:
            error_text.value = "Idade inválida."
            page.update()
            return

        if int(shirt_number.value) <= 0 or not shirt_number.value:
            error_text.value = "Adicione um número válido"
            page.update()
            return
        
        if int(overall.value) < 50 or int(overall.value) > 99:
            error_text.value = "Overall inválido."
            page.update()
            return
        
        if secondary_position.value in "Sem":
            secondary_position.value = None

        height, weight = player_engine.get_height_and_weight(position.value)
        potential = player_engine.calculate_potential(int(overall.value), int(age.value), position.value)

        try:
            country_obj = None
            if country.value:
                country_obj = get_country(country.value)

            payload = {
                "full_name": full_name.value,
                "surname": surname.value,
                "age": age.value,
                "position": position.value,
                "secondary_position": secondary_position.value,
                "preferred_foot": preferred_foot.value,
                "overall": int(overall.value),
                "shirt_number": int(shirt_number.value),
                "country": country_obj,
                "height_cm": height,
                "weight_kg": weight,
                "morale": 000,
                "fitness": 100,
                "status": "status",
                "potential": potential,
                "salary_weekly": 0000,
                "contract_until": 00000,
                "current_club_id": club.id
            }
        except Exception as ex:
            error_text.value = f"Valores inválidos: {ex}"
            print(ex)
            page.update()
            return

    form = ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        circle_with_text,
                        alignment=ft.alignment.center,
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=10,
                        padding=20,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
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
            ft.TextButton("Salvar", on_click=lambda e: submit(e)),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return modal
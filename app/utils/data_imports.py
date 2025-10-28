import re
from typing import List

import flet as ft

from app.db.models import Club, Competition, Player
from app.services.club_service import create_club
from app.services.country_service import get_country
from app.services.league_service import create_league
from app.services.player_service import create_player
from app.services.player_engine_stats_service import PlayerEngineStatsService
from app.db.models import PlayerStatus

class ImportData:
    pattern = re.compile(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")
    player_engine = PlayerEngineStatsService()
    @classmethod
    def data_import_competitions(
        cls, competitions: List[Competition], page: ft.Page, on_save_callback=None
    ):
        for competition in competitions:
            if not cls.pattern.match(
                competition.get("primary_color")
            ) or not cls.pattern.match(competition.get("secondary_color")):
                page.open(ft.SnackBar(ft.Text(f"Adicione uma hexadecimal válido.")))
                page.update()
                return

            if not competition.get("name"):
                page.open(ft.SnackBar(ft.Text(f"Preencha o Nome.")))
                page.update()
                return

            if int(competition.get("level")) == 0:
                page.open(ft.SnackBar(ft.Text(f"Preencha o Nível.")))
                page.update()
                return

            if (
                int(competition.get("points_win")) == 0
                or int(competition.get("points_draw")) == 0
            ):
                page.open(
                    ft.SnackBar(
                        ft.Text(f"Preencha os pontos por vitória, empate e derrota.")
                    )
                )
                page.update()
                return

            try:
                country_obj = None
                if competition.get("country_id"):
                    country_obj = get_country(competition.get("country_id"))

                payload = {
                    "name": competition.get("name").strip(),
                    "type": competition.get("type"),
                    "level": int(competition.get("level")),
                    "max_teams": int(competition.get("max_teams")),
                    "points_win": int(competition.get("points_win")),
                    "points_draw": int(competition.get("points_draw")),
                    "points_lose": int(competition.get("points_lose")),
                    "gd_first": int(competition.get("gd_first")),
                    "logo_path": competition.get("logo_path"),
                    "primary_color": competition.get("primary_color"),
                    "secondary_color": competition.get("secondary_color"),
                    "country": country_obj,
                }

                create_league(payload)
                if on_save_callback:
                    on_save_callback()

                page.open(
                    ft.SnackBar(
                        ft.Text(f"{len(competitions)} ligas importadas com sucesso!")
                    )
                )
            except Exception as ex:
                page.open(ft.SnackBar(ft.Text(f"Valores inválidos: {ex}")))
                print(ex)
                page.update()
                return

    @classmethod
    def data_import_clubs(cls, clubs: List[Club], page: ft.Page, on_save_callback=None):
        for club in clubs:
            if not cls.pattern.match(
                club.get("primary_color")
            ) or not cls.pattern.match(club.get("secondary_color")):
                page.open(ft.SnackBar(ft.Text(f"Adicione uma hexadecimal válido.")))
                page.update()
                return

            if not club.get("name"):
                page.open(ft.SnackBar(ft.Text(f"Preencha o Nome.")))
                page.update()
                return

            try:
                country_obj = None
                if club.get("country_id"):
                    country_obj = get_country(club.get("country_id"))

                payload = {
                    "name": club.get("name").strip(),
                    "short_name": (
                        club.get("short_name").strip()
                        if club.get("short_name")
                        else None
                    ),
                    "reputation": (
                        int(club.get("reputation")) if club.get("reputation") else 0
                    ),
                    "budget": float(club.get("budget")) if club.get("budget") else 0.0,
                    "wage_budget": (
                        float(club.get("wage_budget"))
                        if club.get("wage_budget")
                        else 0.0
                    ),
                    "federation": club.get("federation"),
                    "stadium": (
                        club.get("stadium").strip() if club.get("stadium") else None
                    ),
                    "crest_path": club.get("crest_path"),
                    "primary_color": club.get("primary_color"),
                    "secondary_color": club.get("secondary_color"),
                    "country": country_obj,
                }

                create_club(payload)
                if on_save_callback:
                    on_save_callback()

                page.open(
                    ft.SnackBar(ft.Text(f"{len(clubs)} clubes importados com sucesso!"))
                )
            except Exception as ex:
                page.open(ft.SnackBar(ft.Text(f"Valores inválidos: {ex}")))
                print(ex)
                page.update()
                return

    @classmethod
    def data_import_players(cls, players: List[Player], page: ft.Page, club_id: int):
        for player in players:
            if not player.get("full_name"):
                page.open(ft.SnackBar(ft.Text(f"Preencha o Nome completo.")))
                page.update()
                return

            if int(player.get("age")) < 16 or int(player.get("age")) > 40:
                page.open(ft.SnackBar(ft.Text(f"Idade inválida.")))
                page.update()
                return
            
            if int(player.get("shirt_number")) <= 0 or not player.get("shirt_number"):
                page.open(ft.SnackBar(ft.Text(f"Número de camisa inválido.")))
                page.update()
                return
            overall = player.get("overall")
            if overall is not None:
                overall = int(overall)
                if overall == 0:
                    overall = cls.player_engine.generate_overall(int(player.get("age")))
            else:
                overall = cls.player_engine.generate_overall(int(player.get("age")))

            if overall < 50 or overall > 99:
                page.open(ft.SnackBar(ft.Text(f"Overall inválido.")))
                page.update()
                return

            
            height, weight = cls.player_engine.get_height_and_weight(player.get("position"))
            potential = cls.player_engine.calculate_potential(
                overall, int(player.get("age")), player.get("position")
            )

            weekly, months = cls.player_engine.generate_salary_and_contract(
                overall, int(player.get("age")), position=player.get("position")
            )

            try:
                country_obj = None
                if player.get("country_id"):
                    country_obj = get_country(int(player.get("country_id")))

                payload = {
                    "full_name": player.get("full_name").upper(),
                    "surname": player.get("surname").upper() if player.get("surname") else None,
                    "age": int(player.get("age")),
                    "position": player.get("position"),
                    "secondary_position": player.get("secondary_position") if player.get("secondary_position") else None,
                    "preferred_foot": player.get("preferred_foot"),
                    "overall": overall,
                    "shirt_number": int(player.get("shirt_number")),
                    "country": country_obj,
                    "height_cm": height,
                    "weight_kg": weight,
                    "fitness": 100,
                    "status": PlayerStatus.ACTIVE.value,
                    "potential": potential,
                    "salary_weekly": weekly,
                    "contract_until": months,
                    "current_club_id": club_id,
                }
                create_player(payload)
            except Exception as ex:
                page.open(ft.SnackBar(ft.Text(f"Valores inválidos: {ex}")))
                print(ex)
                page.update()
                return

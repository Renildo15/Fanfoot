from typing import List

import flet as ft

from app.db.models import Player
from app.services.club_service import get_club
from app.services.player_engine_stats_service import PlayerEngineStatsService
from app.utils.get_position import get_position


def _to_int_safe(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def players_table(players: List[Player], is_from_csv: bool = False):
    rows = []
    player_engine = PlayerEngineStatsService()
    club_cache: dict[int, str] = {}

    for player in players:
        full_name = ""
        club_name = "Livre"
        age = 0
        position = "Desconhecido"
        overall = 0
        potential = 0

        if is_from_csv:
            club_id = player.get("current_club_id") or None
            if club_id is not None and club_id != "":
                try:
                    club_id_int = int(club_id)
                except ValueError:
                    club_id_int = None
                if club_id_int:
                    if club_id_int in club_cache:
                        club_name = club_cache[club_id_int]
                    else:
                        try:
                            club_obj = get_club(club_id_int)
                            club_name = club_obj.name if club_obj else "Livre"
                        except Exception:
                            club_name = "Livre"
                        club_cache[club_id_int] = club_name

            full_name = player.get("full_name") or "Desconhecido"
            age = _to_int_safe(player.get("age"), 0)
            position = player.get("position") or "Desconhecido"
            overall = _to_int_safe(player.get("overall"), 0)
            potential = _to_int_safe(player.get("potential"), 0)

            if potential == 0:
                potential = player_engine.calculate_potential(overall, age, position)

            position_display = get_position(position)

        else:
            full_name = getattr(player, "full_name", "Desconhecido")
            age = getattr(player, "age", 0)
            position = getattr(player, "position", "Desconhecido")
            overall = getattr(player, "overall", 0)
            potential = getattr(player, "potential", 0)

            club_id = getattr(player, "current_club_id", None)
            if club_id:
                if club_id in club_cache:
                    club_name = club_cache[club_id]
                else:
                    try:
                        club_obj = get_club(club_id)
                        club_name = club_obj.name if club_obj else "Livre"
                    except Exception:
                        club_name = "Livre"
                    club_cache[club_id] = club_name
            else:
                club_name = "Livre"
            position_display = get_position(position)

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(full_name)),
                    ft.DataCell(ft.Text(str(age))),
                    ft.DataCell(ft.Text(position_display)),
                    ft.DataCell(ft.Text(str(overall))),
                    ft.DataCell(ft.Text(str(potential))),
                    ft.DataCell(ft.Text(club_name)),
                ]
            )
        )

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Idade")),
            ft.DataColumn(ft.Text("Posição")),
            ft.DataColumn(ft.Text("Overall")),
            ft.DataColumn(ft.Text("Potencial")),
            ft.DataColumn(ft.Text("Clube")),
        ],
        rows=rows,
    )

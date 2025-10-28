from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, select

from app.db.db import get_session
from app.db.models import (Country, Player, PlayerPreferredFoot, PlayerStatus,
                           Position)


class PlayerCreate(SQLModel):
    full_name: str
    surname: Optional[str]
    age: int
    position: Position
    secondary_position: Optional[Position]
    preferred_foot: PlayerPreferredFoot
    height_cm: int
    weight_kg: float
    overall: int
    potential: int
    fitness: int
    status: PlayerStatus
    shirt_number: int
    salary_weekly: float
    contract_until: int
    current_club_id: Optional[int]
    country: Optional[Country]


def create_player(data: PlayerCreate) -> Player:
    with get_session() as s:
        player = Player(**data)
        s.add(player)
        s.commit()
        s.refresh(player)

        return player


def list_players() -> List[Player]:
    with get_session() as s:
        stmt = select(Player)
        results = s.exec(stmt)
        players = results.all()
        return players


def get_player(player_id: int):
    with get_session() as s:
        stmt = (
            select(Player)
            .where(Player.id == player_id)
            .options(selectinload(Player.club))
            .options(selectinload(Player.country))
        )

        result = s.exec(stmt).first()
        return result
    
def delete_player(player_id:int):
    with get_session() as s:
        stmt = select(Player).where(Player.id == player_id)
        results = s.exec(stmt)
        player = results.one()

        s.delete(player)
        s.commit()
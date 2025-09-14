from sqlmodel import SQLModel
from typing import Optional, Tuple, List
from sqlmodel import select, col, or_, func
from app.db.db import get_session
from app.db.models import Coach


def list_coachs() -> List[Coach]:
    with get_session() as s:
        stmt = select(Coach)
        results = s.exec(stmt)
        coachs = results.all()
        # heroes = session.exec(select(Hero)).all() compact version
        return coachs
def get_coach(coach_id:int):
    with get_session() as s:
        return s.get(Coach, coach_id)
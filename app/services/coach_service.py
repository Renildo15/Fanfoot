from sqlmodel import SQLModel
from typing import Optional, Tuple, List
from sqlmodel import select, col, or_, func
from app.db.db import get_session
from app.db.models import Coach, CoachStyle

class CoachCreate(SQLModel):
    full_name: str
    surname: Optional[str]
    age: int = 35
    style: CoachStyle
    reputation: int
    experience: int
    salary_weekly: float
    contract_until: str 
    club_id: Optional[int]
    country_id: int

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
    
def create_coach(data: CoachCreate) -> Coach:
    with get_session() as s:
        coach = Coach(**data)
        s.add(coach)
        s.commit()
        s.refresh(coach)

        return coach
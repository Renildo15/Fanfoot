from sqlmodel import SQLModel
from typing import Optional, Tuple, List
from app.db.models import ClubFederation, Club
from app.db.db import get_session

class ClubCreate(SQLModel):
    name: str
    short_name: Optional[str] = None
    reputation: int = 0
    budget: float = 0.0
    wage_budget: float = 0.0
    federation: Optional[ClubFederation]
    crest_path: Optional[str]
    primary_color: Optional[str]
    secondary_color: Optional[str]
    league_id: Optional[int]               
    country_id: Optional[int]

def create_club(data: ClubCreate) -> Club:
    with get_session() as s:
        club = Club(**data)
        s.add(club)
        s.commit()
        s.refresh(club)
        return club
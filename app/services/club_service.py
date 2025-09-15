from typing import List, Optional, Tuple

from sqlmodel import SQLModel, col, func, or_, select

from app.db.db import get_session
from app.db.models import Club, ClubFederation


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
    competition_id: Optional[int]
    country_id: Optional[int]


def create_club(data: ClubCreate) -> Club:
    with get_session() as s:
        club = Club(**data)
        s.add(club)
        s.commit()
        s.refresh(club)
        return club


def get_club(club_id: int) -> Club:
    with get_session() as s:
        return s.get(Club, club_id)


def list_clubs(
    *,
    q: Optional[str] = None,
    country: Optional[str] = None,
    federation_: Optional[ClubFederation] = None,
    order_by: str = "reputation, name",
    limit: int = 50,
    offset: int = 0,
) -> Tuple[List[Club], int]:
    with get_session() as s:
        count_stmt = select(func.count()).select_from(Club)
        stmt = select(Club)

        if q:
            like = f"%{q}%"
            filter_condition = or_(Club.name.ilike(like), Club.country.ilike(like))
            count_stmt = count_stmt.where(filter_condition)
            stmt = stmt.where(filter_condition)

        if country:
            count_stmt = count_stmt.where(Club.country == country)
            stmt = stmt.where(Club.country == country)

        if federation_:
            count_stmt = count_stmt.where(Club.federation == federation_)
            stmt = stmt.where(Club.federation == federation_)

        total = s.scalar(count_stmt)

        order_clauses = []
        for key in [k.strip() for k in order_by.split(",") if k.strip()]:
            desc = key.startswith("-")
            field = key[1:] if desc else key
            if hasattr(Club, field):
                attr = getattr(Club, field)
                order_clauses.append(attr.desc() if desc else attr)

        if order_clauses:
            stmt = stmt.order_by(*order_clauses)
        stmt = stmt.offset(offset).limit(limit)

        items = list(s.scalars(stmt).all())

        return items, total

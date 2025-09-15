from typing import Iterable, List, Optional, Tuple

from sqlmodel import SQLModel, col, func, or_, select

from app.db.db import get_session
from app.db.models import Club, Competition, CompetitionType


class LeagueCreate(SQLModel):
    name: str
    type: CompetitionType
    country: Optional[str] = None
    level: int = 1
    max_teams: int = 0
    points_win: int = 3
    points_draw: int = 1
    points_lose: int = 0
    gd_first: int = 1
    logo_path: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None


class LeagueUpdate(SQLModel):
    name: Optional[str] = None
    type: Optional[CompetitionType] = None
    country: Optional[str] = None
    level: Optional[int] = None
    max_teams: Optional[int] = None
    points_win: Optional[int] = None
    points_draw: Optional[int] = None
    points_lose: Optional[int] = None
    gd_first: Optional[int] = None
    logo_path: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None


def create_league(data: LeagueCreate) -> Competition:
    with get_session() as s:
        league = Competition(**data)
        # breakpoint()
        s.add(league)
        s.commit()
        s.refresh(league)
        return league


def get_league(competition_id: int) -> Optional[Competition]:
    with get_session() as s:
        return s.get(Competition, competition_id)


def count_clubs(competition_id: int) -> int:
    with get_session() as s:
        return s.exec(select(Club).where(Club.competition_id == competition_id)).count()


def list_leagues(
    *,
    q: Optional[str] = None,
    country: Optional[str] = None,
    type_: Optional[CompetitionType] = None,
    level_min: Optional[int] = None,
    level_max: Optional[int] = None,
    order_by: str = "level, name",
    limit: int = 50,
    offset: int = 0,
) -> Tuple[List[Competition], int]:
    with get_session() as s:
        # Query para contar o total
        count_stmt = select(func.count()).select_from(Competition)

        # Query para obter os itens
        stmt = select(Competition)

        # Aplicar filtros em ambas as queries
        if q:
            like = f"%{q}%"
            filter_condition = or_(
                Competition.name.ilike(like), Competition.country.ilike(like)
            )
            count_stmt = count_stmt.where(filter_condition)
            stmt = stmt.where(filter_condition)

        if country:
            count_stmt = count_stmt.where(Competition.country == country)
            stmt = stmt.where(Competition.country == country)

        if type_:
            count_stmt = count_stmt.where(Competition.type == type_)
            stmt = stmt.where(Competition.type == type_)

        if level_min is not None:
            count_stmt = count_stmt.where(Competition.level >= level_min)
            stmt = stmt.where(Competition.level >= level_min)

        if level_max is not None:
            count_stmt = count_stmt.where(Competition.level <= level_max)
            stmt = stmt.where(Competition.level <= level_max)

        # Obter o total
        total = s.scalar(count_stmt)

        # Aplicar ordenação
        order_clauses = []
        for key in [k.strip() for k in order_by.split(",") if k.strip()]:
            desc = key.startswith("-")
            field = key[1:] if desc else key
            if hasattr(Competition, field):
                attr = getattr(Competition, field)
                order_clauses.append(attr.desc() if desc else attr)

        if order_clauses:
            stmt = stmt.order_by(*order_clauses)

        # Aplicar limite e offset
        stmt = stmt.offset(offset).limit(limit)

        # Executar a query e obter os resultados
        items = list(s.scalars(stmt).all())

        return items, total


def update_league(competition_id: int, data: LeagueUpdate) -> Optional[Competition]:
    with get_session() as s:
        league = s.get(Competition, competition_id)

        if not league:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(league, k, v)
        s.add(league)
        s.commit()
        s.refresh(league)
        return league


def delete_league(competition_id: int, *, force: bool = False) -> bool:
    with get_session() as s:
        league = s.get(Competition, competition_id)

        if not league:
            return False

        clubs = list(
            s.exec(select(Club).where(Club.competition_id == competition_id)).all()
        )
        if clubs and not force:
            return False

        if clubs and force:
            for c in clubs:
                c.competition_id = None
                s.add(c)
        s.delete(league)
        s.commit()

        return True

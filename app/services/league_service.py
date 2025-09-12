from typing import Iterable, Optional, Tuple, List
from sqlmodel import select, col, or_, func
from app.db.db import get_session
from app.db.models import League, LeagueType, Club
from sqlmodel import SQLModel

class LeagueCreate(SQLModel):
    name: str
    type: LeagueType
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
    type: Optional[LeagueType] = None
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


def create_league(data: LeagueCreate) -> League:
    with get_session() as s:
        league = League(**data)
        # breakpoint()
        s.add(league)
        s.commit()
        s.refresh(league)
        return league
    
def get_league(league_id: int) -> Optional[League]:
    with get_session() as s:
        return s.get(League, league_id)
    
def count_clubs(league_id: int) -> int:
    with get_session() as s:
        return s.exec(select(Club).where(Club.league_id == league_id)).count()
    
def list_leagues(
    *,
    q: Optional[str] = None,
    country: Optional[str] = None,
    type_: Optional[LeagueType] = None,
    level_min: Optional[int] = None,
    level_max: Optional[int] = None,
    order_by: str = "level, name",
    limit: int = 50,
    offset: int = 0,
) -> Tuple[List[League], int]:
    with get_session() as s:
        # Query para contar o total
        count_stmt = select(func.count()).select_from(League)
        
        # Query para obter os itens
        stmt = select(League)

        # Aplicar filtros em ambas as queries
        if q:
            like = f"%{q}%"
            filter_condition = or_(
                League.name.ilike(like),
                League.country.ilike(like)
            )
            count_stmt = count_stmt.where(filter_condition)
            stmt = stmt.where(filter_condition)
        
        if country:
            count_stmt = count_stmt.where(League.country == country)
            stmt = stmt.where(League.country == country)
        
        if type_:
            count_stmt = count_stmt.where(League.type == type_)
            stmt = stmt.where(League.type == type_)
        
        if level_min is not None:
            count_stmt = count_stmt.where(League.level >= level_min)
            stmt = stmt.where(League.level >= level_min)
        
        if level_max is not None:
            count_stmt = count_stmt.where(League.level <= level_max)
            stmt = stmt.where(League.level <= level_max)

        # Obter o total
        total = s.scalar(count_stmt)

        # Aplicar ordenação
        order_clauses = []
        for key in [k.strip() for k in order_by.split(",") if k.strip()]:
            desc = key.startswith("-")
            field = key[1:] if desc else key
            if hasattr(League, field):
                attr = getattr(League, field)
                order_clauses.append(attr.desc() if desc else attr)
        
        if order_clauses:
            stmt = stmt.order_by(*order_clauses)

        # Aplicar limite e offset
        stmt = stmt.offset(offset).limit(limit)
        
        # Executar a query e obter os resultados
        items = list(s.scalars(stmt).all())
        
        return items, total
    
def update_league(league_id: int, data:LeagueUpdate) -> Optional[League]:
    with get_session() as s:
        league = s.get(League, league_id)

        if not league:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(league, k, v)
        s.add(league)
        s.commit()
        s.refresh(league)
        return league

def delete_league(league_id: int, *, force: bool = False) -> bool:
    with get_session() as s:
        league = s.get(League, league_id)

        if not league:
            return False
        
        clubs = list(s.exec(select(Club).where(Club.league_id == league_id)).all())
        if clubs and not force:
            return False
        
        if clubs and force:
            for c in clubs:
                c.league_id = None
                s.add(c)
        s.delete(league)
        s.commit()

        return True
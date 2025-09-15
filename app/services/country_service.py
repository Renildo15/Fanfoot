from typing import List, Optional, Tuple

from sqlmodel import SQLModel, col, or_, select

from app.db.db import get_session
from app.db.models import Country


class CountryCreate(SQLModel):
    code: str
    name: str
    flag: str


def create_country(data: CountryCreate):
    with get_session() as s:
        country = Country(**data)
        s.add(country)
        s.commit()
        s.refresh(country)
        return country


def get_countries_count():
    with get_session() as s:
        countries = s.exec(select(Country)).all()
        return len(countries)


def get_countries(q: Optional[str] = None) -> List[Country]:
    with get_session() as s:
        stmt = select(Country)

        if q:
            like = f"%{q}%"
            stmt = stmt.where(
                or_(col(Country.name).ilike(like), col(Country.code).ilike(like))
            )

        stmt = stmt.order_by(Country.name)

        items = list(s.exec(stmt).all())
        return items


def get_country(country_id: int) -> Country:
    with get_session() as s:
        return s.get(Country, country_id)

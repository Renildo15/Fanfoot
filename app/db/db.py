from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

DB_FILE = Path("data/footfantasy.db")
DB_FILE.parent.mkdir(exist_ok=True, parents=True)

engine = create_engine(
    f"sqlite:///{DB_FILE}",
    echo=False,
    connect_args={"check_same_thread": False},
)


def init_db():
    from app.db import models

    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)

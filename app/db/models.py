from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
import enum

class Position(str, enum.Enum):
    GK = "GK"
    RB = "RB"
    LB = "LB"
    CB = "CB"
    RWB = "RWB"
    LWB = "LWB"
    CDM = "CDM"
    CM = "CM"
    CAM = "CAM"
    RM = "RM"
    LM = "LM"
    RW = "RW"
    LW = "LW"
    CF = "CF"
    ST = "ST"

class PlayerPreferredFoot(str, enum.Enum):
    R="R"
    L="L"
    B="B"

class PlayerStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INJURED = "INJURED"
    SUSPENDED = "SUSPENDED"
    ACADEMY = "ACADEMY"
    RETIRED = "RETIRED"

class LeagueType(str, enum.Enum):
    LEAGUE = "LEAGUE" 
    CUP = "CUP"

class ClubFederation(str, enum.Enum):
    FHV = "FHV"
    FRF = "FRF"
    FMH = "FMH"

class Country(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    flag: str
    
    # FIXED: Use SQLModel's relationship syntax without List annotation
    leagues: list["League"] = Relationship(back_populates="country")
    clubs: list["Club"] = Relationship(back_populates="country")
    players: list["Player"] = Relationship(back_populates="country")

class League(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: LeagueType = Field(sa_column_kwargs={"nullable": False})
    level: int = 1
    max_teams: int = Field(default=0)
    points_win: int = 3
    points_draw: int = 1
    points_lose: int = 0
    gd_first: int = 1

    logo_path: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None    

    country_id: Optional[int] = Field(default=None, foreign_key="country.id")
    country: Optional[Country] = Relationship(back_populates="leagues")

    clubs: list["Club"] = Relationship(back_populates="league")
    player_stats: list["PlayerStatsSeason"] = Relationship(back_populates="competition")

class Club(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    short_name: Optional[str] = None
    reputation: int = 0
    budget: float = 0.0
    wage_budget: float = 0.0
    federation: Optional[ClubFederation] = Field(sa_column_kwargs={"nullable": True})

    crest_path: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None

    league_id: Optional[int] = Field(default=None, foreign_key="league.id")
    league: Optional[League] = Relationship(back_populates="clubs")

    country_id: Optional[int] = Field(default=None, foreign_key="country.id")
    country: Optional[Country] = Relationship(back_populates="clubs")

    players: list["Player"] = Relationship(back_populates="club")
    player_stats: list["PlayerStatsSeason"] = Relationship(back_populates="club")

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(index=True)
    surname: Optional[str] = None
    age: int = 16
    position: Position = Field(sa_column_kwargs={"nullable": False})
    secondary_position: Optional[Position] = Field(sa_column_kwargs={"nullable": True})
    preferred_foot: PlayerPreferredFoot = Field(sa_column_kwargs={"nullable": False})
    height_cm: int = 170
    weight_kg: int = 70
    overall: int = 50
    potential: int = 50
    morale: int = 40
    fitness: int = 100
    status: PlayerStatus = Field(default=PlayerStatus.ACTIVE, sa_column_kwargs={"nullable": False})
    shirt_number: int = 0
    salary_weekly: float = 0.0
    contract_until: str = "2030-06-30"

    current_club_id: Optional[int] = Field(default=None, foreign_key="club.id")
    club: Optional[Club] = Relationship(back_populates="players")

    country_id: int = Field(default=None, foreign_key="country.id")
    country: Optional[Country] = Relationship(back_populates="players")

    stats: list["PlayerStatsSeason"] = Relationship(back_populates="player")

class PlayerStatsSeason(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="player.id")
    club_id: Optional[int] = Field(default=None, foreign_key="club.id")
    competition_id: Optional[int] = Field(default=None, foreign_key="league.id")
    season_year: int
    matches_played: int = 0
    goals: int = 0
    assists: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    avg_rating: float = 0.0

    player: Player = Relationship(back_populates="stats")
    club: Optional[Club] = Relationship(back_populates="player_stats")
    competition: Optional[League] = Relationship(back_populates="player_stats")
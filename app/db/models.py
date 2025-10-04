import enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class CoachStyle(str, enum.Enum):
    OFFENSIVE = "OFFENSIVE"
    DEFENSIVE = "DEFENSIVE"
    BALANCED = "BALANCED"
    COUNTER_ATTACK = "COUNTER_ATTACK"
    POSSESSION = "POSSESSION"
    PRESSING = "PRESSING"


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
    R = "R"
    L = "L"
    B = "B"


class PlayerStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INJURED = "INJURED"
    SUSPENDED = "SUSPENDED"
    ACADEMY = "ACADEMY"
    RETIRED = "RETIRED"


class CompetitionType(str, enum.Enum):
    LEAGUE = "LEAGUE"
    CUP = "CUP"
    LEAGUE_KNOCKOUT = "LEAGUE & KNOCKOUT"


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
    competitions: list["Competition"] = Relationship(back_populates="country")
    clubs: list["Club"] = Relationship(back_populates="country")
    players: list["Player"] = Relationship(back_populates="country")
    coach: Optional["Coach"] = Relationship(
        back_populates="country", sa_relationship_kwargs={"uselist": False}
    )


class Competition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: CompetitionType = Field(sa_column_kwargs={"nullable": False})
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
    country: Optional[Country] = Relationship(back_populates="competitions")

    club_associations: list["ClubCompetition"] = Relationship(
        back_populates="competition"
    )
    player_stats: list["PlayerStatsSeason"] = Relationship(back_populates="competition")

    @property
    def clubs(self):
        return [assoc.club for assoc in self.club_associations]


class Club(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    short_name: Optional[str] = None
    reputation: int = 0
    budget: float = 0.0
    wage_budget: float = 0.0
    federation: Optional[ClubFederation] = Field(sa_column_kwargs={"nullable": True})
    stadium: Optional[str] = None

    crest_path: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None

    # competition_id: Optional[int] = Field(default=None, foreign_key="competition.id")
    # competition: Optional[Competition] = Relationship(back_populates="clubs")

    country_id: Optional[int] = Field(default=None, foreign_key="country.id")
    country: Optional[Country] = Relationship(back_populates="clubs")

    competition_associations: list["ClubCompetition"] = Relationship(
        back_populates="club"
    )
    players: list["Player"] = Relationship(back_populates="club")
    player_stats: list["PlayerStatsSeason"] = Relationship(back_populates="club")

    coach: Optional["Coach"] = Relationship(
        back_populates="club", sa_relationship_kwargs={"uselist": False}
    )
    coach_history: list["CoachHistory"] = Relationship(back_populates="club")

    @property
    def competitions(self):
        return [assoc.competition for assoc in self.competition_associations]

    @property
    def current_coach(self):
        return self.coach


class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(index=True)
    surname: Optional[str] = None
    age: int = 16
    position: Position = Field(sa_column_kwargs={"nullable": False})
    secondary_position: Optional[Position] = Field(sa_column_kwargs={"nullable": True})
    preferred_foot: PlayerPreferredFoot = Field(sa_column_kwargs={"nullable": False})
    height_cm: int = 170 #gerar de forma aleatoria
    weight_kg: int = 70 #gerar de forma aleatoria
    overall: int = 50 #gerar de forma aleatoria e manual
    potential: int = 50 #gerar de forma aleatoria somente para jovens
    morale: int = 40 #gerar de forma aleatoria
    fitness: int = 100
    status: PlayerStatus = Field(
        default=PlayerStatus.ACTIVE, sa_column_kwargs={"nullable": False}
    )
    shirt_number: int = 0
    salary_weekly: float = 0.0 #gerar de forma aleatoria
    contract_until: str = "2030-06-30" #gerar de forma aleatoria

    current_club_id: Optional[int] = Field(default=None, foreign_key="club.id")
    club: Optional[Club] = Relationship(back_populates="players")

    country_id: int = Field(default=None, foreign_key="country.id")
    country: Optional[Country] = Relationship(back_populates="players")

    stats: list["PlayerStatsSeason"] = Relationship(back_populates="player")


class PlayerStatsSeason(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="player.id")
    club_id: Optional[int] = Field(default=None, foreign_key="club.id")
    competition_id: Optional[int] = Field(default=None, foreign_key="competition.id")
    season_year: int
    matches_played: int = 0
    goals: int = 0
    assists: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    avg_rating: float = 0.0

    player: Player = Relationship(back_populates="stats")
    club: Optional[Club] = Relationship(back_populates="player_stats")
    competition: Optional[Competition] = Relationship(back_populates="player_stats")


class ClubCompetition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    club_id: int = Field(foreign_key="club.id")
    competition_id: int = Field(foreign_key="competition.id")
    season_year: int = Field(default=2024)  # Ano da temporada

    # Relações (opcionais, mas úteis para acesso)
    club: Optional["Club"] = Relationship(back_populates="competition_associations")
    competition: Optional["Competition"] = Relationship(
        back_populates="club_associations"
    )


class Coach(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(index=True)
    surname: Optional[str] = None
    age: int = 35
    style: CoachStyle = Field(default=CoachStyle.BALANCED)
    reputation: int = Field(default=50, ge=1, le=100)  # 1-100
    experience: int = Field(default=1, ge=0)  # Anos de experiência
    salary_weekly: float = Field(default=0.0)
    contract_until: str = Field(default="2025-06-30")

    # Relação One-to-One com Club (um técnico para um clube)
    club_id: Optional[int] = Field(default=None, foreign_key="club.id", unique=True)
    club: Optional["Club"] = Relationship(back_populates="coach")

    country_id: int = Field(default=None, foreign_key="country.id")
    country: Optional[Country] = Relationship(back_populates="coach")

    # Histórico de clubes (Many-to-Many)
    club_history: list["CoachHistory"] = Relationship(back_populates="coach")


class CoachHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    coach_id: int = Field(foreign_key="coach.id")
    club_id: int = Field(foreign_key="club.id")
    season_start: int = Field(default=2024)
    season_end: Optional[int] = Field(default=None)  # None se ainda estiver no clube
    matches: int = Field(default=0)
    wins: int = Field(default=0)
    draws: int = Field(default=0)
    losses: int = Field(default=0)

    coach: Coach = Relationship(back_populates="club_history")
    club: "Club" = Relationship(back_populates="coach_history")


from app.db.models import LeagueType

def get_type_value(value):
    match value:
        case LeagueType.LEAGUE.value:
            return "Liga"
        case LeagueType.CUP.value:
            return "Copa"
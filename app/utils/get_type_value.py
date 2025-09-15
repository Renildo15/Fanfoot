from app.db.models import CompetitionType


def get_type_value(value):
    match value:
        case CompetitionType.LEAGUE.value:
            return "Liga"
        case CompetitionType.CUP.value:
            return "Copa"

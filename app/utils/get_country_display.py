from app.services.country_service import get_country

def get_country_display(country_id:int):
    country = get_country(country_id)

    if not country:
        return "N/A"
    return country.name
import requests

from app.services.country_service import create_country, get_countries_count


def fetch_countries():
    resp = requests.get("https://restcountries.com/v3.1/all?fields=flags,cca2,name")
    data = resp.json()

    return [
        {
            "code": c["cca2"].lower(),
            "name": c["name"]["common"],
            "flag": c["flags"]["png"],
        }
        for c in data
    ]


countries_count = get_countries_count()
countries = fetch_countries()

if countries_count <= 1:
    for country in countries:
        create_country(country)
        print(f"{country} adicionado!")

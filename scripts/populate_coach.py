import csv
from app.services.club_service import get_club
from app.services.country_service import get_country
from app.services.coach_service import create_coach
from app.db.models import CoachStyle

def reader_csv():
    with open("./data/coach_csv.csv", 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        csv_data = list(csv_reader)

        for coach_data in csv_data:
            try:
                # Verificar se o clube existe
                club_id = int(coach_data['club_id'])
                club = get_club(club_id)
                if not club:
                    print(f"Clube com ID {club_id} não encontrado. Pulando técnico {coach_data['full_name']}")
                    continue

                # Verificar se o país existe
                country_id = int(coach_data['country_id'])
                country = get_country(country_id)
                if not country:
                    print(f"País com ID {country_id} não encontrado. Pulando técnico {coach_data['full_name']}")
                    continue

                # Converter o estilo para o enum
                try:
                    style = CoachStyle(coach_data["style"])
                except ValueError:
                    print(f"Estilo inválido: {coach_data['style']}. Usando padrão BALANCED")
                    style = CoachStyle.BALANCED

                payload = {
                    "full_name": coach_data["full_name"],
                    "surname": coach_data["surname"],
                    "age": int(coach_data["age"]),
                    "style": style,
                    "reputation": int(coach_data["reputation"]),
                    "experience": int(coach_data["experience"]),
                    "salary_weekly": float(coach_data["salary_weekly"]),
                    "contract_until": coach_data.get("contract_until", "2025-06-30"),
                    "club_id": club_id,  # ✅ APENAS O ID, não o objeto
                    "country_id": country_id  # ✅ APENAS O ID, não o objeto
                }
                
                create_coach(payload)
                print(f"Técnico {coach_data['full_name']} salvo com sucesso!")
                
            except Exception as e:
                print(f"Erro ao processar técnico {coach_data.get('full_name', 'N/A')}: {e}")
                continue

reader_csv()
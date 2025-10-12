import random
from typing import Dict, Tuple

from app.db.models import Position


class PlayerEngineStatsService:
    PROFILES: Dict[str, Tuple[int, int]] = {
        "GK": (185, 200),
        "RB": (170, 185),
        "LB": (170, 185),
        "CB": (170, 196),
        "RWB": (170, 185),
        "LWB": (170, 185),
        "CDM": (170, 190),
        "CM": (170, 190),
        "RM": (170, 190),
        "LM": (170, 190),
        "RW": (170, 190),
        "LW": (170, 190),
        "CF": (165, 185),
        "ST": (165, 185),
        "DEFAULT": (160, 200),
    }

    IMC_RANGES: Dict[str, Tuple[float, float]] = {
        "GK": (23.5, 26.0),
        "CB": (23.0, 25.5),
        "RB": (22.0, 24.5),
        "LB": (22.0, 24.5),
        "RWB": (22.0, 24.0),
        "LWB": (22.0, 24.0),
        "CDM": (22.5, 24.5),
        "CM": (22.0, 24.0),
        "CAM": (21.5, 23.5),
        "RM": (21.0, 23.5),
        "LM": (21.0, 23.5),
        "RW": (21.0, 23.0),
        "LW": (21.0, 23.0),
        "CF": (21.5, 23.5),
        "ST": (22.0, 24.0),
        "DEFAULT": (21.5, 24.5),
    }

    PEAK_AGE = {
        "GK": 30,
        "CB": 28,
        "LB": 28,
        "RB": 28,
        "LWB": 28,
        "RWB": 28,
        "CDM": 27,
        "CM": 27,
        "CAM": 27,
        "LM": 27,
        "RM": 27,
        "LW": 26,
        "RW": 26,
        "CF": 26,
        "ST": 26,
    }

    def _choice_height(self, position: Position) -> int:
        pos = position.upper()
        low, high = self.PROFILES.get(pos, self.PROFILES["DEFAULT"])
        return random.choice(range(low, high + 1))

    def _generate_weight(self, height_cm: int, position: Position) -> float:
        height_m = height_cm / 100
        low, high = self.IMC_RANGES.get(position.upper(), self.IMC_RANGES["DEFAULT"])
        imc = random.uniform(low, high)
        weight = imc * (height_m**2)

        return round(weight, 1)

    def get_height_and_weight(self, position: Position) -> Tuple[int, float]:
        player_height = self._choice_height(position)
        player_weight = self._generate_weight(player_height, position)

        return int(player_height), float(player_weight)

    def calculate_potential(self, overall: int, age: int, position: str) -> int:
        pos = position.upper()
        factor_evolution = list(range(2, 6))
        peak_age = self.PEAK_AGE.get(pos, 27)

        years_to_peak = max(peak_age - age, 0)
        max_margin = years_to_peak * random.choice(factor_evolution)

        potential = overall + max_margin

        potential += random.randint(0, 3)

        potential = min(potential, 99)

        return potential

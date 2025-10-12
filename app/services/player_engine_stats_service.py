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

    SALARY_CONFIG = {
        "min_weekly": 200,  # salário mínimo semanal (unidade genérica)
        "max_weekly": 250_000,  # teto plausível semanal (ajuste se quiser)
        "base_overall_min": 40,  # overall mínimo esperado
        "base_overall_max": 99,  # overall máximo esperado
        # multiplicador por posição
        "position_multiplier": {
            "GK": 1.05,
            "CB": 1.00,
            "LB": 0.95,
            "RB": 0.95,
            "LWB": 0.95,
            "RWB": 0.95,
            "CDM": 1.00,
            "CM": 1.00,
            "CAM": 1.05,
            "RM": 0.98,
            "LM": 0.98,
            "RW": 1.05,
            "LW": 1.05,
            "CF": 1.10,
            "ST": 1.10,
            "DEFAULT": 1.0,
        },
        # bonus por nível de promessa: multiplica a diferença até o teto
        "promise_multiplier": {
            "low": 0.9,
            "normal": 1.0,
            "high": 1.15,
            "star": 1.30,  # prodígio
        },
        # ajuste de idade (reduz leve salário para muito jovem; aumenta para experientes)
        "age_modifier": lambda age: 0.9 if age <= 17 else (1.15 if age >= 30 else 1.0),
    }

    CONTRACT_CONFIG = {
        # meses mínimos e máximos de contrato
        "min_months": 1,
        "max_months": 84,  # 7 anos
        # regras: jovens recebem contratos mais longos, veteranos mais curtos
        "years_for_youth_long": 4,  # base years for youth
        "age_young_threshold": 22,
        "age_old_threshold": 30,
        # chance de contrato extra (assinatura premium) para estrelas
        "star_extra_months": 24,
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

    def generate_overall(self, age: int) -> int:
        min_overall = max(50, age * 2)
        max_overall = min(age * 3 + 20, 99)

        overall = random.randint(min_overall, max_overall)

        return overall

    def _generate_weekly_salary(
        self,
        overall: int,
        age: int,
        position: Position,
        promise: str = "normal",
        config: dict = SALARY_CONFIG,
    ) -> float:
        """
        Retorna salário semanal (int) baseado em overall, idade, posição e categoria 'promise'.
        'promise' deve ser uma das keys em SALARY_CONFIG["promise_multiplier"].
        """
        pos = position.upper()
        pm = config["position_multiplier"].get(
            pos, config["position_multiplier"]["DEFAULT"]
        )
        prom_mult = config["position_multiplier"].get(promise, 1.0)

        low = config["base_overall_min"]
        high = config["base_overall_max"]
        norm = max(0.0, min(1.0, (overall - low) / (high - low)))

        base_salary = config["min_weekly"] + norm * (
            config["max_weekly"] - config["min_weekly"]
        )

        age_mod = config["age_modifier"](age)
        salary = base_salary * pm * prom_mult * age_mod

        variation = random.uniform(0.95, 1.05)
        salary *= variation

        salary = float(
            max(config["min_weekly"], min(config["max_weekly"], round(salary)))
        )

        return salary

    def _generate_contract_length(
        self,
        overall: int,
        age: int,
        promise: str = "normal",
        config: dict = CONTRACT_CONFIG,
    ) -> int:
        """
        Retorna duração do contrato em meses.
        Estratégia simples:
        - Jogadores jovens (< threshold) recebem contratos mais longos (3-5 anos)
        - Idade normal (threshold..old) recebe contratos médios (1-4 anos)
        - Jogadores velhos recebem contratos curtos (6-24 meses)
        - Jogadores 'star' ou com very high overall podem ganhar contratos maiores e/ou extensão
        """
        # base em meses dependendo da idade
        if age <= config["age_young_threshold"]:
            base_years = config["years_for_youth_long"]
            # para muito jovens, dar entre base_years e base_years+2 anos (em meses)
            months = random.randint(base_years * 12, (base_years + 2) * 12)
        elif age >= config["age_old_threshold"]:
            # veteranos: 6 a 24 meses
            months = random.randint(6, 24)
        else:
            # adultos em carreira: 12 a 60 meses (1 a 5 anos)
            months = random.randint(12, 60)

        # se promessa for 'high' ou 'star', aumenta chance de contrato longo
        if promise == "high":
            months = int(months * 1.15)
        elif promise == "star":
            months = int(months * 1.4) + config["star_extra_months"]

        # se overall muito alto, extender levemente
        if overall >= 85:
            months = int(months * 1.25)
        elif overall >= 75:
            months = int(months * 1.08)

        # clamp
        months = max(config["min_months"], min(config["max_months"], months))
        return months

    def generate_salary_and_contract(
        self, overall: int, age: int, position: Position = "DEFAULT", promise: str = "normal"
    ) -> Tuple[float, int]:
        weekly = self._generate_weekly_salary(overall, age, position, promise)
        months = self._generate_contract_length(overall, age, promise)
        return weekly, months

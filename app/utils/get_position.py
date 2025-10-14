from app.db.models import Position


def get_position(position: Position) -> str:
    match position:
        case Position.GK:
            return "Goleiro"
        case Position.RB:
            return "Lateral Direito"
        case Position.LB:
            return "Lateral Esquerdo"
        case Position.CB:
            return "Zagueiro Central"
        case Position.RWB:
            return "Lateral Direito"
        case Position.LWB:
            return "Lateral Esquerdo"
        case Position.CDM:
            return "Volante"
        case Position.CM:
            return "Meio-Campo Central"
        case Position.CAM:
            return "Meia Ofensivo"
        case Position.RM:
            return "Meio-Campo Direito"
        case Position.LM:
            return "Meio-Campo Esquerdo"
        case Position.RW:
            return "Ponta Direita"
        case Position.LW:
            return "Ponta Esquerda"
        case Position.CF:
            return "Centroavante"
        case Position.ST:
            return "Atacante"
        case _:
            return "Desconhecido"


def get_position_from_ptbr(position_pt: str) -> Position | None:
    match position_pt.lower():
        case "goleiro":
            return Position.GK.value
        case "lateral direito":
            return Position.RB.value
        case "lateral esquerdo":
            return Position.LB.value
        case "zagueiro central":
            return Position.CB.value
        case "lateral direito":
            return Position.RWB.value
        case "lateral esquerdo":
            return Position.LWB.value
        case "volante":
            return Position.CDM.value
        case "meio-campo central":
            return Position.CM.value
        case "meia ofensivo":
            return Position.CAM.value
        case "meio-campo direito":
            return Position.RM.value
        case "meio-campo esquerdo":
            return Position.LM
        case "ponta direita":
            return Position.RW.value
        case "ponta esquerda":
            return Position.LW.value
        case "centroavante":
            return Position.CF.value
        case "atacante":
            return Position.ST.value
        case _:
            return None

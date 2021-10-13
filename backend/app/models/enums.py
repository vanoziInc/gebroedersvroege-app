from enum import  Enum


class GenderEnum(str, Enum):
    stier = 'stier'
    vaars = 'vaars'

class BreedEnum(str, Enum):
    zwart_bont = 'zwart bont'
    belgisch_blauw ='belgisch blauw'
    rood_bont = 'rood bont'

class BirthProcessEnum(str, Enum):
    vlot = 'vlot'
    normaal = 'normaal'
    zwaar = 'zwaar'

class FirstMilkEnum(str, Enum):
    ochtend = "'s ochtends"
    middag = "'s middags"
    avond = "'s avonds"
    volgende_dag = 'volgende dag'

class DischargeReasonEnum(str, Enum):
    kalver_handelaar = "kalver_handelaar"
    schietmasker = "schietmasker"
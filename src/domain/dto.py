from dataclasses import dataclass

@dataclass
class CurrencyDTO:
    code: str
    name: str
    sign: str

@dataclass
class ExchangeRateDTO:
    base_id: int
    target_id: int
    rate: float
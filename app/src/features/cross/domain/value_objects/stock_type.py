from enum import Enum


class StockType(Enum):
    """
    Enum representing different types of stocks.
    """
    ON = "ON"
    PN = "PN"
    PNA = "PNA"
    PNB = "PNB"
    PNC = "PNC"
    PND = "PND"
    UNIT = "UNIT"
    BDR = "BDR"
    ETF = "ETF"
    FII = "FII"
    OTHER = "OTHER"

    @property
    def description(self) -> str:
        """
        Provides a human-readable description of the stock type.
        """
        descriptions = {
            "ON": "Ordinary shares — voting rights",
            "PN": "Preferred shares — preference in dividends",
            "PNA": "Class A Preferred",
            "PNB": "Class B Preferred",
            "PNC": "Class C Preferred",
            "PND": "Class D Preferred",
            "UNIT": "Unit Shares — combination of different classes",
            "BDR": "BDRs — Brazilian Depositary Receipts",
            "ETF": "ETFs — Exchange Traded Funds",
            "FII": "FIIs — Real Estate Investment Funds",
            "OTHER": "Other types of stocks or assets",
        }
        
        return descriptions[self.value]

    @classmethod
    def from_ticker_suffix(cls, suffix: str) -> dict[str, "StockType"]:
        """
        Determines the stock type based on the ticker suffix.
        """
        mapping = {
            "3": cls.ON,
            "4": cls.PN,
            "5": cls.PNA,
            "6": cls.PNB,
            "7": cls.PNC,
            "8": cls.PND,
            "11": cls.UNIT,  # Can be UNIT, ETF or FII — needs to be validated by the asset
            "34": cls.BDR,
        }
        try:
            return mapping[suffix]
        except KeyError:
            raise ValueError(f"Sufixo de ticker inválido: {suffix}")

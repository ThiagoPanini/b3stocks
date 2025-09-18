from dataclasses import dataclass


@dataclass(frozen=True)
class VariationThreshold:
    """
    Represents variation thresholds for a stock.

    Attributes:
        upper_bound (float): Upper bound for stock variation notifications (e.g. 0.02 for +2% variation).
        lower_bound (float): Lower bound for stock variation notifications (e.g. 0.02 for -2% variation).
    """

    upper_bound: float
    lower_bound: float

    def __post_init__(self):  # type: ignore[override]
        # Basic validation: thresholds must be positive numbers
        if self.upper_bound <= 0 or self.lower_bound <= 0:
            raise ValueError("upper_bound and lower_bound must be > 0")

from enum import Enum
from datetime import timezone, timedelta


class Timezone(Enum):
    """
    Enum representing different timezones
    """
    UTC = timezone.utc
    SAO_PAULO = timezone(timedelta(hours=-3))
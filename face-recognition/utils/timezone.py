from datetime import datetime
import pytz
from dateutil import parser

TZ = pytz.timezone('Asia/Ho_Chi_Minh')


def parse_to_utc_naive(ts: str) -> datetime | None:
    """Parse a timestamp string to a UTC-naive datetime suitable for DB storage/queries.

    Behavior:
    - If ts is None or empty -> return None
    - Use dateutil.parser to parse the string. If parsed datetime is naive, assume it's in Asia/Ho_Chi_Minh and convert to UTC.
    - Return a naive datetime in UTC (tzinfo removed) to match existing DB conventions.
    """
    if not ts:
        return None
    try:
        dt = parser.parse(ts)
    except Exception:
        return None

    if dt.tzinfo is None:
        # assume local (Asia/Ho_Chi_Minh)
        dt_local = TZ.localize(dt)
    else:
        dt_local = dt.astimezone(TZ)

    dt_utc = dt_local.astimezone(pytz.utc)
    # return naive UTC datetime to match repository usage
    return dt_utc.replace(tzinfo=None)

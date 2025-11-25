from datetime import datetime
from db.nguoi_repository import NguoiRepository
from utils.timezone import parse_to_utc_naive, TZ
from dateutil import parser

nguoi_repo = NguoiRepository()


def _parse_to_local_date(s: str):
    if not s:
        return None
    try:
        dt = parser.parse(s)
    except Exception:
        return None
    # If naive assume local TZ; otherwise convert to local
    if dt.tzinfo is None:
        dt_local = TZ.localize(dt)
    else:
        dt_local = dt.astimezone(TZ)
    return dt_local.date()


def query_checklogs_service(date: str = None, date_from: str = None, date_to: str = None, user_id: int = None, status: str = None, limit: int = 100, offset: int = 0):
    try:
        date_parsed = _parse_to_local_date(date)
        date_from_parsed = _parse_to_local_date(date_from)
        date_to_parsed = _parse_to_local_date(date_to)

        rows = nguoi_repo.query_checklogs(date=date_parsed, date_from=date_from_parsed, date_to=date_to_parsed, full_name=None, user_id=user_id, status=status, limit=limit, offset=offset)
        result = [r.__dict__ for r in rows]
        # Convert datetime values in dicts to ISO strings
        for item in result:
            if isinstance(item.get('check_in'), datetime):
                item['check_in'] = item['check_in'].isoformat()
            if isinstance(item.get('check_out'), datetime):
                item['check_out'] = item['check_out'].isoformat()
        return {"success": True, "total": len(result), "checklogs": result}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi truy vấn checklog: {e}", "status_code": 500}

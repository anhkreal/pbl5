from db.nguoi_repository import NguoiRepository
from datetime import datetime, time
import pytz

# timezone for Vietnam (UTC+7)
TZ = pytz.timezone('Asia/Ho_Chi_Minh')

nguoi_repo = NguoiRepository()


def checkin_service(user_id: int, edited_by: int = None, note: str = None):
    """Create a check-in for user_id. Determine lateness based on shift:
    - 'day' shift cutoff: 06:00 local
    - 'night' shift cutoff: 14:00 local

    Store check_in datetime (UTC) and return the created record id and status.
    """
    try:
        user = nguoi_repo.get_by_id(int(user_id))
        if not user:
            return {"success": False, "message": "Không tìm thấy user", "status_code": 404}

        shift = getattr(user, 'shift', 'day')

        # use local time (UTC+7) for cutoff comparison
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        now_local = now_utc.astimezone(TZ)

        # Prevent duplicate check-in: if there's already a checklog for this user on the local date, do not insert
        existing = nguoi_repo.find_checklog_by_user_and_date(user_id=int(user_id), date_only=now_local.date())
        if existing:
            # Return conflict - already checked in for today
            return {"success": False, "message": "Đã tồn tại check-in cho user này vào ngày hôm nay", "status_code": 409}

        if shift == 'night':
            cutoff = time(14, 0, 0)  # local 14:00
        else:
            cutoff = time(6, 0, 0)  # local 06:00

        status = 'on_time' if now_local.time() <= cutoff else 'late'

        # store check_in as UTC timestamp
        rowid = nguoi_repo.add_checkin(user_id=int(user_id), shift=shift, status=status, edited_by=edited_by, note=note)
        if rowid:
            return {"success": True, "id": rowid, "status": status}
        else:
            return {"success": False, "message": "Không thể tạo check-in", "status_code": 500}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi tạo check-in: {e}", "status_code": 500}

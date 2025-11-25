from db.nguoi_repository import NguoiRepository
from db.models import Nguoi
from datetime import datetime

nguoi_repo = NguoiRepository()


def edit_users_service(user_id: int, data: dict, avatar_bytes: bytes = None):
    try:
        existing = nguoi_repo.get_by_id(user_id)
        if not existing:
            return {"success": False, "message": "Không tìm thấy người", "status_code": 404}

        # Update allowed fields if present in data
        for field in ['full_name', 'age', 'address', 'phone', 'gender', 'role', 'shift', 'status', 'pin']:
            if field in data:
                setattr(existing, field, data[field])

        if avatar_bytes is not None:
            existing.avatar_url = avatar_bytes

        existing.updated_at = None
        affected = nguoi_repo.update_by_id(user_id, existing)
        if affected > 0:
            return {"success": True, "message": "Cập nhật thành công"}
        else:
            return {"success": False, "message": "Không thể cập nhật", "status_code": 500}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi cập nhật: {e}", "status_code": 500}

from db.nguoi_repository import NguoiRepository
from datetime import datetime

nguoi_repo = NguoiRepository()


def update_avatar_service(user_id: int, avatar_bytes: bytes):
    try:
        existing = nguoi_repo.get_by_id(user_id)
        if not existing:
            return {"success": False, "message": "Không tìm thấy người", "status_code": 404}

        existing.avatar_url = avatar_bytes
        existing.updated_at = None
        affected = nguoi_repo.update_by_id(user_id, existing)
        if affected > 0:
            return {"success": True, "message": "Cập nhật ảnh đại diện thành công"}
        else:
            return {"success": False, "message": "Không thể cập nhật ảnh đại diện", "status_code": 500}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi cập nhật avatar: {e}", "status_code": 500}

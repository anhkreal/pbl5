from db.nguoi_repository import NguoiRepository

nguoi_repo = NguoiRepository()


def resign_user_service(user_id: int):
    try:
        existing = nguoi_repo.get_by_id(user_id)
        if not existing:
            return {"success": False, "message": "Không tìm thấy người", "status_code": 404}

        # if already resigned, return idempotent success
        if getattr(existing, 'status', None) == 'resigned':
            return {"success": True, "message": "Nhân viên đã nghỉ việc"}

        existing.status = 'resigned'
        existing.updated_at = None
        affected = nguoi_repo.update_by_id(user_id, existing)
        if affected > 0:
            return {"success": True, "message": "Cập nhật trạng thái: resigned"}
        else:
            return {"success": False, "message": "Không thể cập nhật trạng thái", "status_code": 500}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi cập nhật trạng thái: {e}", "status_code": 500}

from db.nguoi_repository import NguoiRepository

nguoi_repo = NguoiRepository()


def change_shift_service(user_id: int, new_shift: str):
    if not new_shift:
        return {"success": False, "message": "shift mới không được để trống", "status_code": 400}
    try:
        existing = nguoi_repo.get_by_id(user_id)
        if not existing:
            return {"success": False, "message": "Không tìm thấy người", "status_code": 404}
        existing.shift = new_shift
        affected = nguoi_repo.update_by_id(user_id, existing)
        if affected > 0:
            return {"success": True, "message": f"Đã cập nhật ca làm cho user {user_id} -> {new_shift}"}
        else:
            return {"success": False, "message": "Không thể cập nhật ca làm", "status_code": 500}
    except Exception as e:
        return {"success": False, "message": f"Lỗi: {e}", "status_code": 500}

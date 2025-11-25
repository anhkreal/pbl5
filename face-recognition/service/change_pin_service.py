from db.nguoi_repository import NguoiRepository

nguoi_repo = NguoiRepository()


def change_pin_service(identifier, old_pin: str, new_pin: str):
    """Change the pin field for a given class_id (nguoi.id).

    Verifies the provided old_pin matches before updating to new_pin.

    Returns dict with success/message and status_code when appropriate.
    """
    if not new_pin:
        return {"success": False, "message": "Mã PIN mới không được để trống", "status_code": 400}
    if len(new_pin) < 4:
        return {"success": False, "message": "Mã PIN phải có ít nhất 4 ký tự", "status_code": 400}

    try:
        # identifier may be an integer id or a username string (current_user)
        existing = None
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            try:
                existing = nguoi_repo.get_by_id(int(identifier))
            except Exception:
                existing = None
        if existing is None:
            # try by username
            try:
                # add a small helper query in repository: get_by_username
                existing = nguoi_repo.get_by_username(identifier)
            except Exception:
                existing = None

        if not existing:
            return {"success": False, "message": f"Không tìm thấy người với identifier={identifier}", "status_code": 404}

        # Verify old PIN
        existing_pin = getattr(existing, 'pin', None)
        if existing_pin is None:
            # If there is currently no PIN set, we require old_pin to be empty string
            if old_pin not in (None, ''):
                return {"success": False, "message": "Mã PIN cũ không khớp", "status_code": 401}
        else:
            if str(existing_pin) != str(old_pin):
                return {"success": False, "message": "Mã PIN cũ không khớp", "status_code": 401}

        # Update the pin and persist
        existing.pin = new_pin
        affected = nguoi_repo.update_by_id(existing.id, existing)
        if affected > 0:
            return {"success": True, "message": f"Đã cập nhật PIN cho user id={existing.id}"}
        else:
            return {"success": False, "message": "Không thể cập nhật PIN", "status_code": 500}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi cập nhật PIN: {e}", "status_code": 500}

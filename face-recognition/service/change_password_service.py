from db.taikhoan_repository import TaiKhoanRepository


def change_password_service(username: str, current_password: str, new_password: str):
    """Verify current password and update to new_password for username.

    Returns dict with success flag and message.
    """
    repo = TaiKhoanRepository()

    # Basic password policy
    if not new_password or len(new_password) < 6:
        return {"success": False, "message": "Mật khẩu mới phải có ít nhất 6 ký tự", "status_code": 400}

    # Verify current password
    try:
        ok = repo.check_login(username, current_password)
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi kiểm tra mật khẩu hiện tại: {e}", "status_code": 500}

    if not ok:
        return {"success": False, "message": "Mật khẩu hiện tại không chính xác", "status_code": 401}

    # Update password
    try:
        rows = repo.update_password(username, new_password)
        if rows <= 0:
            return {"success": False, "message": "Không thể cập nhật mật khẩu (username không tồn tại)", "status_code": 404}
        return {"success": True, "message": "Đã cập nhật mật khẩu thành công"}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi cập nhật mật khẩu: {e}", "status_code": 500}

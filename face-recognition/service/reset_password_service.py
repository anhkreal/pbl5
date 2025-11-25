from db.nguoi_repository import NguoiRepository
import logging
import traceback

nguoi_repo = NguoiRepository()

# Configure a module-level logger for debugging purposes
logger = logging.getLogger('reset_password_service')
if not logger.handlers:
    # Ensure logs directory exists
    import os
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception:
        # best-effort: if we cannot create, fall back to current working directory
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
    handler = logging.FileHandler(os.path.join(log_dir, 'reset_password.log'))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def reset_password_service(user_id: int, default_pin: str = '123456'):
    try:
        existing = nguoi_repo.get_by_id(user_id)
        if not existing:
            return {"success": False, "message": "Không tìm thấy người", "status_code": 404}
        existing.pin = default_pin
        affected = nguoi_repo.update_by_id(user_id, existing)
        if affected > 0:
            return {"success": True, "message": f"Đã reset PIN cho user {user_id} về '{default_pin}'"}
        else:
            return {"success": False, "message": "Không thể reset PIN", "status_code": 500}
    except Exception as e:
        tb = traceback.format_exc()
        # Log the full traceback to a logfile for debugging
        try:
            logger.exception(f"Error resetting PIN for user_id={user_id}: {e}\n{tb}")
        except Exception:
            # If logging fails, still include traceback in console
            print(f"Logging failed: {e}")
            print(tb)
        # Return a sanitized error message to the client while preserving status 500
        return {"success": False, "message": "Lỗi khi reset PIN. Kiểm tra log server để biết chi tiết.", "detail": str(e), "status_code": 500}

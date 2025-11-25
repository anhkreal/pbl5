from db.nguoi_repository import NguoiRepository

nguoi_repo = NguoiRepository()


def verify_pin_service(user_id: int = None, username: str = None, pin: str = None):
    """Verify that the provided pin matches the stored pin for the given user id or username.

    Returns dict with success True/False and optional message.
    """
    try:
        if user_id is None and username is None:
            return {"success": False, "message": "user_id or username required", "status_code": 400}

        if user_id is not None:
            nguoi = nguoi_repo.get_by_id(int(user_id))
        else:
            nguoi = nguoi_repo.get_by_username(username)

        if not nguoi:
            return {"success": False, "message": "User not found", "status_code": 404}

        existing_pin = getattr(nguoi, 'pin', None)
        if existing_pin is None:
            # Treat None as no-pin configured
            return {"success": False, "message": "No PIN configured for user", "status_code": 404}

        if str(existing_pin) == str(pin):
            return {"success": True}
        else:
            return {"success": False, "message": "Invalid PIN", "status_code": 401}
    except Exception as e:
        return {"success": False, "message": f"Error verifying PIN: {e}", "status_code": 500}

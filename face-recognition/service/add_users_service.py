from db.models import Nguoi
from db.nguoi_repository import NguoiRepository
from datetime import datetime

nguoi_repo = NguoiRepository()


def add_users_service(full_name: str, age: int = None, phone: str = None, shift: str = 'day', address: str = None, gender: str = None, role: str = 'user', pin: str = None, avatar_bytes: bytes = None):
    # Basic validation
    if not full_name:
        return {"success": False, "message": "full_name là bắt buộc", "status_code": 400}

    new_nguoi = Nguoi(
        id=None,
        username=None,
        pin=pin,
        full_name=full_name,
        age=age,
        address=address,
        phone=phone,
        gender=gender,
        role=role,
        shift=shift,
        status='working',
        avatar_url=avatar_bytes,
        created_at=None,
        updated_at=None
    )
    try:
        new_id = nguoi_repo.add(new_nguoi)
        return {"success": True, "message": "Đã thêm nhân viên", "class_id": new_id}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi thêm nhân viên: {e}", "status_code": 500}

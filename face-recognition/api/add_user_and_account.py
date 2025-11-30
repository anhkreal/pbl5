from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from db.nguoi_repository import NguoiRepository
from db.taikhoan_repository import TaiKhoanRepository
from db.models import TaiKhoan, Nguoi

add_user_and_account_router = APIRouter()

@add_user_and_account_router.post("/add-user-account", summary="Thêm mới nhân viên và tài khoản (yêu cầu đăng nhập)")
def add_user_and_account(
    full_name: str = Form(None),
    username: str = Form(...),
    age: int = Form(None),
    address: str = Form(None),
    phone: str = Form(None),
    shift: str = Form('day'),
    current_user: str = Depends(get_current_user_mysql)
):
    nguoi_repo = NguoiRepository()
    taikhoan_repo = TaiKhoanRepository()

    # Kiểm tra username đã tồn tại chưa
    if taikhoan_repo.get_by_username(username):
        return JSONResponse(content={"success": False, "message": "Username đã tồn tại"}, status_code=400)

    # Thêm tài khoản với mật khẩu mặc định 123456 (không mã hóa)
    default_password = "123456"
    try:
        tk = TaiKhoan(username=username, passwrd=default_password)
        taikhoan_repo.add(tk)
    except Exception as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi khi thêm tài khoản: {e}"}, status_code=500)

    # Thêm nhân viên
    try:
        nguoi = Nguoi(
            id=None,
            username=username,
            pin=None,
            full_name=full_name,
            age=age,
            address=address,
            phone=phone,
            gender=None,
            role='user',
            shift=shift,
            status='working',
            avatar_url=None,
            created_at=None,
            updated_at=None
        )
        nguoi_id = nguoi_repo.add(nguoi)
    except Exception as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi khi thêm nhân viên: {e}"}, status_code=500)

    return JSONResponse(content={"success": True, "message": "Đã thêm mới nhân viên và tài khoản thành công", "user_id": nguoi_id, "username": username})

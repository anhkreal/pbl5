
from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.change_shift_service import change_shift_service
from db.nguoi_repository import NguoiRepository


change_shift_router = APIRouter()


@change_shift_router.put(
    "/edit-users/{user_id}/shift",
    summary="Thay đổi ca làm của nhân viên (yêu cầu đăng nhập)"
)
def change_shift(
    user_id: int,
    new_shift: str = Form(...),
    current_user: str = Depends(get_current_user_mysql)
):
    result = change_shift_service(user_id, new_shift)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)


# Đổi ca làm theo username
@change_shift_router.put(
    "/edit-users/by-username/{username}/shift",
    summary="Thay đổi ca làm của nhân viên theo username (yêu cầu đăng nhập)"
)
def change_shift_by_username(
    username: str,
    new_shift: str = Form(...),
    current_user: str = Depends(get_current_user_mysql)
):
    nguoi_repo = NguoiRepository()
    nguoi = nguoi_repo.get_by_username(username)
    if not nguoi:
        return JSONResponse(
            content={"success": False, "message": "Không tìm thấy user với username này"},
            status_code=404
        )
    result = change_shift_service(nguoi.id, new_shift)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

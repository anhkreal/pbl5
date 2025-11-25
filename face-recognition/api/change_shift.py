from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.change_shift_service import change_shift_service

change_shift_router = APIRouter()


@change_shift_router.put("/edit-users/{user_id}/shift", summary="Thay đổi ca làm của nhân viên (yêu cầu đăng nhập)")
def change_shift(user_id: int, new_shift: str = Form(...), current_user: str = Depends(get_current_user_mysql)):
    result = change_shift_service(user_id, new_shift)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

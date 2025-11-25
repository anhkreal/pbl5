from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.reset_password_service import reset_password_service

reset_password_router = APIRouter()


@reset_password_router.post('/edit-users/{user_id}/reset-password', summary="Reset mật khẩu nhân viên về mặc định (yêu cầu đăng nhập)")
def reset_password(user_id: int, current_user: str = Depends(get_current_user_mysql)):
    result = reset_password_service(user_id)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

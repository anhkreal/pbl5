from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.change_password_service import change_password_service

change_password_router = APIRouter()


@change_password_router.post(
    "/change-password",
    summary="Thay đổi mật khẩu (yêu cầu đăng nhập)",
)
def change_password(
    current_password: str = Form(...),
    new_password: str = Form(...),
    current_user: str = Depends(get_current_user_mysql)
):
    """Protected endpoint: change password for current logged-in user."""
    result = change_password_service(current_user, current_password, new_password)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        # remove status_code from body (returned via HTTP status)
        body = {k: v for k, v in result.items() if k != "status_code"}
    else:
        body = result
    return JSONResponse(content=body, status_code=status_code)

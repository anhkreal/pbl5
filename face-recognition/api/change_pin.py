from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.change_pin_service import change_pin_service

change_pin_router = APIRouter()


@change_pin_router.post(
    "/change-pin",
    summary="Thay đổi mã PIN cho người (yêu cầu đăng nhập)",
)
def change_pin(
    old_pin: str = Form(..., description="Mã PIN hiện tại"),
    new_pin: str = Form(..., description="Mã PIN mới"),
    current_user: str = Depends(get_current_user_mysql)
):
    # Change PIN for the currently authenticated user (current_user is username)
    result = change_pin_service(current_user, old_pin, new_pin)
    status_code = result.get("status_code", 200)
    body = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=body, status_code=status_code)

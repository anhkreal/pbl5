from fastapi import APIRouter, Form, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.add_users_service import add_users_service

add_users_router = APIRouter()


@add_users_router.post("/add-users", summary="Thêm mới nhân viên (yêu cầu đăng nhập)")
def add_users(
    full_name: str = Form(...),
    age: int = Form(None),
    phone: str = Form(None),
    shift: str = Form('day'),
    address: str = Form(None),
    gender: str = Form(None),
    role: str = Form('user'),
    pin: str = Form(None),
    avatar: UploadFile = File(None),
    current_user: str = Depends(get_current_user_mysql)
):
    avatar_bytes = None
    if avatar is not None:
        avatar_bytes = avatar.file.read()

    result = add_users_service(full_name, age, phone, shift, address, gender, role, pin, avatar_bytes)
    status_code = result.get('status_code', 200)
    if 'status_code' in result:
        body = {k: v for k, v in result.items() if k != 'status_code'}
    else:
        body = result
    return JSONResponse(content=body, status_code=status_code)

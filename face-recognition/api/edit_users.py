from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.edit_users_service import edit_users_service

edit_users_router = APIRouter()


@edit_users_router.put("/edit-users/{user_id}", summary="Cập nhật thông tin nhân viên (yêu cầu đăng nhập)")
def edit_users(
    user_id: int,
    full_name: str | None = Body(None),
    age: int | None = Body(None),
    address: str | None = Body(None),
    phone: str | None = Body(None),
    gender: str | None = Body(None),
    role: str | None = Body(None),
    shift: str | None = Body(None),
    status: str | None = Body(None),
    pin: str | None = Body(None),
    current_user: str = Depends(get_current_user_mysql),
):
    """Accepts individual JSON fields (not a single JSON `data` object).
    Example body: {"full_name":"Nguyen Van A","phone":"09123...","age":30}
    Avatar upload is handled by `/edit-users/{user_id}/avatar`.
    """
    data = {}
    if full_name is not None:
        data['full_name'] = full_name
    if age is not None:
        data['age'] = age
    if address is not None:
        data['address'] = address
    if phone is not None:
        data['phone'] = phone
    if gender is not None:
        data['gender'] = gender
    if role is not None:
        data['role'] = role
    if shift is not None:
        data['shift'] = shift
    if status is not None:
        data['status'] = status
    if pin is not None:
        data['pin'] = pin

    result = edit_users_service(user_id, data, None)
    status_code = result.get('status_code', 200)
    if 'status_code' in result:
        body = {k: v for k, v in result.items() if k != 'status_code'}
    else:
        body = result
    return JSONResponse(content=body, status_code=status_code)

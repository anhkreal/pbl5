from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.update_avatar_service import update_avatar_service

update_avatar_router = APIRouter()


@update_avatar_router.post('/edit-users/{user_id}/avatar', summary="Cập nhật ảnh đại diện (lưu dạng BLOB) (yêu cầu đăng nhập)")
def update_avatar(user_id: int, avatar: UploadFile = File(...), current_user: str = Depends(get_current_user_mysql)):
    # Defensive read: make sure the file pointer is at start
    try:
        avatar.file.seek(0)
    except Exception:
        pass
    avatar_bytes = avatar.file.read()
    result = update_avatar_service(user_id, avatar_bytes)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.delete_emotion_service import delete_emotion_service

delete_emotion_router = APIRouter()


@delete_emotion_router.delete('/delete-emotion/{emotion_id}', summary='Xóa một bản ghi emotion log (yêu cầu đăng nhập)')
def delete_emotion(emotion_id: int, current_user: str = Depends(get_current_user_mysql)):
    result = delete_emotion_service(emotion_id)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.query_emotion_service import query_emotion_service

emotion_router = APIRouter()


@emotion_router.get('/emotion', summary='Truy vấn emotion logs (lọc theo user, thời gian, cảm xúc)')
def query_emotion(
    user_id: int = Query(None),
    emotion_type: str = Query(None),
    start_ts: str = Query(None),
    end_ts: str = Query(None),
    limit: int = Query(100),
    offset: int = Query(0),
    include_image_base64: bool = Query(False),
    current_user: str = Depends(get_current_user_mysql)
):
    result = query_emotion_service(user_id=user_id, emotion_type=emotion_type, start_ts=start_ts, end_ts=end_ts, limit=limit, offset=offset, include_image_base64=include_image_base64)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

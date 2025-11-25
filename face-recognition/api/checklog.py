from fastapi import APIRouter, Depends, Query
from auth.mysql_auth import get_current_user_mysql
from service.checklog_service import query_checklogs_service

checklog_router = APIRouter()


@checklog_router.get('/checklog', summary='Xem danh sách chấm công (lọc theo ngày, tên, trạng thái)')
def get_checklogs(
    date: str = Query(None),
    date_from: str = Query(None),
    date_to: str = Query(None),
    user_id: int = Query(None),
    status: str = Query(None),
    limit: int = Query(100),
    offset: int = Query(0),
    current_user=Depends(get_current_user_mysql)
):
    result = query_checklogs_service(date=date, date_from=date_from, date_to=date_to, user_id=user_id, status=status, limit=limit, offset=offset)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return body

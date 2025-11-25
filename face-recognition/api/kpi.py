from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from service.kpi_service import query_kpis_service, query_kpis_for_user_service

kpi_router = APIRouter()


@kpi_router.get('/kpi', summary='Xem danh sách KPI (lọc theo ngày hoặc tháng, theo tên nhân viên)')
def get_kpis(
    date: str = Query(None, description='YYYY-MM-DD'),
    month: str = Query(None, description='YYYY-MM'),
    full_name: str = Query(None),
    limit: int = Query(100),
    offset: int = Query(0),
):
    result = query_kpis_service(date=date, month=month, full_name=full_name, limit=limit, offset=offset)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)




@kpi_router.get('/kpi/{user_id}', summary='Xem chi tiết KPI của nhân viên')
def get_kpis_for_user(
    user_id: int,
    date: str = Query(None, description='YYYY-MM-DD'),
    month: str = Query(None, description='YYYY-MM'),
    limit: int = Query(100),
    offset: int = Query(0),
):
    result = query_kpis_for_user_service(user_id=user_id, date=date, month=month, limit=limit, offset=offset)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from service.checkin_service import checkin_service

checkin_router = APIRouter()


@checkin_router.post('/checkin/{id}', summary='Tạo check-in cho user tại thời điểm hiện tại')
def checkin(id: int, note: str = Form(None)):
    # No authentication required for checkin endpoint per request
    result = checkin_service(user_id=id, edited_by=None, note=note)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

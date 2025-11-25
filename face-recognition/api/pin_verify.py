from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from service.pin_service import verify_pin_service

pin_router = APIRouter()


@pin_router.post('/system/pin-verify', summary='Kiểm tra mã PIN hợp lệ')
def pin_verify(user_id: int = Body(None), username: str = Body(None), pin: str = Body(...)):
    result = verify_pin_service(user_id=user_id, username=username, pin=pin)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from auth.mysql_auth import get_current_user_mysql
from service.resign_user_service import resign_user_service

resign_user_router = APIRouter()


@resign_user_router.put('/edit-users/{user_id}/resign', summary="Cho nhân viên thôi việc (yêu cầu đăng nhập)")
def resign_user(user_id: int, current_user: str = Depends(get_current_user_mysql)):
    result = resign_user_service(user_id)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)

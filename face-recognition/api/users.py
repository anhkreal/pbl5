from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from db.nguoi_repository import NguoiRepository

users_router = APIRouter()
nguoi_repo = NguoiRepository()


@users_router.get("/users", summary="Lấy danh sách nhân viên (lọc theo tên, trạng thái, ca)")
def get_users(
    query: str = Query(None, description="Tìm theo tên/địa chỉ/phone/..."),
    status: str = Query(None, description="Lọc theo trạng thái (ví dụ 'working')"),
    shift: str = Query(None, description="Lọc theo ca làm (ví dụ 'day')"),
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=200),
    sort_by: str = Query('full_name_asc')
):
    try:
        res = nguoi_repo.search_nguoi_paged(query=query or "", page=page, page_size=page_size, sort_by=sort_by, status=status, shift=shift)
        # Convert dataclass objects to dicts
        nguoi_list = [n.to_dict(include_avatar_base64=False) for n in res.get('nguoi_list', [])]
        return JSONResponse(content={"total": res.get('total', 0), "users": nguoi_list})
    except Exception as e:
        return JSONResponse(content={"message": f"Lỗi khi lấy danh sách nhân viên: {e}"}, status_code=500)


@users_router.get("/users/{user_id}", summary="Xem thông tin chi tiết nhân viên")
def get_user_detail(user_id: int, include_avatar_base64: bool = Query(False, description="Bao gồm ảnh avatar base64")):
    try:
        nguoi = nguoi_repo.get_by_id(user_id)
        if not nguoi:
            return JSONResponse(content={"message": "Không tìm thấy nhân viên"}, status_code=404)
        return JSONResponse(content={"user": nguoi.to_dict(include_avatar_base64=include_avatar_base64)})
    except Exception as e:
        return JSONResponse(content={"message": f"Lỗi khi lấy thông tin nhân viên: {e}"}, status_code=500)



from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from service.nguoi_info_service import get_nguoi_info_service

list_nguoi_router = APIRouter()

@list_nguoi_router.get(
    '/list_nguoi',
    summary="Danh sách thông tin người trong hệ thống",
    description="""
    **Lấy danh sách thông tin tất cả người đã được lưu trong hệ thống**
    
    API này cung cấp:
    - Danh sách tất cả người trong cơ sở dữ liệu
    - Thông tin chi tiết: tên, tuổi, giới tính, nơi ở, class_id
    - Tính năng tìm kiếm theo tên
    - Phân trang để hiển thị hiệu quả
    
    **Tham số tìm kiếm:**
    - query: Từ khóa tìm kiếm theo tên (để trống để hiển thị tất cả)
    - page: Số trang hiện tại (bắt đầu từ 1)
    - page_size: Số lượng kết quả mỗi trang (tối đa 100)
    
    **Kết quả trả về:**
    - Danh sách người phù hợp với điều kiện tìm kiếm
    - Tổng số kết quả tìm được
    - Thông tin phân trang
    """,
    response_description="Danh sách thông tin người với phân trang",
    tags=["📊 Tìm Kiếm & Thống Kê"]
)
def list_nguoi(
    query: str = Query("", description="Từ khóa tìm kiếm theo tên (để trống để hiển thị tất cả)"),
    page: int = Query(1, ge=1, description="Số trang hiện tại (bắt đầu từ 1)"),
    page_size: int = Query(15, ge=1, le=100, description="Số lượng kết quả mỗi trang (1-100)"),
    sort_by: str = Query('full_name_asc', description='Sắp xếp theo: full_name_asc, full_name_desc, age_asc, age_desc, id_asc, id_desc, created_asc, created_desc, updated_asc, updated_desc')
):
    try:
        nguoi_list = get_nguoi_info_service(query, page, page_size, sort_by)
        return JSONResponse(content={"results": nguoi_list}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

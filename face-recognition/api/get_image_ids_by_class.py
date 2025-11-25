from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from service.get_image_ids_by_class_service import get_image_ids_by_class_api_service

get_image_ids_by_class_router = APIRouter()



@get_image_ids_by_class_router.get(
    '/get_image_ids_by_class',
    summary="Lấy danh sách ảnh theo class_id",
    description="""
    **Lấy tất cả image_id thuộc một class_id cụ thể**
    
    API này cung cấp:
    - Danh sách tất cả ảnh thuộc về một người (class_id)
    - Thông tin chi tiết từng ảnh (image_id, image_path)
    - Kiểm tra số lượng ảnh của mỗi người
    - Hỗ trợ quản lý và kiểm tra dữ liệu
    
    **Tham số đầu vào:**
    - class_id: ID nhóm người cần truy vấn
    
    **Kết quả trả về:**
    - Danh sách image_id thuộc class_id
    - Đường dẫn ảnh tương ứng
    - Tổng số ảnh của người này
    - Metadata bổ sung (nếu có)
    
    **Ứng dụng:**
    - Kiểm tra số lượng ảnh của từng người
    - Quản lý dữ liệu training
    - Debug class mapping
    - Bulk operations trên ảnh của 1 người
    """,
    response_description="Danh sách ảnh thuộc class_id được chỉ định",
    tags=["📊 Tìm Kiếm & Thống Kê"]
)
def get_image_ids_by_class_api(
    class_id: str = Query(..., description="ID nhóm người cần truy vấn danh sách ảnh")
):
    result = get_image_ids_by_class_api_service(class_id)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

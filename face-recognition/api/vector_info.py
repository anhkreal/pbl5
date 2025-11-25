from fastapi import APIRouter
from fastapi.responses import JSONResponse
from service.vector_info_service import get_vector_info_service


vector_info_router = APIRouter()

@vector_info_router.get(
    '/vector_info',
    summary="Thông tin chi tiết về vectors",
    description="""
    **Xem thông tin chi tiết về tất cả vectors trong hệ thống**
    
    API này cung cấp:
    - Danh sách tất cả vectors đã được lưu trữ
    - Mapping giữa image_id và vector position trong FAISS
    - Thông tin metadata của từng vector
    - Statistics về phân bố vectors
    - Trạng thái đồng bộ giữa database và FAISS index
    
    **Thông tin chi tiết bao gồm:**
    - vector_count: Tổng số vectors
    - image_id_mapping: Map giữa image_id và index position
    - metadata_info: Thông tin class_id, image_path cho từng vector
    - consistency_check: Kiểm tra tính nhất quán dữ liệu
    - storage_info: Thông tin lưu trữ và bộ nhớ
    
    **Ứng dụng:**
    - Debug mapping issues
    - Kiểm tra data consistency
    - Database maintenance
    - Performance analysis
    - Troubleshooting search problems
    
    **Lưu ý:**
    - API này có thể trả về nhiều dữ liệu nếu hệ thống có nhiều vectors
    - Sử dụng cẩn thận với database lớn
    """,
    response_description="Thông tin chi tiết về tất cả vectors trong hệ thống",
    tags=["📊 Tìm Kiếm & Thống Kê"]
)
def get_vector_info():
    result = get_vector_info_service()
    status_code = result.get("status_code", 200)
    # Xóa status_code khỏi dict nếu có
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)
    

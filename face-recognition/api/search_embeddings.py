from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from service.embedding_query_service import search_embeddings_api

embedding_search_router = APIRouter()

@embedding_search_router.get(
    '/search_embeddings',
    summary="Tìm kiếm embedding khuôn mặt",
    description="""
    **Tìm kiếm thông tin embedding khuôn mặt trong cơ sở dữ liệu**
    
    API này cho phép:
    - Tìm kiếm embedding theo image_id, image_path, hoặc class_id
    - Xem chi tiết thông tin lưu trữ của từng ảnh
    - Kiểm tra trạng thái dữ liệu trong hệ thống
    - Hỗ trợ phân trang để dễ quản lý
    
    **Cách sử dụng:**
    - query: Từ khóa tìm kiếm (có thể là image_id, đường dẫn ảnh, hoặc class_id)
    - page: Số trang hiện tại
    - page_size: Số lượng kết quả mỗi trang
    
    **Kết quả trả về:**
    - Danh sách embedding phù hợp
    - Chi tiết image_id, image_path, class_id
    - Thông tin phân trang
    - Tổng số kết quả tìm được
    
    **Ứng dụng:**
    - Kiểm tra dữ liệu đã lưu
    - Debug hệ thống
    - Quản lý cơ sở dữ liệu
    """,
    response_description="Danh sách embedding khuôn mặt với phân trang",
    tags=["📊 Tìm Kiếm & Thống Kê"]
)
def search_embeddings_api_route(
    query: str = Query('', description='Từ khóa tìm kiếm (image_id, image_path, class_id) - để trống để hiển thị tất cả'),
    page: int = Query(1, ge=1, description='Số trang hiện tại (bắt đầu từ 1)'),
    page_size: int = Query(15, ge=1, le=15, description='Số lượng kết quả mỗi trang (tối đa 15)'),
    sort_by: str = Query('image_id_asc', description='Sắp xếp theo: image_id_asc, image_id_desc, class_id_asc, class_id_desc, image_path_asc, image_path_desc, created_asc, created_desc, updated_asc, updated_desc')
):
    result = search_embeddings_api(query, page, page_size, sort_by)
    # Convert numpy types to native Python types for JSON serialization
    import numpy as np
    def convert(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert(v) for v in obj]
        return obj
    result = convert(result)
    return JSONResponse(content=result)

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from service.index_status_service import index_status_service

status_router = APIRouter()



@status_router.get(
    '/index_status',
    summary="Trạng thái chỉ mục FAISS",
    description="""
    **Kiểm tra trạng thái chi tiết của chỉ mục tìm kiếm FAISS**
    
    API này cung cấp thông tin:
    - Trạng thái hoạt động của FAISS index
    - Tổng số vectors đã được lưu trữ
    - Loại index đang sử dụng (IndexFlatIP, IndexIVFFlat, v.v.)
    - Kích thước embedding (thường là 512 dimensions)
    - Thông tin bộ nhớ và hiệu suất index
    
    **Chi tiết trả về:**
    - index_ready: Index có sẵn sàng để sử dụng không
    - total_vectors: Tổng số embedding trong index
    - index_type: Loại FAISS index
    - embedding_dimension: Số chiều của vector embedding
    - memory_usage: Bộ nhớ index đang sử dụng
    - last_updated: Thời gian cập nhật gần nhất
    
    **Ứng dụng:**
    - Kiểm tra tình trạng index trước khi query
    - Monitoring dung lượng database
    - Debug các vấn đề tìm kiếm
    - Capacity planning cho FAISS
    """,
    response_description="Thông tin chi tiết về trạng thái FAISS index",
    tags=["📊 Tìm Kiếm & Thống Kê"]
)
def index_status():
    result = index_status_service()
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import time


from service.face_query_top5_service import query_face_top5_service as face_query_top5_service

face_query_top5_router = APIRouter()

@face_query_top5_router.post(
    '/query_top5',
    summary="Nhận diện khuôn mặt - Top 5 kết quả",
    description="""
    **Nhận diện khuôn mặt và trả về 5 kết quả giống nhất**
    
    API này tương tự `/query` nhưng trả về nhiều kết quả hơn:
    - Nhận ảnh chứa khuôn mặt từ người dùng
    - Trích xuất đặc trưng khuôn mặt
    - Tìm kiếm 5 khuôn mặt giống nhất trong database
    - Sắp xếp theo độ tương tự giảm dần
    - Trả về thông tin chi tiết của từng kết quả
    
    **Ưu điểm so với /query:**
    - Có nhiều lựa chọn kết quả
    - Cho phép so sánh độ tương tự
    - Phù hợp khi không chắc chắn về identity
    - Hỗ trợ manual verification
    
    **Kết quả trả về:**
    - Top 5 khuôn mặt tương tự nhất
    - Score độ tương tự cho từng kết quả
    - Thông tin người: tên, tuổi, giới tính, nơi ở
    - image_id và đường dẫn ảnh
    
    **Lưu ý:**
    - Ảnh phải chứa ít nhất 1 khuôn mặt rõ ràng
    - Hỗ trợ định dạng: JPG, PNG, WEBP
    - Kích thước file tối đa: 10MB
    """,
    response_description="Top 5 kết quả nhận diện khuôn mặt với độ tương tự cao nhất",
    tags=["👤 Nhận Diện Khuôn Mặt"]
)
async def query_face_top5(
    file: UploadFile = File(
        ..., 
        description="File ảnh chứa khuôn mặt cần nhận diện (JPG, PNG, WEBP)",
        media_type="image/*"
    )
):
    result = await face_query_top5_service(file)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from service.anti_spoofing_service import spoof_detection_service

# Response models để fix OpenAPI schema
class AntiSpoofingResponse(BaseModel):
    success: str
    is_spoof: bool
    confidence: float
    method: str = None
    error: str = None

anti_spoofing_router = APIRouter()

@anti_spoofing_router.post(
    "/check-spoof",
    operation_id="check_face_spoofing",  # Fix OpenAPI naming conflict
    response_model=AntiSpoofingResponse,  # Proper response model
    summary="Kiểm tra khuôn mặt giả mạo",
    description="""
    **Kiểm tra xem khuôn mặt trong ảnh có phải là giả mạo không**
    
    API này sẽ:
    - Nhận ảnh chứa khuôn mặt từ người dùng
    - Sử dụng DeepFace để kiểm tra tính thực của khuôn mặt
    - Trả về kết quả kiểm tra cùng với độ tin cậy
    
    **Trả về:**
    - success: REAL hoặc SPOOF
    - confidence: độ tin cậy của kết quả (0-1)
    
    **Lưu ý:**
    - Ảnh phải chứa ít nhất 1 khuôn mặt rõ ràng
    - Hỗ trợ các định dạng: JPG, PNG
    - Kích thước file tối đa: 10MB
    """,
    response_description="Kết quả kiểm tra khuôn mặt giả mạo",
    tags=["🛡️ Chống Giả Mạo"]
)
async def check_face_spoofing(
    image: UploadFile = File(
        ...,
        description="File ảnh chứa khuôn mặt cần kiểm tra (JPG, PNG)",
        media_type="image/*"
    )
):
    """
    Kiểm tra khuôn mặt giả mạo trong ảnh
    """
    try:
        # Gọi service kiểm tra
        spoof_check = await spoof_detection_service.check_spoof(image)
        
        # Tạo response
        response = {
            "success": spoof_check.get("message", "UNKNOWN"),
            "is_spoof": not spoof_check.get("is_real", False),
            "confidence": spoof_check.get("confidence", 0.5),
            "method": spoof_check.get("method", "Unknown")
        }
        
        if "error" in spoof_check:
            response["error"] = spoof_check["error"]
            
        return response  # Return dict instead of JSONResponse to match response_model
        
    except Exception as e:
        return AntiSpoofingResponse(
            success="ERROR",
            is_spoof=True,
            confidence=0.0,
            method="Error",
            error=f"Lỗi kiểm tra giả mạo: {str(e)}"
        )

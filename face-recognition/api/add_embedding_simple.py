from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from service.add_embedding_simple_service import simple_add_embedding_service

simple_add_router = APIRouter()

@simple_add_router.post(
    '/add_embedding_simple',
    summary="Thêm khuôn mặt mới - Chỉ cần ảnh (Auto Generate All - Public API)",
    description="""
    **🚀 API ĐƠN GIẢN CÔNG KHAI - Chỉ cần upload ảnh, tất cả thông tin khác tự động tạo**
    
    ⚡ **KHÔNG CẦN AUTHENTICATION** - API công khai cho demo và test
    
    **🤖 Tự động xử lý:**
    - 📷 **image_id**: Tự động tạo ID unique
    - 🗂️ **image_path**: Tự động tạo "image_{id}.jpg"
    - 🆔 **class_id**: Tự động tạo ID người mới
    - 👤 **ten**: Tự động tạo "Người lạ {class_id}"
    - 🎂 **tuoi**: Predict từ ảnh bằng AI
    - ⚧️ **gioitinh**: Predict từ ảnh bằng AI  
    - 🏠 **noio**: Mặc định "default"
    
    **Chỉ cần:**
    - 📁 Upload file ảnh (JPG, PNG, WEBP)
    
    **Lưu ý:**
    - 🚫 Ảnh phải chứa đúng 1 khuôn mặt rõ ràng
    - 📏 Kích thước file tối đa: 10MB
    - 🤖 AI sẽ tự động nhận diện tuổi và giới tính
    - 🌐 API công khai - có thể sử dụng mà không cần đăng nhập
    """,
    response_description="Kết quả thêm khuôn mặt với tất cả thông tin được tự động tạo",
    tags=["🚀 Thêm Đơn Giản (Public)"]
)
async def add_embedding_simple(
    file: UploadFile = File(
        ..., 
        description="File ảnh khuôn mặt (JPG, PNG, WEBP) - Tất cả thông tin khác tự động tạo",
        media_type="image/*"
    )
):
    """
    🌐 Public API - Thêm khuôn mặt đơn giản chỉ cần ảnh (không cần auth)
    
    Tất cả thông tin khác sẽ được tự động tạo bằng AI và logic tự động.
    """
    print("Public API: Adding embedding simple without auth")
    
    result = await simple_add_embedding_service(file)
    
    # Thêm thông tin audit log (không có user info vì public API)
    result["audit_info"] = {
        "performed_by": "anonymous",
        "user_role": "public",
        "action": "add_embedding_simple",
        "auto_generated": True,
        "auth_required": False
    }
    
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

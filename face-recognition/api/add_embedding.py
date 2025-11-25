from fastapi import APIRouter, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from service.add_embedding_service import add_embedding_service
from Depend.depend import AddEmbeddingInput
# 🔐 Import MySQL Authentication with Dynamic Auth
from auth.mysql_auth import get_current_user_mysql

add_router = APIRouter()

@add_router.post(
    '/add_embedding',
    summary="Thêm khuôn mặt mới vào hệ thống (Cần MySQL Login)",
    description="""
    **🔒 API BẢO MẬT - Thêm khuôn mặt và thông tin cá nhân vào cơ sở dữ liệu**
    
    ⚠️ **YÊU CẦU AUTHENTICATION:**
    - **MySQL Login**: Bắt buộc đăng nhập bằng `/auth/login`
    - **Session Cookie**: Tự động gửi kèm sau khi đăng nhập
    - **Permission**: Cần đăng nhập MySQL để thực hiện
    
    API này cho phép:
    - 📷 Thêm ảnh khuôn mặt mới vào hệ thống
    - 👤 Lưu thông tin cá nhân chi tiết (tên, tuổi, giới tính, nơi ở)
    - 🤖 Tự động trích xuất đặc trưng khuôn mặt
    - 🔄 Cập nhật chỉ mục tìm kiếm FAISS
    
    **Quy tắc nhập liệu:**
    - ✅ Tất cả các trường thông tin đều bắt buộc
    - 🔄 Nếu chỉ thêm ảnh cho class_id đã tồn tại, vẫn phải điền đầy đủ thông tin
    - 🆔 image_id phải là duy nhất trong hệ thống
    - 👥 class_id dùng để nhóm các ảnh của cùng 1 người
    
    **Lưu ý bảo mật:**
    - 🔐 API này được bảo vệ bởi JWT authentication
    - 📝 Mọi thao tác được log lại với user ID
    - ⏱️ Rate limiting áp dụng để chống spam
    - 🚫 Ảnh phải chứa đúng 1 khuôn mặt rõ ràng
    - 📁 Hỗ trợ định dạng: JPG, PNG, WEBP
    - 📏 Kích thước file tối đa: 10MB
    """,
    response_description="Kết quả thêm khuôn mặt mới vào hệ thống với thông tin authentication",
    tags=["➕ Thêm Dữ Liệu (Protected)"]
)
async def add_embedding(
    input: AddEmbeddingInput = Depends(AddEmbeddingInput.as_form),
    file: UploadFile = File(
        ..., 
        description="File ảnh khuôn mặt cần thêm vào hệ thống (JPG, PNG, WEBP)",
        media_type="image/*"
    ),
    current_user: str = Depends(get_current_user_mysql)
):
    """
    🔒 Protected API - Thêm khuôn mặt mới vào hệ thống
    
    Chỉ user đã đăng nhập MySQL mới có thể sử dụng.
    Yêu cầu tất cả thông tin đầy đủ.
    """
    print(f"User {current_user} dang them embedding with full info")
    
    result = await add_embedding_service(input, file)
    
    # Thêm thông tin audit log
    if result.get("success"):
        result["audit_info"] = {
            "performed_by": current_user,
            "user_role": "user",  # MySQL auth doesn't have role info
            "action": "add_embedding"
        }
    
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

# fe cần phải truyền về api toàn bộ trường, không được bỏ trống thông tin
# nếu như chỉ thêm ảnh (class_id đã tồn tại) --> điền dữ liệu rác
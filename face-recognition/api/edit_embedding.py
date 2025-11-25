from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from Depend.depend import EditEmbeddingInput
from service.edit_embedding_service import edit_embedding_service
# 🔐 Import MySQL Authentication
from auth.mysql_auth import get_current_user_mysql

edit_embedding_router = APIRouter()

@edit_embedding_router.post(
    '/edit_embedding',
    summary="Chỉnh sửa thông tin khuôn mặt (Cần MySQL Login)",
    description="""
    **🔒 API BẢO MẬT - Cập nhật thông tin khuôn mặt và ảnh trong hệ thống**
    
    ⚠️ **YÊU CẦU AUTHENTICATION:**
    - **MySQL Login**: Bắt buộc đăng nhập bằng `/auth/login`
    - **Session Cookie**: Tự động gửi kèm sau khi đăng nhập
    - **Permission**: Cần đăng nhập MySQL để thực hiện
    
    API này cho phép:
    - 🔄 Cập nhật ảnh khuôn mặt cho image_id đã tồn tại
    - 📂 Thay đổi đường dẫn ảnh (image_path)
    - 🤖 Tự động cập nhật đặc trưng khuôn mặt nếu có ảnh mới
    - 🔄 Đồng bộ thông tin trong chỉ mục tìm kiếm FAISS
    
    **Cách sử dụng:**
    - 🆔 **image_id**: Bắt buộc, phải tồn tại trong hệ thống
    - 📂 **image_path**: Tùy chọn, đường dẫn mới cho ảnh
    - 📷 **file**: Tùy chọn, ảnh mới để thay thế
    
    **Lưu ý bảo mật:**
    - 🔐 API này được bảo vệ bởi JWT authentication
    - 📝 Mọi thao tác được log lại với user ID
    - ⏱️ Rate limiting áp dụng để chống spam
    - 🔍 Phải cung cấp ít nhất image_id để xác định record
    - 🚫 Nếu có ảnh mới, phải chứa đúng 1 khuôn mặt rõ ràng
    - 📁 Hỗ trợ định dạng: JPG, PNG, WEBP
    - 📏 Kích thước file tối đa: 10MB
    """,
    response_description="Kết quả cập nhật thông tin khuôn mặt với thông tin authentication",
    tags=["✏️ Chỉnh Sửa Dữ Liệu (Protected)"]
)
def edit_embedding(
    input: EditEmbeddingInput = Depends(EditEmbeddingInput.as_form),
    file: UploadFile = File(
        None, 
        description="File ảnh mới để thay thế (tùy chọn - JPG, PNG, WEBP)",
        media_type="image/*"
    ),
    current_user: str = Depends(get_current_user_mysql)
):
    """
    🔒 Protected API - Chỉnh sửa thông tin khuôn mặt
    
    Chỉ user đã đăng nhập MySQL mới có thể sử dụng.
    """
    print(f"User {current_user} dang chinh sua embedding")
    
    result = edit_embedding_service(input, file)
    
    # Thêm thông tin audit log
    if result.get("success"):
        result["audit_info"] = {
            "performed_by": current_user,
            "user_role": "user",  # MySQL auth doesn't have role info
            "action": "edit_embedding",
            "target_image_id": input.image_id if hasattr(input, 'image_id') else None
        }
    
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

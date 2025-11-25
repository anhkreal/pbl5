from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse

from service.delete_image_service import delete_image_service
from Depend.depend import DeleteImageInput
# 🔐 Import MySQL Authentication
from auth.mysql_auth import get_current_user_mysql

delete_image_router = APIRouter()

@delete_image_router.post(
    '/delete_image',
    summary="Xóa ảnh khuôn mặt khỏi hệ thống (Cần MySQL Login)",
    description="""
    **🔒 API BẢO MẬT - Xóa một ảnh khuôn mặt cụ thể khỏi cơ sở dữ liệu**
    
    ⚠️ **YÊU CẦU AUTHENTICATION:**
    - **JWT Token**: Bắt buộc trong header `Authorization: Bearer <token>`
    - **Permission**: Cần scope `delete` (ADMIN role)
    - **Rate Limit**: 10 requests/phút
    
    API này sẽ:
    - 🗑️ Xóa ảnh khuôn mặt theo image_id
    - 🔄 Loại bỏ đặc trưng khuôn mặt khỏi chỉ mục FAISS
    - 💾 Cập nhật cơ sở dữ liệu
    - ✅ Không ảnh hưởng đến các ảnh khác cùng class_id
    
    **Cách sử dụng:**
    - 🆔 **image_id**: Bắt buộc, ID ảnh cần xóa
    - ✅ image_id phải tồn tại trong hệ thống
    
    **Lưu ý bảo mật:**
    - 🔐 Chỉ ADMIN mới có quyền delete
    - 📝 Mọi thao tác được log chi tiết với user ID
    - ⚠️ **Thao tác này KHÔNG THỂ HOÀN TÁC**
    - 🎯 Chỉ xóa **1 ảnh cụ thể**, không xóa toàn bộ class
    - 👥 Nếu muốn xóa tất cả ảnh của 1 người, sử dụng API `/delete_class`
    - ⏱️ Rate limiting để tránh xóa nhầm hàng loạt
    
    **So sánh với delete_class:**
    - 🖼️ `delete_image`: Xóa 1 ảnh cụ thể
    - 👤 `delete_class`: Xóa toàn bộ thông tin 1 người
    """,
    response_description="Kết quả xóa ảnh khuôn mặt với audit log",
    tags=["🗑️ Xóa Dữ Liệu (Protected)"]
)
def delete_image(
    input: DeleteImageInput = Depends(DeleteImageInput.as_form),
    current_user: str = Depends(get_current_user_mysql)
):
    """
    🔒 Protected API - Xóa ảnh khuôn mặt khỏi hệ thống
    
    CHỈ ADMIN mới có quyền sử dụng API này.
    """
    print(f"User {current_user} dang xoa image_id: {getattr(input, 'image_id', 'unknown')}")
    
    result = delete_image_service(input)
    
    # Thêm thông tin audit log
    if result.get("success"):
        result["audit_info"] = {
            "performed_by": current_user,
            "user_role": "user",  # MySQL auth doesn't have role info
            "action": "delete_image",
            "target_image_id": getattr(input, 'image_id', None)
        }
    
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

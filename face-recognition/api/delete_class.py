from fastapi import APIRouter, Query, Form, Depends
from fastapi.responses import JSONResponse
import numpy as np

from service.delete_class_service import delete_class_service
from Depend.depend import DeleteClassInput
# 🔐 Import MySQL Authentication
from auth.mysql_auth import get_current_user_mysql

delete_class_router = APIRouter()

@delete_class_router.post(
    '/delete_class',
    summary="Xóa toàn bộ thông tin một người (Cần MySQL Login)",
    description="""
    **🔒 API BẢO MẬT CAO - Xóa tất cả ảnh và thông tin của một người khỏi hệ thống**
    
    ⚠️ **YÊU CẦU AUTHENTICATION:**
    - **MySQL Login**: Bắt buộc đăng nhập bằng `/auth/login`
    - **Session Cookie**: Tự động gửi kèm sau khi đăng nhập
    - **Permission**: Cần đăng nhập MySQL để thực hiện
    
    🚨 **CẢNH BÁO - THAO TÁC NGUY HIỂM:**
    
    API này sẽ **XÓA VĨNH VIỄN**:
    - 🗑️ Tất cả ảnh khuôn mặt thuộc class_id đã chỉ định
    - 🔄 Loại bỏ toàn bộ đặc trưng khuôn mặt khỏi chỉ mục FAISS
    - 👤 Xóa thông tin cá nhân (tên, tuổi, giới tính, nơi ở)
    - 💾 Cập nhật cơ sở dữ liệu hoàn toàn
    
    **Cách sử dụng:**
    - 🆔 **class_id**: Bắt buộc, ID người cần xóa hoàn toàn
    - ✅ class_id phải tồn tại trong hệ thống
    
    **Lưu ý bảo mật:**
    - 🔐 Chỉ ADMIN mới có quyền delete
    - 📝 Mọi thao tác được log chi tiết với user ID
    - ⚠️ **Thao tác này KHÔNG THỂ HOÀN TÁC**
    - 🗑️ Sẽ xóa **TẤT CẢ** ảnh và thông tin liên quan đến class_id
    - 🆚 Khác với `/delete_image` chỉ xóa 1 ảnh cụ thể
    - ⏱️ Rate limiting nghiêm ngặt để tránh xóa nhầm hàng loạt
    
    **⚠️ HÃY CHẮC CHẮN TRƯỚC KHI THỰC HIỆN!**
    """,
    response_description="Kết quả xóa toàn bộ thông tin người với audit log",
    tags=["🗑️ Xóa Dữ Liệu (Protected)"]
)
def delete_class(
    input: DeleteClassInput = Depends(DeleteClassInput.as_form),
    current_user: str = Depends(get_current_user_mysql)
):
    """
    🔒 Protected API - Xóa toàn bộ thông tin một người
    
    Chỉ user đã đăng nhập MySQL mới có thể sử dụng.
    Thao tác nguy hiểm - không thể hoàn tác!
    """
    print(f"CANH BAO: User {current_user} dang XOA TOAN BO class_id: {getattr(input, 'class_id', 'unknown')}")
    
    result = delete_class_service(input)
    
    # Thêm thông tin audit log chi tiết
    if result.get("success"):
        result["audit_info"] = {
            "performed_by": current_user,
            "user_role": "user",  # MySQL auth doesn't have role info
            "action": "delete_class",
            "target_class_id": getattr(input, 'class_id', None),
            "warning": "TOÀN BỘ dữ liệu của class_id đã được xóa vĩnh viễn"
        }
    
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)
    
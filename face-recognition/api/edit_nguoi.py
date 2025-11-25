from fastapi import APIRouter, Form, HTTPException, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from service.edit_nguoi_service import edit_nguoi_service
from Depend.depend import EditNguoiInput
# 🔐 Import MySQL Authentication
from auth.mysql_auth import get_current_user_mysql

edit_nguoi_router = APIRouter()

@edit_nguoi_router.post(
    "/edit_nguoi",
    summary="Chỉnh sửa thông tin người (Cần MySQL Login)",
    description="""
    **🔒 API BẢO MẬT - Cập nhật thông tin cá nhân trong hệ thống**
    
    ⚠️ **YÊU CẦU AUTHENTICATION:**
    - **MySQL Login**: Bắt buộc đăng nhập bằng `/auth/login`
    - **JWT Token**: Gửi trong header Authorization
    - **Permission**: Cần đăng nhập MySQL để thực hiện
    
    API này cho phép:
    - 📝 Cập nhật thông tin cá nhân (tên, tuổi, giới tính, nơi ở)
    - 📷 Upload ảnh mới cho người đó
    - 🔄 Tự động cập nhật thông tin trong cơ sở dữ liệu
    
    **Lưu ý bảo mật:**
    - 🔐 API này được bảo vệ bởi MySQL authentication
    - 📝 Mọi thao tác được log lại với user ID
    """,
    response_description="Kết quả cập nhật thông tin người với audit log",
    tags=["✏️ Chỉnh Sửa Thông Tin Người (Protected)"]
)
async def edit_nguoi_api(
    input: EditNguoiInput = Depends(EditNguoiInput.as_form),
    file: UploadFile = File(
        None, 
        description="File ảnh mới (tùy chọn - JPG, PNG, WEBP)",
        media_type="image/*"
    ),
    current_user: str = Depends(get_current_user_mysql)
):
    """
    🔒 Protected API - Chỉnh sửa thông tin người
    
    Chỉ user đã đăng nhập MySQL mới có thể sử dụng.
    """
    print(f"User {current_user} đang chỉnh sửa thông tin người")
    
    try:
        result = edit_nguoi_service(input, file)
        
        # Thêm thông tin audit log
        if result.get("success"):
            result["audit_info"] = {
                "performed_by": current_user,
                "user_role": "user",
                "action": "edit_nguoi",
                "target_class_id": input.class_id if hasattr(input, 'class_id') else None
            }
        
        if result.get("status_code") and result["status_code"] != 200:
            raise HTTPException(status_code=result["status_code"], detail=result["message"])
        
        return JSONResponse(content=result, status_code=200)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in edit_nguoi_api: {str(e)}")
        import traceback
        traceback.print_exc()  # In chi tiết lỗi để debug
        raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi cập nhật")

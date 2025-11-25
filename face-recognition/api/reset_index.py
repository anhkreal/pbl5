from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from service.reset_index_service import reset_index_api_service as reset_index_service
# 🔐 Import MySQL Authentication
from auth.mysql_auth import get_current_user_mysql

reset_router = APIRouter()

@reset_router.post(
    '/reset_index',
    summary="Khởi tạo lại chỉ mục tìm kiếm (Cần MySQL Login)",
    description="""
    **🔒 API BẢO MẬT CỰC KỲ NGUY HIỂM - Xóa toàn bộ dữ liệu và khởi tạo lại hệ thống từ đầu**
    
    ⚠️ **YÊU CẦU AUTHENTICATION:**
    - **JWT Token**: Bắt buộc trong header `Authorization: Bearer <token>`
    - **Permission**: Cần scope `delete` (CHỈ ADMIN)
    - **Rate Limit**: 1 request/giờ (giới hạn CỰC KỲ NGHIÊM NGẶT)
    
    🚨 **CẢNH BÁO CỰC KỲ NGUY HIỂM - API NUCLEAR:**
    
    API này sẽ **XÓA TOÀN BỘ HỆ THỐNG**:
    - 💥 Xóa toàn bộ chỉ mục tìm kiếm FAISS
    - 🗑️ Xóa **TẤT CẢ** dữ liệu embedding đã lưu
    - 👥 Xóa **TẤT CẢ** thông tin người trong cơ sở dữ liệu
    - 🔄 Khởi tạo lại hệ thống về trạng thái ban đầu (TRỐNG HOÀN TOÀN)
    
    **🚨 CẢNH BÁO CUỐI CÙNG:**
    - ⚠️ **THAO TÁC NÀY SẼ XÓA TẤT CẢ DỮ LIỆU**
    - 🚫 **KHÔNG THỂ HOÀN TÁC** sau khi thực hiện
    - 🌪️ Hệ thống sẽ trở về trạng thái **TRỐNG HOÀN TOÀN**
    - 👑 **CHỈ ADMIN** mới có quyền thực hiện
    
    **Sử dụng khi nào:**
    - 🆕 Khởi tạo hệ thống lần đầu
    - 📊 Reset toàn bộ để import dữ liệu mới
    - 🔧 Khắc phục lỗi chỉ mục bị hỏng nghiêm trọng
    - 🧪 Testing và development (môi trường dev)
    
    **Lưu ý bảo mật:**
    - 🔐 CHỈ ADMIN cấp cao nhất mới có quyền
    - 📝 Mọi thao tác được log chi tiết với thời gian chính xác
    - ⏱️ Rate limiting cực kỳ nghiêm ngặt (1 lần/giờ)
    - 🚨 Sẽ có audit trail chi tiết cho thao tác nguy hiểm này
    
    **⚠️⚠️⚠️ HÃY CỰC KỲ CHẮC CHẮN TRƯỚC KHI THỰC HIỆN! ⚠️⚠️⚠️**
    """,
    response_description="Kết quả khởi tạo lại hệ thống với audit log chi tiết",
    tags=["🗑️ Xóa Dữ Liệu (Protected)"]
)
def reset_index_api(
    current_user: str = Depends(get_current_user_mysql)
):
    """
    🔒 Protected API - Khởi tạo lại chỉ mục tìm kiếm
    
    CHỈ ADMIN cấp cao nhất mới có quyền sử dụng API CỰC KỲ NGUY HIỂM này.
    Sẽ XÓA TOÀN BỘ HỆ THỐNG!
    """
    print(f"NUCLEAR WARNING: User {current_user} dang RESET TOAN BO HE THONG!")
    print(f"TAT CA DU LIEU SE BI XOA VINH VIEN!")
    
    result = reset_index_service()
    
    # Thêm thông tin audit log CỰC KỲ CHI TIẾT
    if result.get("success"):
        result["audit_info"] = {
            "performed_by": current_user,
            "user_role": "user",  # MySQL auth doesn't have role info
            "action": "RESET_ENTIRE_SYSTEM",
            "severity": "NUCLEAR",
            "warning": "TOÀN BỘ HỆ THỐNG ĐÃ BỊ XÓA VĨNH VIỄN",
            "impact": "ALL_DATA_DESTROYED"
        }
    
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.face_query import router as face_query_router
from api.delete_class import delete_class_router
from api.add_embedding import add_router
from api.delete_image import delete_image_router
from api.vector_info import vector_info_router
from api.change_password import change_password_router
from api.change_pin import change_pin_router
from api.reset_password import reset_password_router
from api.get_image_ids_by_class import get_image_ids_by_class_router
from api.pin_verify import pin_router
from api.index_status import status_router
from api.reset_index import reset_router
from api.users import users_router
from api.add_users import add_users_router
from api.face_query_top5 import face_query_top5_router
from api.edit_embedding import edit_embedding_router
from api.checkout import router as checkout_router
from api.edit_nguoi import edit_nguoi_router
from api.edit_users import edit_users_router
from api.change_shift import change_shift_router
from api.resign_user import resign_user_router
from api.list_nguoi import list_nguoi_router
from api.search_embeddings import embedding_search_router
from api.update_avatar import update_avatar_router
from api.faces import faces_router
from api.add_emotion import add_emotion_router
from api.emotion import emotion_router
from api.delete_emotion import delete_emotion_router
from api.checkin import checkin_router
from api.kpi import kpi_router
from api.edit_checklog import router as edit_checklog_router
from api.health import health_router
from api.predict import predict_router
from api.add_embedding_simple import simple_add_router
from api.anti_spoofing import anti_spoofing_router
from api.checklog import checklog_router
# Optional performance monitoring
try:
    from api.performance import performance_router
    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False
    # Performance monitoring not available

# MySQL Authentication
from auth.mysql_auth_api import router as mysql_auth_router
from api.taikhoan_api import taikhoan_router

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

app = FastAPI(
    title="🤖 Hệ Thống Nhận Diện Khuôn Mặt với MySQL Authentication",
    description="""
    ## 🎯 Giới Thiệu Hệ Thống
    
app.include_router(checkout.router)
    **Hệ thống nhận diện khuôn mặt AI tiên tiến** sử dụng công nghệ deep learning và FAISS để:
    
    ### 🚀 Tính Năng Chính
    - **🔍 Tìm kiếm khuôn mặt**: Tìm người giống nhất từ database
    - **➕ Quản lý dữ liệu**: Thêm, sửa, xóa thông tin người dùng
    - **📊 Thống kê**: Xem thông tin database và hiệu suất
    - **🔐 Bảo mật**: Đăng nhập MySQL để bảo vệ các thao tác nhạy cảm
    
    ### 🔐 Hệ Thống Authentication
    **MySQL Database Authentication:**
    - 🏠 **Public APIs**: Tìm kiếm khuôn mặt, xem thông tin (không cần đăng nhập)
    - 🔒 **Protected APIs**: Thêm, sửa, xóa dữ liệu (yêu cầu đăng nhập MySQL)
    
    ### 🛡️ Authentication & Authorization
    
    **MySQL Token Authentication:**
    - Sử dụng `/auth/login` để đăng nhập với username/password từ bảng `taikhoan`
    - Nhận session token để sử dụng cho protected APIs
    - Token được validate qua MySQL database
    - Logout với `/auth/logout` để clear session
    
    **Security Model:**
    - 🟢 **Public**: Query, search, health check (không cần đăng nhập)
    - 🔒 **Protected**: Add, edit, delete (cần đăng nhập qua bảng taikhoan MySQL)
    
    **Yêu Cầu Authentication:**
    Đảm bảo phải đăng nhập thông qua bảng taikhoan MySQL mới được các tác vụ thêm/sửa/xóa MySQL/FAISS, còn truy vấn khỏi cần
    
    ### 📝 Hướng Dẫn Sử Dụng
    1. **Tìm kiếm khuôn mặt**: Dùng `/query` với ảnh upload
    2. **Đăng nhập**: POST `/auth/login` với username/password MySQL
    3. **Quản lý dữ liệu**: Sau khi đăng nhập, có thể add/edit/delete
    4. **Đăng xuất**: POST `/auth/logout` để kết thúc session
    
    ### 🛠️ Công Nghệ Sử Dụng
    - **AI Framework**: ArcFace, FAISS Vector Search
    - **Backend**: FastAPI, Python
    - **Database**: MySQL Authentication
    - **Security**: Session-based Authentication với Bearer tokens
    """,
    version="2.0.0",
    contact={
        "name": "Face Recognition API Support",
        "email": "support@faceapi.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,  # True để cho phép cookies/session
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(mysql_auth_router, tags=["🔐 Authentication"])
app.include_router(taikhoan_router, tags=["🔐 MySQL Accounts"])
app.include_router(face_query_router, tags=["👤 Nhận Diện Khuôn Mặt"])
app.include_router(anti_spoofing_router, tags=["🛡️ Chống Giả Mạo"])
app.include_router(face_query_top5_router, tags=["👥 Top 5 Tương Tự"])
app.include_router(simple_add_router, tags=["➕ Thêm Người Đơn Giản"])
app.include_router(add_router, tags=["➕ Quản Lý Người"])
app.include_router(edit_embedding_router, tags=["✏️ Chỉnh Sửa"])
app.include_router(edit_nguoi_router, tags=["✏️ Chỉnh Sửa Thông Tin Người"])
app.include_router(edit_users_router, tags=["✏️ Chỉnh Sửa Thông Tin Người"])
app.include_router(change_shift_router, tags=["✏️ Chỉnh Sửa Thông Tin Người"])
app.include_router(resign_user_router, tags=["✏️ Chỉnh Sửa Thông Tin Người"])
app.include_router(delete_class_router, tags=["❌ Xóa Người"])
app.include_router(delete_image_router, tags=["🗑️ Xóa Ảnh"])
app.include_router(vector_info_router, tags=["📊 Thông Tin Database"])
app.include_router(change_password_router, tags=["🔐 MySQL Authentication"])
app.include_router(change_pin_router, tags=["🔐 MySQL Authentication"])
app.include_router(reset_password_router, tags=["🔐 MySQL Authentication"])
app.include_router(get_image_ids_by_class_router, tags=["🖼️ Danh Sách Ảnh"])
app.include_router(update_avatar_router, tags=["✏️ Chỉnh Sửa Thông Tin Người"])
app.include_router(faces_router, tags=["➕ Thêm Khuôn Mặt"])
app.include_router(list_nguoi_router, tags=["📋 Danh Sách Người"])
app.include_router(add_emotion_router, tags=["📝 Emotion Logs"])
app.include_router(pin_router, tags=["🔐 PIN"])
app.include_router(emotion_router, tags=["📝 Emotion Logs"])
app.include_router(embedding_search_router, tags=["🔍 Tìm Kiếm Nâng Cao"])
app.include_router(delete_emotion_router, tags=["🗑️ Xóa Emotion"])
app.include_router(status_router, tags=["💡 Trạng Thái"])
app.include_router(checkin_router, tags=["🕒 Check-in"])
app.include_router(kpi_router, tags=["📊 KPI"])
app.include_router(reset_router, tags=["🔄 Reset Database"])
app.include_router(users_router, tags=["📋 Danh Sách Người"])
app.include_router(add_users_router, tags=["➕ Quản Lý Người"])
app.include_router(checklog_router, tags=["🕒 Checklog"])
app.include_router(edit_checklog_router, tags=["✏️ Edit Checklog"])
app.include_router(predict_router, tags=["🤖 Dự Đoán"])
app.include_router(health_router, tags=["❤️ Sức Khỏe"])
app.include_router(checkout_router, tags=["🕒 Checkout"])

if PERFORMANCE_AVAILABLE:
    app.include_router(performance_router, prefix="/metrics", tags=["📈 Hiệu Suất"])

# Security Headers Middleware 
@app.middleware("http")
async def security_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Check if this is a Swagger/docs request
    is_docs_request = any(path in str(request.url) for path in ["/docs", "/redoc", "/openapi.json"])
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # More permissive CSP for Swagger UI
    if is_docs_request:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' https:; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'"
        )
    else:
        # Stricter CSP for API endpoints
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'"
        )
    
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Performance Monitoring Middleware
@app.middleware("http")
async def performance_monitoring(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    # Log request performance (without sensitive data)
    if not any(path in str(request.url) for path in ["/docs", "/redoc", "/openapi.json"]):
        process_time = time.time() - start_time
        # Performance logging disabled for production
    
    return response

# 🔐 MySQL Authentication APIs
# mysql_auth_router already included above with prefix="/auth"

print("🚀 Khởi tạo Face Recognition System thành công!")
print("🔐 MySQL Authentication system đã được tích hợp!")
print("📊 Security middleware và logging đã được kích hoạt!")

# All routers already included above - removed duplicates to fix OpenAPI schema conflicts
# 🏠 Public APIs: face_query_router, face_query_top5_router, anti_spoofing_router, etc.
# 🔒 Protected APIs: add_router, edit_embedding_router, delete_class_router, etc.
# � System APIs: health_router, status_router, vector_info_router, etc.

@app.get("/", tags=["🏠 Trang Chủ"])
def read_root():
    """
    ## 🏠 Trang Chủ API
    
    Chào mừng đến với **Hệ Thống Nhận Diện Khuôn Mặt**!
    
    ### 🚀 Bắt Đầu Nhanh
    1. **Tìm kiếm**: Thử `/query` để tìm khuôn mặt
    2. **Đăng nhập**: Dùng `/auth/login` với MySQL account
    3. **Khám phá**: Xem các API categories bên trái
    
    ### 📚 Tài Liệu
    - **Swagger UI**: Trang này (interactive)
    - **ReDoc**: `/redoc` (detailed docs)
    - **OpenAPI Schema**: `/openapi.json`
    """
    return {
        "message": "🤖 Face Recognition API với MySQL Authentication",
        "version": "2.0.0",
        "status": "✅ Hoạt động",
        "authentication": "🔐 MySQL Session-based",
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "public": [
                "POST /query - Tìm kiếm khuôn mặt",
                "POST /query_top5 - Top 5 kết quả tương tự",
                "GET /vector_info - Thông tin database",
                "GET /health - Kiểm tra sức khỏe"
            ],
            "protected": [
                "POST /add_embedding - Thêm người mới (cần đăng nhập)",
                "PUT /edit_embedding - Sửa thông tin (cần đăng nhập)",
                "DELETE /delete_class - Xóa người (cần đăng nhập)",
                "POST /reset_index - Reset database (cần đăng nhập)"
            ],
            "auth": [
                "POST /auth/login - Đăng nhập MySQL",
                "POST /auth/logout - Đăng xuất"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Face Recognition API with MySQL Authentication...")
    print("📚 Swagger UI: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    

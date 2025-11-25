"""
MySQL Authentication API Endpoints
File: auth/mysql_auth_api.py
"""

from fastapi import APIRouter, HTTPException, status, Response, Depends, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .mysql_auth import mysql_auth, get_current_user_mysql, get_current_user_optional
from db.nguoi_repository import NguoiRepository

router = APIRouter(prefix="/auth", tags=["🔐 MySQL Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    username: str
    token: str

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Đăng nhập với MySQL account",
    description="""
    **Đăng nhập hệ thống bằng tài khoản MySQL**
    
    API này cho phép:
    - 🔐 Đăng nhập bằng username/password từ table `taikhoan`
    - 🍪 Tạo session cookie tự động
    - ⏰ Session có hiệu lực 24 giờ
    
    **Sau khi đăng nhập thành công:**
    - Cookie `session_token` sẽ được set tự động
    - Có thể sử dụng các Protected APIs (add, edit, delete)
    
    **Cách sử dụng:**
    - Input: username và password
    - Output: Thông tin đăng nhập + session cookie
    """
)
def login(
    username: str = Form(..., description="Username trong MySQL table taikhoan"), 
    password: str = Form(..., description="Password trong MySQL table taikhoan")
):
    """Đăng nhập với MySQL database"""
    
    # Authenticate với MySQL
    if not mysql_auth.authenticate_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai username hoặc password"
        )
    
    # Tìm role từ nhanvien
    try:
        nguoi_repo = NguoiRepository()
        nguoi = nguoi_repo.get_by_username(username)
        role = getattr(nguoi, 'role', None) if nguoi else None
    except Exception:
        role = None

    # Tạo session (lưu cả role nếu có)
    session_token = mysql_auth.create_session(username, role=role)
    
    # Tạo response với token
    response_data = {
        "success": True,
        "message": f"Đăng nhập thành công với user {username}",
        "username": username,
        "token": session_token,  # Return token in response
        "role": role
    }
    
    # Create JSONResponse để có thể set cookie
    response = JSONResponse(content=response_data)
    response.set_cookie(
        key="session_token",
        value=session_token,
        max_age=86400,  # 24 hours
        httponly=False,  # Allow JS access
        secure=False,    # Set to True in production with HTTPS
        samesite="lax"   # CSRF protection
    )
    
    print(f"✅ User {username} đăng nhập thành công, session: {session_token[:20]}...")
    return response

@router.post(
    "/logout",
    summary="Đăng xuất",
    description="**Đăng xuất và xóa session**"
)
def logout(response: Response, current_user: str = Depends(get_current_user_mysql)):
    """Đăng xuất hệ thống"""
    
    # Get session token from request (need to implement)
    session_token = None  # We'll handle this in the dependency
    
    response_data = {
        "success": True,
        "message": f"User {current_user} đã đăng xuất"
    }
    
    # Clear cookie
    response = JSONResponse(content=response_data)
    response.delete_cookie(key="session_token")
    
    print(f"✅ User {current_user} đăng xuất")
    return response

@router.get(
    "/me",
    summary="Thông tin user hiện tại",
    description="**Lấy thông tin user đang đăng nhập**"
)
def get_current_user_info(current_user: str = Depends(get_current_user_mysql)):
    """Lấy thông tin user hiện tại"""
    return {
        "username": current_user,
        "status": "logged_in",
        "message": f"Bạn đang đăng nhập với user {current_user}"
    }

@router.get(
    "/status",
    summary="Kiểm tra trạng thái đăng nhập", 
    description="**Kiểm tra user có đang đăng nhập không (optional)**"
)
def auth_status(current_user: str = Depends(get_current_user_optional)):
    """Kiểm tra trạng thái authentication"""
    if current_user:
        return {
            "authenticated": True,
            "username": current_user,
            "message": f"Đã đăng nhập với user {current_user}"
        }
    else:
        return {
            "authenticated": False,
            "username": None,
            "message": "Chưa đăng nhập"
        }

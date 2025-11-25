from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.taikhoan_repository import TaiKhoanRepository
from db.nguoi_repository import NguoiRepository

taikhoan_router = APIRouter()


@taikhoan_router.get('/taikhoan/{username}', summary='Lấy thông tin user theo username (nếu có profile)')
def get_taikhoan_by_username(username: str):
    # First try to find a user profile in nhanvien
    nguoi_repo = NguoiRepository()
    nguoi = nguoi_repo.get_by_username(username)
    if nguoi:
        data = nguoi.to_dict(include_avatar_base64=False)
        return JSONResponse(content={'success': True, 'user': data})

    # Fallback: return account info from taikhoan table if exists
    repo = TaiKhoanRepository()
    taikhoan = repo.get_by_username(username)
    if taikhoan:
        return JSONResponse(content={'success': True, 'taikhoan': {'username': taikhoan.username}})

    return JSONResponse(content={'success': False, 'message': 'Không tìm thấy tài khoản hoặc user'}, status_code=404)

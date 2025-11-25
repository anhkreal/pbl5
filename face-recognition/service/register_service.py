from db.taikhoan_repository import TaiKhoanRepository
from db.models import TaiKhoan

def register_service(username: str, passwrd: str):
    repo = TaiKhoanRepository()
    # Kiểm tra tồn tại
    if repo.get_by_username(username):
        return False, "Tên đăng nhập đã tồn tại"
    # Thêm mới
    repo.add(TaiKhoan(username=username, passwrd=passwrd))
    return True, "Đăng ký thành công"

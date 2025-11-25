from db.taikhoan_repository import TaiKhoanRepository

def login_service(username: str, passwrd: str):
    repo = TaiKhoanRepository()
    return repo.check_login(username, passwrd)

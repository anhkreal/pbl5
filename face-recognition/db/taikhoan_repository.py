from db.models import TaiKhoan
from db.connection_helper import ConnectionHelper
from typing import Optional


class TaiKhoanRepository(ConnectionHelper):
    """Repository cho bảng `taikhoan`.

    - map DB rows to `TaiKhoan` dataclass via `from_row`
    - provide authenticate() that returns the TaiKhoan on success
    - keep check_login() for backward compatibility (returns bool)
    """

    def add(self, taikhoan: TaiKhoan):
        sql = "INSERT INTO taikhoan (username, passwrd) VALUES (%s, %s)"
        with self as cursor:
            cursor.execute(sql, (taikhoan.username, taikhoan.passwrd))

    def get_by_username(self, username: str) -> Optional[TaiKhoan]:
        sql = "SELECT * FROM taikhoan WHERE username = %s"
        with self as cursor:
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                return TaiKhoan.from_row(row)
            return None

    def authenticate(self, username: str, passwrd: str) -> Optional[TaiKhoan]:
        """Authenticate username/password and return TaiKhoan if valid, otherwise None.

        NOTE: passwords are stored in plaintext per current schema. For production,
        replace this with hashed passwords (bcrypt) and compare hashes instead.
        """
        sql = "SELECT * FROM taikhoan WHERE username = %s AND passwrd = %s"
        with self as cursor:
            cursor.execute(sql, (username, passwrd))
            row = cursor.fetchone()
            if row:
                return TaiKhoan.from_row(row)
            return None

    def check_login(self, username: str, passwrd: str) -> bool:
        """Compatibility wrapper returning boolean for successful login."""
        return self.authenticate(username, passwrd) is not None

    def update_password(self, username: str, new_passwrd: str) -> int:
        """Update password for a username. Returns number of affected rows."""
        sql = "UPDATE taikhoan SET passwrd = %s WHERE username = %s"
        with self as cursor:
            cursor.execute(sql, (new_passwrd, username))
            return cursor.rowcount

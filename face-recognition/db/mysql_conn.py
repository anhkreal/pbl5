import pymysql

# Thông tin kết nối MySQL (XAMPP mặc định)
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Mặc định XAMPP không có mật khẩu cho root
MYSQL_DB = 'testtest'  # Đặt tên database bạn muốn sử dụng

# Hàm tạo kết nối MySQL

def get_connection():
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

# Ví dụ sử dụng:
if __name__ == '__main__':
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT VERSION()')
            version = cursor.fetchone()
            print('MySQL version:', version)
        conn.close()
    except Exception as e:
        print('Kết nối MySQL thất bại:', e)

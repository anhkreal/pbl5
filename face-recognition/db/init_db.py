"""Database initializer.

Creates the MySQL database named in `mysql_conn.MYSQL_DB` and the tables
used by this project. Safe to run multiple times (uses IF NOT EXISTS).

Usage:
    python db/init_db.py

The script connects to the MySQL server using credentials from
`db/mysql_conn.py`. If your MySQL user does not have privilege to create
databases, run the CREATE DATABASE step manually or use a privileged user.
"""
from __future__ import annotations
import traceback
import os
import sys

# Ensure project root is on sys.path so `from db import mysql_conn` works
# regardless of current working directory or whether the script is executed
# directly (python db/init_db.py) or as a module (python -m db.init_db).
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from db import mysql_conn
import pymysql


TABLE_SQLS = [
    # accounts
    """
    CREATE TABLE IF NOT EXISTS taikhoan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        passwrd VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # people / employees
    """
    CREATE TABLE IF NOT EXISTS nhanvien (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        pin VARCHAR(50),
        full_name VARCHAR(255),
        age INT,
        address TEXT,
        phone VARCHAR(50),
        gender VARCHAR(50),
        role VARCHAR(50),
        shift VARCHAR(50),
        status VARCHAR(50),
        avatar_url LONGBLOB,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # face images
    """
    CREATE TABLE IF NOT EXISTS khuonmat (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        image_url LONGBLOB,
        added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        CONSTRAINT fk_khuonmat_user FOREIGN KEY (user_id) REFERENCES nhanvien(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # emotion logs
    """
    CREATE TABLE IF NOT EXISTS emotion_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        camera_id INT,
        emotion_type VARCHAR(100),
        confidence DOUBLE,
        captured_at DATETIME,
        image LONGBLOB,
        note TEXT,
        CONSTRAINT fk_emotion_user FOREIGN KEY (user_id) REFERENCES nhanvien(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # cameras
    """
    CREATE TABLE IF NOT EXISTS camera (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        ip_address VARCHAR(100),
        port INT,
        protocol VARCHAR(50),
        username VARCHAR(100),
        password VARCHAR(255),
        stream_name VARCHAR(255),
        location VARCHAR(255),
        status VARCHAR(50),
        last_connected DATETIME
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # attendance / check logs
    """
    CREATE TABLE IF NOT EXISTS checklog (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        date DATE,
        check_in DATETIME,
        check_out DATETIME,
        total_hours DOUBLE,
        shift VARCHAR(50),
        status VARCHAR(50),
        edited_by INT,
        note TEXT,
        CONSTRAINT fk_checklog_user FOREIGN KEY (user_id) REFERENCES nhanvien(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # kpi
    """
    CREATE TABLE IF NOT EXISTS kpi (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        date DATE,
        emotion_score DOUBLE,
        attendance_score DOUBLE,
        total_score DOUBLE,
        remark TEXT,
        CONSTRAINT fk_kpi_user FOREIGN KEY (user_id) REFERENCES nhanvien(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
]


def create_database_and_tables(host=None, port=None, user=None, password=None, db_name=None):
    host = host or mysql_conn.MYSQL_HOST
    port = port or mysql_conn.MYSQL_PORT
    user = user or mysql_conn.MYSQL_USER
    password = password if password is not None else mysql_conn.MYSQL_PASSWORD
    db_name = db_name or mysql_conn.MYSQL_DB

    # Connect without specifying database to allow CREATE DATABASE
    conn = None
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password,
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
                               autocommit=False)
        with conn.cursor() as cursor:
            print(f"Creating database {db_name} if not exists...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.execute(f"USE `{db_name}`;")
            for sql in TABLE_SQLS:
                print("Executing table DDL...")
                cursor.execute(sql)
        conn.commit()
        print("Database and tables created/verified successfully.")
    except Exception as e:
        if conn:
            conn.rollback()
        print("Error while creating database/tables:")
        traceback.print_exc()
        raise
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    print("Initializing MySQL database and tables...")
    create_database_and_tables()
    print("Done.")

import os
import sys
import random
from datetime import date, datetime, timedelta

# Ensure project root is on sys.path so imports like `db.*` work when running
# this script directly from the `scripts/` folder.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from db.nguoi_repository import NguoiRepository
from db.taikhoan_repository import TaiKhoanRepository
from db.connection_helper import ConnectionHelper


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def seed(dry_run=True):
    nguoi_repo = NguoiRepository()
    taikhoan_repo = TaiKhoanRepository()

    # Counters for reporting
    counters = {
        'nhanvien': {'ok': 0, 'fail': 0},
        'taikhoan': {'ok': 0, 'fail': 0},
        'checklog': {'ok': 0, 'fail': 0},
        'emotion_log': {'ok': 0, 'fail': 0},
        'kpi': {'ok': 0, 'fail': 0}
    }

    # Create some mock users
    users = []
    shifts = ['day', 'night', 'swing']
    for i in range(1, 21):
        u = {
            'username': f'user{i}',
            'full_name': f'User {i}',
            'age': random.randint(20, 45),
            'address': f'Address {i}',
            'phone': f'09{random.randint(100000,999999)}',
            'gender': random.choice(['male','female']),
            'role': random.choice(['staff','manager','supervisor']),
            'shift': random.choice(shifts),
            'status': 'working',
            'pin': str(1000 + i)
        }
        users.append(u)

    # Insert users and accounts
    with ConnectionHelper() as cursor:
        for u in users:
            # insert nhanvien
            try:
                cursor.execute(
                    'REPLACE INTO nhanvien (username, pin, full_name, age, address, phone, gender, role, shift, status, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (
                        u['username'], u['pin'], u['full_name'], u['age'], u['address'], u['phone'], u['gender'], u['role'], u['shift'], u['status'], datetime.utcnow(), datetime.utcnow()
                    )
                )
                counters['nhanvien']['ok'] += 1
            except Exception:
                counters['nhanvien']['fail'] += 1

            # insert taikhoan with same username and simple password
            try:
                cursor.execute('REPLACE INTO taikhoan (username, passwrd) VALUES (%s,%s)', (u['username'], 'password'))
                counters['taikhoan']['ok'] += 1
            except Exception:
                counters['taikhoan']['fail'] += 1

    # Date range: 2025-09-01 .. 2025-11-15
    start_date = date(2025, 9, 1)
    end_date = date(2025, 11, 15)

    # For each user, create checklogs for each date
    with ConnectionHelper() as cursor:
        for u in users:
            # lookup user id
            cursor.execute('SELECT id FROM nhanvien WHERE username = %s LIMIT 1', (u['username'],))
            row = cursor.fetchone()
            if not row:
                continue
            user_id = row['id']

            for d in daterange(start_date, end_date):
                # simulate presence majority on-time, with some absences/late/early
                rand = random.random()
                if rand < 0.03:
                    # absent whole day - insert no checkin (skip)
                    continue
                check_in = datetime(d.year, d.month, d.day, 8, 0)
                check_out = datetime(d.year, d.month, d.day, 17, 0)
                # small chance late or early leave
                if random.random() < 0.05:
                    # late 5-30 minutes
                    minutes = random.randint(5, 30)
                    check_in = check_in + timedelta(minutes=minutes)
                if random.random() < 0.04:
                    # early leave 5-45 minutes
                    minutes = random.randint(5, 45)
                    check_out = check_out - timedelta(minutes=minutes)

                try:
                    cursor.execute('INSERT INTO checklog (user_id, date, check_in, check_out, shift, status) VALUES (%s, %s, %s, %s, %s, %s)',
                                   (user_id, d, check_in, check_out, u['shift'], 'working'))
                    counters['checklog']['ok'] += 1
                except Exception:
                    counters['checklog']['fail'] += 1

                # Emotion logs: 1-5 negative logs per day randomly
                negative_count = 0
                if random.random() < 0.3:
                    negative_count = random.randint(1, 5)
                for _ in range(negative_count):
                    ts = datetime(d.year, d.month, d.day, random.randint(8, 17), random.randint(0, 59), random.randint(0, 59))
                    try:
                        cursor.execute('INSERT INTO emotion_log (user_id, camera_id, emotion_type, confidence, image, captured_at, note) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                                       (user_id, None, 'sad', round(random.uniform(0.5, 0.95), 2), b'\x00', ts, 'auto-seed'))
                        counters['emotion_log']['ok'] += 1
                    except Exception:
                        counters['emotion_log']['fail'] += 1

                # KPI insert for this date (use emotion_score, attendance_score, total_score)
                try:
                    emotion_score = round(random.uniform(0, 100), 2)
                    attendance_score = round(random.uniform(60, 100), 2)
                    total_score = round((emotion_score * 0.4) + (attendance_score * 0.6), 2)
                    cursor.execute('INSERT INTO kpi (user_id, date, emotion_score, attendance_score, total_score, remark) VALUES (%s, %s, %s, %s, %s, %s)',
                                   (user_id, d, emotion_score, attendance_score, total_score, 'auto-seed'))
                    counters['kpi']['ok'] += 1
                except Exception:
                    counters['kpi']['fail'] += 1

    # Print summary
    print('Seeding completed (dry_run=' + str(dry_run) + ')')
    print('\nSummary:')
    for table, stats in counters.items():
        print(f" - {table}: {stats['ok']} inserted, {stats['fail']} failed")


if __name__ == '__main__':
    seed(dry_run=False)

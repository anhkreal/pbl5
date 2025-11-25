import os
import sys
from datetime import date, datetime

# Ensure project root is on sys.path for imports
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from db.connection_helper import ConnectionHelper


def update_roles():
    ok = 0
    fail = 0
    with ConnectionHelper() as cursor:
        try:
            # Set role='user' for all nhanvien except id=2
            cursor.execute("UPDATE nhanvien SET role = 'user' WHERE id != 2")
            ok = cursor.rowcount
        except Exception:
            fail += 1
    return ok, fail


def kpi_has_rows():
    with ConnectionHelper() as cursor:
        cursor.execute('SELECT COUNT(*) as cnt FROM kpi')
        r = cursor.fetchone()
        return (r and r.get('cnt', 0) > 0)


def populate_kpi(start_date: date, end_date: date):
    ok = 0
    fail = 0
    with ConnectionHelper() as cursor:
        # get all user ids
        cursor.execute('SELECT id FROM nhanvien')
        users = [r['id'] for r in cursor.fetchall()]
        d = start_date
        while d <= end_date:
            for uid in users:
                try:
                    emotion_score = round((uid % 100) * 0.8 + (d.day % 10), 2) % 100
                    attendance_score = round(60 + (uid % 40) + (d.day % 5), 2)
                    total_score = round((emotion_score * 0.4) + (attendance_score * 0.6), 2)
                    cursor.execute('INSERT INTO kpi (user_id, date, emotion_score, attendance_score, total_score, remark) VALUES (%s, %s, %s, %s, %s, %s)', (uid, d, emotion_score, attendance_score, total_score, 'auto-generated'))
                    ok += 1
                except Exception:
                    fail += 1
            d = d.fromordinal(d.toordinal() + 1)
    return ok, fail


def compute_total_hours():
    ok = 0
    fail = 0
    with ConnectionHelper() as cursor:
        cursor.execute('SELECT id, check_in, check_out FROM checklog WHERE check_in IS NOT NULL AND check_out IS NOT NULL')
        rows = cursor.fetchall()
        for r in rows:
            try:
                cid = r['id']
                ci = r['check_in']
                co = r['check_out']
                if not ci or not co:
                    continue
                # ensure datetime objects
                if isinstance(ci, str):
                    ci = datetime.fromisoformat(ci)
                if isinstance(co, str):
                    co = datetime.fromisoformat(co)
                total_hours = (co - ci).total_seconds() / 3600.0
                cursor.execute('UPDATE checklog SET total_hours = %s WHERE id = %s', (round(total_hours, 2), cid))
                ok += 1
            except Exception:
                fail += 1
    return ok, fail


def main():
    print('Updating roles...')
    ok_roles, fail_roles = update_roles()
    print(f'Roles updated: {ok_roles} rows affected, {fail_roles} failures')

    print('Checking KPI table...')
    if not kpi_has_rows():
        print('KPI empty. Populating KPI...')
        start_date = date(2025, 9, 1)
        end_date = date(2025, 11, 15)
        ok_kpi, fail_kpi = populate_kpi(start_date, end_date)
        print(f'KPI inserted: {ok_kpi}, failures: {fail_kpi}')
    else:
        print('KPI already has data; skipping population')

    print('Computing total_hours for checklog...')
    ok_ch, fail_ch = compute_total_hours()
    print(f'checklog updated: {ok_ch} rows, failures: {fail_ch}')


if __name__ == '__main__':
    main()

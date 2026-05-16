import pymysql
import random
from datetime import datetime, timedelta

conn = pymysql.connect(
    host='192.168.10.220',
    user='r3213ascdho',
    password='Awewewewewewewe',
    database='124scdasdas',
    cursorclass=pymysql.cursors.DictCursor
)

WHERE_ROW = "idm = %s AND pic = %s AND kode_unit = %s AND tanggal = %s"

def row_params(r):
    return (r['idm'], r['pic'], r['kode_unit'], r['tanggal'])

def next_weekday(dt, target_weekday):
    days_ahead = target_weekday - dt.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return dt + timedelta(days=days_ahead)

def adjust_date(tanggal):
    if isinstance(tanggal, str):
        tanggal = datetime.strptime(tanggal, '%Y-%m-%d %H:%M:%S')
    elif hasattr(tanggal, 'year') and not hasattr(tanggal, 'hour'):
        tanggal = datetime.combine(tanggal, datetime.min.time())
    result = tanggal + timedelta(minutes=30)
    result += timedelta(minutes=random.randint(10, 50))
    result += timedelta(seconds=random.randint(2, 57))
    wd = result.weekday()
    if wd == 5:
        result = next_weekday(result, 0)
    elif wd == 6:
        result = next_weekday(result, 1)
    return result

try:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM mtc_checklist
            WHERE MONTH(tanggal) = 5
            AND pic = 'sastra'
            AND idm = 10
            -- AND kode_unit = 'C-010'
            AND id_div = 'SEC'
        """)
        rows = cur.fetchall()

        print(f"=== Total rows: {len(rows)} ===")
        for r in rows:
            print(r)

        if not rows:
            print("Tidak ada data ditemukan.")
            exit()

        fields_y = [
            'casing_luar','casing_dalam','power_supply','monitor','keyboard_mouse',
            'putaran_fan','fungsi_hardware','disk_defrag','registry_defrag',
            'registry_cleanup','scan_virus','update_anti_virus','delete_temp_file',
            'backup_data','disk_cleanup','software_office','software_erp',
            'periksa_potensi_rusak','pengaturan_kabel_rapi','software_illegal','user_approve'
        ]
        set_y = ', '.join(f"{f}='Y'" for f in fields_y)
        count3 = 0
        for r in rows:
            cur.execute(f"UPDATE mtc_checklist SET {set_y} WHERE {WHERE_ROW}", row_params(r))
            count3 += cur.rowcount
        print(f"\n[3] Updated {count3} rows -> semua field = 'Y'")

        for r in rows:
            tgl_selesai = adjust_date(r['tanggal'])
            r['_tgl_selesai'] = tgl_selesai
            cur.execute(
                f"UPDATE mtc_checklist SET tgl_selesai = %s WHERE {WHERE_ROW}",
                (tgl_selesai, *row_params(r))
            )
            print(f"  idm={r['idm']} kode_unit={r['kode_unit']} tanggal={r['tanggal']} -> tgl_selesai={tgl_selesai}")
        print(f"\n[4] Updated tgl_selesai untuk {len(rows)} rows")

        for r in rows:
            ts = r['_tgl_selesai']
            mail_dt = ts + timedelta(seconds=random.randint(1, 3))
            r['_mail'] = mail_dt
            cur.execute(
                f"UPDATE mtc_checklist SET mail = %s WHERE {WHERE_ROW}",
                (mail_dt, *row_params(r))
            )
            print(f"  idm={r['idm']} kode_unit={r['kode_unit']} tgl_selesai={ts} -> mail={mail_dt}")
        print(f"\n[5] Updated mail untuk {len(rows)} rows")

        for r in rows:
            mail = r['_mail']
            tgl_ua = mail + timedelta(
                days=random.randint(0, 2),
                hours=random.randint(1, 6),
                minutes=random.randint(1, 58),
                seconds=random.randint(1, 50)
            )
            cur.execute(
                f"UPDATE mtc_checklist SET tgl_user_approve = %s WHERE {WHERE_ROW}",
                (tgl_ua, *row_params(r))
            )
            print(f"  idm={r['idm']} kode_unit={r['kode_unit']} mail={mail} -> tgl_user_approve={tgl_ua}")
        print(f"\n[6] Updated tgl_user_approve untuk {len(rows)} rows")

        count7 = 0
        for r in rows:
            cur.execute(
                f"UPDATE mtc_checklist SET status_mtc = 'finish' WHERE {WHERE_ROW}",
                row_params(r)
            )
            count7 += cur.rowcount
        print(f"\n[7] Updated status_mtc='finish' untuk {count7} rows")

        conn.commit()
        print("\n=== SEMUA UPDATE BERHASIL (commit) ===")

finally:
    conn.close()

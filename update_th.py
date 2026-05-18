import mysql.connector
import random
from datetime import datetime

# =========================
# KONFIGURASI DATABASE
# =========================
db = mysql.connector.connect(
    host="localhost",
    user="contoh",
    password="contoh",
    database="contoh"
)

cursor = db.cursor(dictionary=True)

# =========================
# WAKTU SEKARANG
# =========================
now = datetime.now()

current_date = now.strftime('%Y-%m-%d')
current_hour = now.strftime('%H')

# weekday():
# Senin=0 ... Minggu=6
is_sunday = now.weekday() == 6

# =========================
# AMBIL DEVICE
# =========================
cursor.execute("""
    SELECT device_id, average_data, device_name, ip_address
    FROM device
""")

devices = cursor.fetchall()

for device in devices:

    device_id = device['device_id']
    average_data = device['average_data']
    device_name = device['device_name']
    ip_address = device['ip_address']

    # format:
    # suhu_weekday,hum_weekday,suhu_sunday,hum_sunday
    try:
        avg_temp_weekday, avg_hum_weekday, avg_temp_sunday, avg_hum_sunday = map(
            float,
            average_data.split(',')
        )
    except Exception as e:
        print(f"Gagal parsing average_data device {device_id}: {e}")
        continue

    # =========================
    # PILIH DATA BERDASARKAN HARI
    # =========================
    if is_sunday:
        base_temp = avg_temp_sunday
        base_hum = avg_hum_sunday
    else:
        base_temp = avg_temp_weekday
        base_hum = avg_hum_weekday

    # =========================
    # CEK APAKAH DATA SUDAH ADA
    # =========================
    cursor.execute("""
        SELECT device_id
        FROM data_suhu
        WHERE device_id = %s
        AND DATE(date) = %s
        AND HOUR(date) = %s
        LIMIT 1
    """, (device_id, current_date, current_hour))

    existing = cursor.fetchone()

    # =========================
    # JIKA BELUM ADA → INSERT
    # =========================
    if not existing:

        # random naik/turun
        temp_random = random.uniform(0.1, 0.5)
        hum_random = random.uniform(0.1, 1)

        # random plus/minus
        suhu = round(
            base_temp + random.choice([-1, 1]) * temp_random,
            2
        )

        kelembapan = round(
            base_hum + random.choice([-1, 1]) * hum_random,
            2
        )

        cursor.execute("""
            INSERT INTO data_suhu
            (
                device_id,
                device_name,
                temperature,
                humidity,
                ip_address,
                date
            )
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (
            device_id,
            device_name,
            suhu,
            kelembapan,
            ip_address
        ))

        # =========================
        # UPDATE TABLE DEVICE
        # =========================
        cursor.execute("""
            UPDATE device
            SET
                temperature = %s,
                humidity = %s,
                updated_date = NOW()
            WHERE device_id = %s
        """, (
            suhu,
            kelembapan,
            device_id
        ))

        db.commit()

        print(f"Insert dummy data -> {device_id} | suhu={suhu} | hum={kelembapan}")

    else:
        print(f"Data sudah ada -> {device_id}")

# =========================
# CLOSE
# =========================
cursor.close()
db.close()

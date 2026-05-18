import speedtest
import mysql.connector
from datetime import datetime
import subprocess
import json

# isp = "Iforte"

DB_CONFIG = {
    "host": "localhost",
    "user": "contoh",
    "password": "contoh",
    "database": "contoh"
}

def run_speedtest():
    result = subprocess.run(
        ["speedtest", "--json"],
        capture_output=True,
        text=True
    )
    
    data = json.loads(result.stdout)

    ping = data["ping"]
    download = data["bytes_received"] / 1_000_000
    upload = data["upload"] / 1_000_000
    server = data["server"]["name"]
    isp = data["client"]["isp"]

    return isp, ping, download, upload, server

    # st = speedtest.Speedtest()

    # st.get_best_server()

    # download = st.download() / 1_000_000
    # upload = st.upload() / 1_000_000
    # ping = st.results.ping
    # server = st.results.server['name']

    # return ping, download, upload, server

def save_results(isp, download, upload, ping, timestamp, server):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query = """
        INSERT INTO isp_speedtest (isp, download_mbps, upload_mbps, ping_ms, created_at, server_city)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        isp,
        download, 
        upload, 
        ping, 
        timestamp,
        server))
    conn.commit()

    cursor.close()
    conn.close()

def main():
    isp, ping, download, upload, server = run_speedtest()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    save_results(
        isp, 
        float("{0:.2f}".format(download)),
        float("{0:.2f}".format(upload)),
        float("{0:.2f}".format(ping)),
        timestamp,
        server
    )
    
if __name__ == "__main__":
    main()

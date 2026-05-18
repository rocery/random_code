import mysql.connector
import subprocess
import re

db_config = {
    'host': 'locallost',
    'user': 'd21',
    'password': 'sda21',
    'database': 'asdsdwawikwok'
}

def ping(ip_address):
    """Ping the IP address and return detailed results including time, packet loss, etc."""
    try:
        # Use subprocess to ping the IP address and capture the output
        result = subprocess.run(['ping', '-c', '8', ip_address], capture_output=True, text=True)
        
        # Check if ping was successful
        if result.returncode == 0:
            output = result.stdout
            # Extract the packet loss and time information using regex
            packet_loss = re.search(r'(\d+)% packet loss', output).group(1)
            time_info = re.search(r'rtt min/avg/max/mdev = ([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+) ms', output)
            
            if time_info:
                min_time = time_info.group(1)
                avg_time = time_info.group(2)
                max_time = time_info.group(3)
                mdev_time = time_info.group(4)
                
                return {
                    'reachable': True,
                    'packet_loss': f"{packet_loss}%",
                    'min_time': f"{min_time} ms",
                    'avg_time': f"{avg_time} ms",
                    'max_time': f"{max_time} ms",
                    'mdev_time': f"{mdev_time} ms"
                }
        else:
            return {'reachable': False}

    except Exception as e:
        #print(f"Failed to ping {ip_address}: {e}")
        return {'reachable': False}

def update_ping_status(connection, device_name, ping_data):
    """Update the 'ping' column in the 'device' table with the ping data."""
    cursor = connection.cursor()

    # Format the data for the 'ping' column
    if ping_data['reachable']:
        ping_summary = (
            f"Reachable, Packet Loss: {ping_data['packet_loss']}, "
            f"Min Time: {ping_data['min_time']}, Avg Time: {ping_data['avg_time']}, "
            f"Max Time: {ping_data['max_time']}, MDev Time: {ping_data['mdev_time']}"
        )
    else:
        ping_summary = "Unreachable"

    # SQL query to update the 'ping' column
    update_query = "UPDATE device SET ping = %s WHERE device_name = %s"
    cursor.execute(update_query, (ping_summary, device_name))
    
    # Commit the changes to the database
    connection.commit()
    #print(f"Updated ping status for {device_name}")
    
while True:
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(**db_config)
        
        if connection.is_connected():
            print("Connected to the database.")
            
            # Create a cursor object to interact with the database
            cursor = connection.cursor()

            # SQL query to fetch both device_name and ip_address from the 'device' table
            query = "SELECT device_name, ip_address FROM device"
            cursor.execute(query)

            # Fetch all rows from the executed query
            result = cursor.fetchall()

            # Check if any devices were found
            if result:
                print("Devices and their ping status:")
                for row in result:
                    device_name = row[0]  # device_name is in the first column
                    print(device_name)
                    ip = row[1]           # ip_address is in the second column
                    print(ip)
                    # Ping the IP address and get detailed results
                    ping_result = ping(ip)
                    
                    if ping_result['reachable']:
                        print(f"Device: {device_name}, IP: {ip} - Reachable")
                        print(f"  Packet Loss: {ping_result['packet_loss']}")
                        print(f"  Min Time: {ping_result['min_time']}")
                        print(f"  Avg Time: {ping_result['avg_time']}")
                        print(f"  Max Time: {ping_result['max_time']}")
                        print(f"  MDev Time: {ping_result['mdev_time']}")
                    else:
                        print(f"Device: {device_name}, IP: {ip} - Unreachable")
                    
                    # Update the 'ping' column in the database
                    update_ping_status(connection, device_name, ping_result)
            else:
                print("No devices found in 'device' table.")

    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection closed.")

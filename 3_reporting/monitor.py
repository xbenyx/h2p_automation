import subprocess
import sqlite3
import requests
import json
import smtplib
import sys
import paramiko
sys.path.append('./utils')
from config_utils import load_config, load_token
import db_utils
from configparser import ConfigParser

def get_status_description(status):
    status_map = {
        0: "unCracked",
        1: "Partially Cracked",
        2: "Cracked"
    }
    return status_map.get(status, str(status))

def create_file(name, status, hashlistid, hashes):
    # Load config
    config = load_config()
    # Folder remote directory for creating files
    sftp_config = config.get('sftp', {})
    # Create the file name
    filename = f"{name}_{status}_{hashlistid}.txt"
    # Write hashes to the file
    with open(filename, 'w') as file:
        print(hashes)
        for hash_value in hashes:
            file.write(hash_value + '\n')

        # Write metadata to the file
        file.write("\nMetadata:\n")
        file.write(f"Name: {name}\n")
        file.write(f"Status: {get_status_description(status)}\n")
        file.write(f"Hashmode: {hashlistid}\n")

    # Connect to SFTP
    transport = paramiko.Transport((sftp_config['hostname'], sftp_config['port']))
    transport.connect(username=sftp_config['username'], password=sftp_config['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Upload the file to the remote directory
    remote_path = f"{sftp_config['remote_directory_post']}/{filename}"
    sftp.put(filename, remote_path)

    # Close the SFTP connection
    sftp.close()
    transport.close()

# Function to monitor cracked hashlists
def monitor_hashlists(conn):
    config = load_config()
    token = load_token()
    # Connect to the database
    cursor = conn.cursor()

    # Fetch rows from Hashlists table where Cracked is 0 or 1
    cursor.execute("SELECT * FROM Hashlists WHERE Status IN (0,1)")
    rows = cursor.fetchall()
    print(rows)
    # Iterate over the rows and make API calls
    for row in rows:
        hashlist_id = row[1]  # Assuming hashlist_id is at index 1, adjust accordingly
        url = config['backend']['backend_url'] + f'/ui/hashlists/{hashlist_id}'
        params = {'expand': 'hashes'}
        headers = {'Authorization': f'Bearer {load_token()}'}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data)
            name_db = row[0]
            cracked_db = row[4]
            cracked = data.get('cracked')
            hashcount = data.get('hashCount')
            hashes = data.get('hashes')
            status = row[3]
            plaintext_hashes = []
            for hash_data in hashes:
                if hash_data.get('isCracked', False):
                if not hash_data.get('isCracked', False):
                    plaintext = hash_data.get('hash')
                    if plaintext:
                        plaintext_hashes.append(plaintext)

            # if cracked > cracked_db:
            if cracked >= cracked_db:
                # Create New file
                create_file(name_db, status, hashlist_id, plaintext_hashes)
                # Save changes to database
                if cracked == hashcount:
                    # Update status to Cracked (2) for hashes where status is 2 (Cracked)
                    update_status_in_database(hashlist_id, 2)
                else:
                    # Update status to Partially Cracked (1) for hashes where status is 1 (Partially Cracked)
                    # Update also Cracked and Cracked
                    update_status_in_database(hashlist_id, 1, cracked, hashcount)

        elif response.status_code == 401:
            # Handle 401 Unauthorized status code
            # Run token manager script
            subprocess.run(["python", "token/token_manager.py"])
            # Re-run monitor_hashlists after token_manager completes
            monitor_hashlists(conn)
        else:
            print(f"Failed to fetch data for hashlist ID {hashlist_id}")

    # Close database connection
    conn.close()

def connect_to_sftp(self, sftp_config):
    transport = paramiko.Transport((sftp_config['hostname'], sftp_config['port']))
    transport.connect(username=sftp_config['username'], password=sftp_config['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp

def update_status_in_database(hashlist_id, status, cracked=None, hashcount=None):
    try:
        conn = db_utils.establish_connection()
        cursor = conn.cursor()
        if cracked is not None and hashcount is not None:
            cursor.execute("UPDATE Hashlists SET Status = ?, Cracked = ?, Hashcount = ? WHERE HashlistId = ?", (status, cracked, hashcount, hashlist_id))
        else:
            cursor.execute("UPDATE Hashlists SET Status = ? WHERE HashlistId = ?", (status, hashlist_id))
        conn.commit()
    except Exception as e:
        print("An error occurred while updating the status in the database:", e)
    finally:
        if 'conn' in locals():
            db_utils.close_connection(conn)

if __name__ == "__main__":
    try:
        conn = db_utils.establish_connection()
        monitor_hashlists(conn)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        if 'conn' in locals():
            db_utils.close_connection(conn)


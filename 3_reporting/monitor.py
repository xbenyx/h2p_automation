import subprocess
import sqlite3
import requests
import json
import smtplib
import sys
sys.path.append('./utils')
from config_utils import load_config, load_token
import db_utils
from configparser import ConfigParser

def create_file(name, status, hashlistid, hashes):
    # Load config
    config = load_config()
    # Folder remote directory for creating files
    remote_directory_post = config.get('sftp', {}).get('remote_directory_post')
    # Create the file name
    filename = f"{name}_{status}_{hashlistid}.txt"

    # Write hashes to the file
    # with open(filename, 'w') as file:
    #     for hash_value in hashes:
    #         file.write(hash_value + '\n')

    #     # Write metadata to the file
    #     file.write("\nMetadata:\n")
    #     file.write(f"Name: {name}\n")
    #     file.write(f"Status: {status}\n")
    #     file.write(f"Hashmode: {hashlistid}\n")

# Function to monitor cracked hashlists
def monitor_hashlists(conn):
    config = load_config()
    token = load_token()
    # Connect to the database
    cursor = conn.cursor()

    # Fetch rows from Hashlists table where Cracked is 0 or 1
    # cursor.execute("SELECT * FROM Hashlists WHERE Status IN (0,1))
    cursor.execute("SELECT * FROM Hashlists WHERE Cracked IN (0,1) AND HashlistId = 162")
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
            hashes = data.get('hashes', [])
            print(hashes)
            plaintext_hashes = []

            for hash_data in hashes:
                if hash_data.get('isCracked', False):
                    plaintext_hashes.append(hash_data.get('hash', ''))

            print("Plaintext Hashes:", plaintext_hashes)

            # if cracked > cracked_db:
            if cracked >= cracked_db:
               print('here')
               # Create New file
               create_file(name_db, 'status', hashlist_id, hash)

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

if __name__ == "__main__":
    try:
        conn = db_utils.establish_connection()
        monitor_hashlists(conn)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        if 'conn' in locals():
            db_utils.close_connection(conn)


import subprocess
import os
import json
import requests
import sqlite3
import sys
sys.path.append('./utils')
from config_utils import load_config, load_token
import db_utils

def load_path_importfiles():
    config = load_config()
    return config['local_directory']

def load_headers():
    token = load_token()
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

def create_custom_name(hashmode_number, hash, date, index=None, subindex=None):
    # Create the custom name using hashmode_number, date, and the first 15 characters of the hash
    name = ""
    if index is not None:
        if subindex is None:
            name += f"{index}_"
        else:
            name += f"{index}."
    if subindex is not None:
        name += f"{subindex}_"
    name += f"{hashmode_number}_{date}_{hash[:15]}"
    return name

def load_files_and_make_api_call():
    config = load_config()
    # Load data from hashmode.json
    with open('2_import_attack/hashmode.json', 'r') as json_file:
        hashmode_data = json.load(json_file)

    # Iterate over files in the import_files folder
    import_folder = load_path_importfiles()
    for filename in os.listdir(import_folder):
        file_path = os.path.join(import_folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                # Initialize variables
                number = None
                hashes = []
                metadata_found = False
                metadata = ""
                date = None
                hashmode_number = None

                # Read content of the file
                for line in file:
                    line = line.strip()
                    if line:
                        if line.startswith("Metadata:"):
                            metadata_found = True
                        elif metadata_found:
                            metadata += line + "\n"
                        else:
                            hashes.append(line)
                # Extract number from metadata
                for line in metadata.strip().split("\n"):
                    key, value = line.split(":")
                    if key.strip() == "Hashmode":
                        hashmode_number = int(value.strip())
                    elif key.strip() == "Date":
                        date = value.strip()

                if hashmode_number is None:
                    print("Error: Hashmode not found in metadata.")
                    continue
                elif date is None:
                    print("Error: Date not found in metadata.")
                    continue

                if not hashes:
                    print("Error: No data found.")
                    continue

                # Join hashes into a single string if not combined
                if not config.get("multiple_hashlists_perfile", True):
                    hashes_str = '\n'.join(hashes)
                # Check if number exists in hashmode_data
                if str(hashmode_number) in hashmode_data:
                    tasks = hashmode_data[str(hashmode_number)]

                    if config.get("multiple_hashlists_perfile", True):
                        for i, hash in enumerate(hashes, start=1):
                            # Create a custom name for the hashlist
                            hashlist_name = create_custom_name(hashmode_number, hash, date, i)

                            # Make API call to create hashlist
                            hashlistId = create_hashlist(hashmode_number, hashlist_name, hash)

                            if hashlistId is not None:
                                # Make API call for each task
                                for j, task in enumerate(tasks, start=1):
                                    # Create a custom name for the task
                                    task_name = create_custom_name(hashmode_number, hash, date, i, j)
                                    # Make API call using task data
                                    create_task(task, task_name, hashlistId, hash)
                    else:
                        # Create a custom name for the hashlist
                        hashlist_name = create_custom_name(hashmode_number, hashes_str, date)

                        # Make API call to create hashlist
                        hashlistId = create_hashlist(hashmode_number, hashlist_name, hashes_str)

                        if hashlistId is not None:
                            # Make API call for each task
                            for j, task in enumerate(tasks, start=1):
                                # Create a custom name for the task
                                task_name = create_custom_name(hashmode_number, '', date, subindex=j)
                                # Make API call using task data
                                create_task(task, task_name, hashlistId, hashes_str)

                else:
                    print(f"No matching data found in hashmode.json for number {hashmode_number}")

def create_hashlist(hashmode, name, hash):
    config = load_config()
    headers = load_headers()
    # API endpoint
    if 'backend' in config and 'backend_url' in config['backend']:
        backend_url = config['backend']['backend_url']
    else:
        backend_url = ''  # Or any default value you prefer

    url = backend_url + '/ui/hashlists'
    # Data for the API call
    data = {
        "name": name,
        "hashTypeId": hashmode,
        "format": 2,
        "separator": ";",
        "isSalted": False,
        "isHexSalt": False,
        "accessGroupId": 1,
        "useBrain": False,
        "brainFeatures": 3,
        "notes": "",
        "sourceType": "paste",
        "sourceData": hash,
        "hashCount": 0,
        "isArchived": False,
        "isSecret": True
    }
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)
    # Check if the API call was successful
    if response.status_code == 201:
        # Extract hashlistId from the response JSON
        print("Created Hashlist Sucessful:", response.json())
        response_data = response.json()
        hashlistId = response_data.get('_id')
        # Save data to the database
        save_to_database(name, hashlistId, hash, hashmode)
        return hashlistId
    elif response.status_code == 401:
        # Handle 401 Unauthorized status code
        # Run token manager script
        subprocess.run(["python", "token/token_manager.py"])
        # Re-run monitor_hashlists after token_manager completes
        create_hashlist()
    else:
        print(f"Failed to create hashlist. Status code: {response.status_code}, Reason: {response.reason}")
        return None

def create_task(task, name, hashlistId, hash):
    config = load_config()
    headers = load_headers()
    # API endpoint
    if 'backend' in config and 'backend_url' in config['backend']:
        backend_url = config['backend']['backend_url']
    else:
        backend_url = ''  # Or any default value you prefer

    url = backend_url + '/ui/tasks'
    # Data for the API call
    data = {
        "taskName": name,
        "notes": task["notes"],
        "hashlistId": hashlistId,
        "attackCmd": task["attackCmd"],
        "priority": task["priority"],
        "maxAgents": task["maxAgents"],
        "chunkTime": task["chunkTime"],
        "statusTimer": task["statusTimer"],
        "color": task["color"],
        "isCpuTask": task["isCpuTask"],
        "skipKeyspace": task["skipKeyspace"],
        "crackerBinaryId": task["crackerBinaryId"],
        "crackerBinaryTypeId": task["crackerBinaryTypeId"],
        "isArchived": task["isArchived"],
        "staticChunks": task["staticChunks"],
        "chunkSize": task["chunkSize"],
        "forcePipe": task["forcePipe"],
        "preprocessorId": task["preprocessorId"],
        "preprocessorCommand": task["preprocessorCommand"],
        "isSmall": task["isSmall"],
        "useNewBench": task["useNewBench"],
        "files": task["files"]
    }
    #print("Request Data:")
    #print(json.dumps(data, indent=2))
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)
    # Check if the API call was successful
    if response.status_code == 201:
        print("Created Task Sucessful:", response.json())
    else:
        print(f"API call failed. Status code: {response.status_code}, Reason: {response.reason}")

def save_to_database(name, hashlistId, hash, hashmode):
    try:
        cursor = conn.cursor()
        # Create a table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS Hashlists
                          (Name TEXT, HashlistId TEXT, Hash TEXT, Hashmode INTEGER, Cracked INTEGER)''')
        # Insert data into the table
        # Cracked value 0 = No cracked, 1 = Partially cracked, 2 = Fully cracked
        cursor.execute("INSERT INTO Hashlists VALUES (?, ?, ?, ?, ?)", (name, hashlistId, hash, hashmode, 0))
        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Data saved to the database.")
    except sqlite3.Error as e:
        print("SQLite error:", e)

if __name__ == "__main__":
    try:
        conn = db_utils.establish_connection()
        load_files_and_make_api_call()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        if 'conn' in locals():
            db_utils.close_connection(conn)


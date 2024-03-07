import os
import json
import requests

def load_config():
    with open('../token/config.json') as f:
        return json.load(f)

def load_token():
    with open('../token/token.json') as f:
        token_data = json.load(f)
        return token_data.get('token')

def load_headers():
    token = load_token()
    return {"Authorization": f"Bearer {token}"}

def create_custom_name(hashmode_number, string, date, index=None):
    # Create the custom name using hashmode_number, date, and the first 10 characters of the string
    name = f"{hashmode_number}_{date}_{string[:10]}"
    if index is not None:
        name += f"_{index}"
    return name

def load_files_and_make_api_call():
    # Load data from hashmode.json
    with open('hashmode.json', 'r') as json_file:
        hashmode_data = json.load(json_file)

    # Iterate over files in the import_files folder
    import_folder = "import_files"
    for filename in os.listdir(import_folder):
        file_path = os.path.join(import_folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                # Read content of the file
                content = file.read().strip()

                # Extract number and string from content
                number, string = None, None
                metadata_found = False
                metadata = ""
                for line in content.split("\n"):
                    if line.startswith("Metadata:"):
                        metadata_found = True
                    elif metadata_found:
                        metadata += line + "\n"
                    else:
                        number, string = line.split(' ', 1)

                # Extract number from metadata
                hashmode_number = None
                for line in metadata.strip().split("\n"):
                    key, value = line.split(":")
                    if key.strip() == "Hashmode":
                        hashmode_number = int(value.strip())
                        break

                if hashmode_number is None:
                    print("Error: Hashmode not found in metadata.")
                    continue

                # Check if number exists in hashmode_data
                if str(hashmode_number) in hashmode_data:
                    tasks = hashmode_data[str(hashmode_number)]

                    # Create a custom name
                    hashlist_name = create_custom_name(hashmode_number, string, date)

                    # Make API call to create hashlist
                    hashlistId = create_hashlist(hashmode_number, hashlist_name, string)

                    if hashlistId is not None:
                        # Make API call for each task
                        task_name = create_custom_name(hashmode_number, string, date, i)
                        for i, task in enumerate(tasks, start=1):
                            # Make API call using task data
                            create_task(task, task_name, hashlistId, string)
                else:
                    print(f"No matching data found in hashmode.json for number {hashmode_number}")

def create_hashlist(hashmode, name, string):
    config = load_config()
    headers = load_headers()
    # API endpoint
    url = config.get('backend_url') + '/hashlists'
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
        "sourceType": "import",
        "sourceData": string,
        "hashCount": 0,
        "isArchived": False,
        "isSecret": True
    }
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)
    # Check if the API call was successful
    if response.status_code == 201:
        # Extract hashlistId from the response JSON
        response_data = response.json()
        hashlistId = response_data.get('id')
        return hashlistId
    else:
        print(f"Failed to create hashlist. Status code: {response.status_code}, Reason: {response.reason}")
        return None

def create_task(task, name, hashlistId, string):
    config = load_config()
    headers = load_headers()
    # API endpoint
    url = config.get('backend_url') + '/tasks'
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
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)
    # Check if the API call was successful
    if response.status_code == 201:
        print("API call successful:", response.json())
    else:
        print(f"API call failed. Status code: {response.status_code}, Reason: {response.reason}")

if __name__ == "__main__":
    load_files_and_make_api_call()

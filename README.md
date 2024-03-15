# SFTP Hashtopolis Automation

This basic tool uses Hashtopolis API V2 to streamline the creation of hashlists and attacks (tasks) by simply dropping hashes into a designated remote folder.

## Usage Examples

### 1: Automated Hashlist Creation

1. **Drop Hashes into Remote Directory**: Place a text file containing hashes in the designated remote directory (`remote_directory_get`). The tool will automatically detect and process the file.

2. **Automatic Hashlist Creation**: Upon detecting the file, the tool will read the hashes and generate a corresponding hashlist in Hashtopolis using the provided configuration settings.

3. **Task Generation**: After creating the hashlist, the tool will analyze the hashmode and initiate the appropriate attack(tasks) according to the predefined templates in the `hashmode.json` configuration file.

### 2: Attack Task Execution

1. **Hashlist Cracking**: Once the attack(tasks) are created, Hashtopolis will begin cracking the hashes using the specified attack methods and resources.

2. **Status Monitoring**: The tool continuously monitors the status of the hashlists, waiting for any crack.

3. **Email Notifications (Optional)**: If configured, the tool can send email notifications at specified intervals to update users on the progress and status of the cracking operations.

### 3: Post-Cracking Actions

1. **Result Reporting**: Upon successful cracking of hashes, the tool generates a report containing the cracked passwords and other relevant information.

2. **File Generation**: The tool creates a text file with the cracked passwords and places it in the designated remote directory (`remote_directory_post`).

3. **Additional Processing**: Users can further process the cracked passwords file as needed for additional analysis or actions.

# Automatic Setup and Running

This project provides a convenient way to automatically install dependencies and start the application using the `__init__.py` file. By running this file, users can quickly set up the environment and launch the application without manually installing dependencies.

The application can be installed in any machine, as soon as the machine has access to Hashtopolis(offline servers). **Important**: Please refer to the Hashtopolis documentation for instructions on how to enabling the API v2.

## Installation and Setup

To use the automatic setup and running feature, follow these steps:

1. **Clone the Repository**: First, clone the project repository to your local machine using the following command:

    ```bash
    git clone https://github.com/xbenyx/h2p_automation.git
    ```

2. **Navigate to the Project Directory**: Change into the project directory using the `cd` command:

    ```bash
    cd h2p_automation
    ```
3. **Config file**: Change the settings in the config file and place t

The correct configuration is crucial for the proper functioning of this automation tool. Below is an example of a configuration file (`config.json`) with explanations for each key:

```json
{
    "backend": {
        "username": "admin",
        "password": "hashtopolis",
        "backend_url": "https://localhost:8080/api/v2"
    },
    "sftp": {
        "hostname": "Target_IP",
        "port": 22,
        "username": "username",
        "password": "password",
        "remote_directory_get": "/home/....",
        "remote_directory_post": "/home/...."
    },
    "local_directory": "/home/....",
    "multiple_hashlists_perfile": false,
    "sftp_interval": 25,
    "smtp_enable": false,
    "smtp_interval": 25,
    "smtp": {
        "sender_email": "your_sender_email@example.com",
        "receiver_email": "receiver_email@example.com",
        "smtp_server": "smtp....",
        "smtp_port": 587,
        "smtp_username": "username",
        "smtp_password": "password"
    }
}
```

Here's the explanation of the keys and subkeys in the provided JSON configuration:

- **backend**: Configuration details for the backend server.
  - *username*: Username for authentication.
  - *password*: Password for authentication.
  - *backend_url*: URL of the backend server.

- **sftp**: Configuration details for the SFTP server.
  - *hostname*: Hostname or IP address of the SFTP server.
  - *port*: Port number for the SFTP connection.
  - *username*: Username for SFTP authentication.
  - *password*: Password for SFTP authentication.
  - *remote_directory_get*: Remote directory path for fetching files.
  - *remote_directory_post*: Remote directory path for posting files.

- **local_directory**: Local directory path for file operations.

- **multiple_hashlists_perfile**: Boolean indicating whether multiple hashlists are allowed per file. If true, each file will create one hashlist for each hash.

- **sftp_interval**: Interval in seconds for SFTP operations.

- **smtp_enable**: Boolean indicating whether SMTP email notifications are enabled.

- **smtp_interval**: Interval in seconds for SMTP operations. This determines the time interval for checking changes and sending reports.

- **smtp**: Configuration details for SMTP email.
  - *sender_email*: Email address of the sender for outgoing emails.
  - *receiver_email*: Email address of the receiver for incoming emails.
  - *smtp_server*: SMTP server address for sending emails.
  - *smtp_port*: Port number for the SMTP server.
  - *smtp_username*: Username for SMTP authentication.
  - *smtp_password*: Password for SMTP authentication.

Ensure that you provide accurate values for each key in the configuration file to avoid errors and ensure smooth operation of the project.

**Important**: The SFTP permissions should be configured to allow read access to `remote_directory_get` for read and delete files, and write access to `remote_directory_post` for creating files.

Here's how you might set permissions for `remote_directory_get` and `remote_directory_post`:

```bash
# Linux system
chmod +rd remote_directory_get && chmod +w remote_directory_post

# Windows system
icacls remote_directory_get /grant Everyone:(R,D) && icacls remote_directory_post /grant Everyone:(W)

# Mac System
chmod +rd remote_directory_get && chmod +w remote_directory_post
```
These commands ensure that the SFTP user has the necessary permissions to perform read and delete operations in `remote_directory_get` and write operations in `remote_directory_post`. Adjust permissions according to your specific setup and security requirements.

4. **Config Hashmode**: Task templates need to be added to match your the hashmode from the hashes in the text file. Go to the location 2_import_attack and configure the hashmode.json. You can add multiple task templates for each hashmode. ie. The app will read the file and create a hashlist, then read the hashmode.json and create 1, 2 or x tasks.

5. **Run the `__init__.py` File**: Execute the `__init__.py` file to automatically install dependencies and start the application. Use the following command:

    ```bash
    python __init__.py
    ```

This command will trigger the setup process, which includes installing dependencies specified in the `requirements.txt` file and starting the application.

## Usage

Once the setup process is complete, the application will be launched automatically.

Just place the files in the remote_directory_get, the app will download the files. Once is a crack it will create a file with the hashes in remote_directory_post.

- **remote_directory_get**: The file needs to be in .txt format and contain the below structure, for example:

  ```plaintext
  7e866b1d0a354f31d62b6055a8742473ee71bfb5
  1459794da58333d4a2a949f84b882f92e957a356
  dfd2ed72dd10d7bcf42f6ce4625266d78575010c

  Metadata:
  Date: 2024-07-06
  Hashmode: 100
  ```

- **remote_directory_post**: The file will be created with the extension .txt and structure as below, for example:

  ```plaintext
  hash1
  hash2
  hash3

  Metadata:
  Name: name
  Status: status
  Hashmode: hashlistid
  ```

See additional notes to understand naming.

## Additional Notes

- **Dependencies**: The `__init__.py` file utilizes `pip` to install project dependencies listed in the `requirements.txt` file. Make sure to keep this file up to date with any new dependencies required by the project.

- **Folder Structure**: Below is the folder structure.

```
h2p_automation/
│
├── 1_monitoring_sftp/
├── 2_import_attack/
├── 3_reporting/
├── database/
├── import_files/
├── logs/
├── token/
├── util/
│
└── __init__.py
```

- **`1_monitoring_sftp/`**: Contains scripts and resources for monitoring SFTP activity.

- **`2_import_attack/`**: Dedicated to importing attack-related data and resources.

- **`3_reporting/`**: Holds scripts and tools for generating reports based on collected data.

- **`database/`**: Stores the project's database files and related scripts.

- **`import_files/`**: Contains files and data to be imported or processed by the application.

- **`logs/`**: Stores log files generated by the application.

- **`token/`**: Holds resources related to authentication and authorization.

- **`util/`**: Contains utility scripts and modules used across the application.

- **`__init__.py`**: Marks the directory as a Python package and may contain initialization code.

This provides a visual representation of the project's folder structure along with an explanation of each directory's purpose.

- **Error Handling**: In case of any errors during the setup or application launch process, error messages will be displayed in the terminal, and some errors stored in the logs folder.

**Naming Convention:**

- **Hashlist Naming Format**:
  - Each hashlist follows the format: `{Hashmode}_{File_Date}_{First_15chars_Hash}`.
    - `{Hashmode}`: The identifier for the hash algorithm used.
    - `{File_Date}`: The date in the file metadata.
    - `{First_15chars_Hash}`: The first 15 characters of the hash value.

- **Task Naming Format**:
  - Each task follows the format: `{Index}_{Hashmode}_{File_Date}_{First_15chars_Hash}`.
    - `{Index}`: An optional index indicating the sequence of the hash within the file, if applicable.
    - `{Hashmode}`: The identifier for the hash algorithm used.
    - `{File_Date}`: The date when the file was processed.
    - `{First_15chars_Hash}`: The first 15 characters of the hash value.

**Example:**

Suppose we have a hashlist generated from a file containing Sha1 hashes, processed on July 6, 2024.

- **Hashlist Name**:
  - Hashmode: 100
  - File Date: 2024-07-06
  - First 15 Characters of Hash: `b89eaac7e61417341b710b727768294d0e6a277b`
  - **Hashlist Name**: `100_2024-07-06_b89eaac7e614173`

Now, let's consider a task created for this hashlist:

- **Task Name**:
  - Index: 1 (assuming it's the first hash in the file)
  - Hashmode: 100
  - File Date: 2024-07-06
  - First 15 Characters of Hash: `b89eaac7e61417341b710b727768294d0e6a277b`
  - **Task Name**: `1_100_2024-07-06_b89eaac7e614173`

The naming convention tries to help identify what hashlists and tasks are being processed using this tool and give an easy hint.

## On Development

Currently SMTP is still on development, it works but a logic needs to be implement once a hashlist is cracked/

## Contributing

Hey there! 👋 We're thrilled that you're considering contributing to our project! Here are a few guidelines to help you get started:

### How Can I Contribute?

1. **Report Bugs**: If you come across any bugs or issues while using our project, please report them. Be sure to include detailed information about the problem and steps to reproduce it.

2. **Submit Feature Requests**: Have a great idea for a new feature or improvement? Let us know by opening an issue. We'd love to hear your suggestions and feedback!

3. **Contribute Code**: We welcome contributions of all sizes, from small bug fixes to major feature enhancements. Fork our repository, make your changes, and submit a pull request.

4. **Spread the Word**: Enjoying our project? Help us spread the word by sharing it with your friends and colleagues. You can also star our repository on GitHub to show your support!

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE.md](LICENSE.md) file for details.

The MIT License is a permissive open-source license that allows for unrestricted use, modification, distribution, and sublicensing of the software. It is suitable for collaborative projects and encourages contributions from the community.
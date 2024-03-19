import os
import time
import paramiko
import json
import subprocess
import logging
import logging.handlers

class SftpMonitor:
    def __init__(self):
        self.imported_files = set()  # Set to keep track of imported files
        self.setup_logging()

    def setup_logging(self):
        # Create a logger
        self.logger = logging.getLogger("SftpMonitor")
        self.logger.setLevel(logging.DEBUG)

        # Create a rotating file handler for logs with maximum size 1MB and keep backup count as 1
        log_file = os.path.join(os.getcwd(), "logs/sftp_monitor_logs.txt")
        file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=1)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)

    def main(self):
        if not os.path.exists('config.json'):
            # Create config.json with default settings
            default_config = {
                "sftp": {
                    "hostname": "localhost",
                    "port": 22,
                    "username": "user",
                    "password": "pass",
                    "remote_directory_get": "/home/..full_path",
                    "remote_directory_post":  "/home/..full_path",
                },
                "local_directory": "/home/..full_path",
                "sftp_interval": 25
            }
            with open('config.json', 'w') as f:
                json.dump(default_config, f, indent=4)
            print("Settings need to be added to config.json. Please update the configuration.")

        # Load configuration from JSON file
        with open('config.json') as f:
            config = json.load(f)

        sftp_config = config['sftp']
        local_dir = config['local_directory']
        sftp_interval = config['sftp_interval']
        while True:
            self.logger.info("Checking for new files...")
            time.sleep(sftp_interval)  # Sleep for sftp_interval seconds

            try:
                # Connect to SFTP server
                self.logger.info("Connecting to SFTP server...")
                sftp = self.connect_to_sftp(sftp_config)
                self.logger.info("Connected to SFTP server")

                # Retrieve the list of files from the remote directory
                self.logger.info("Contents of remote directory:")
                remote_files = sftp.listdir(sftp_config['remote_directory_get'])
                self.logger.info(remote_files)

                # Check for new files in the local directory
                files = self.check_for_new_files(local_dir)
                self.logger.info(f"Found {len(files)} files in local directory")

                # Iterate over each file in the remote directory
                for file in remote_files:
                    if file not in self.imported_files:  # Check if file has not been imported yet
                        remote_path = sftp_config['remote_directory_get'] + "/" + file
                        local_path = os.path.join(local_dir, file)
                        self.logger.info(f"Downloading file: {file}")

                        # Download the file from the SFTP server to the local directory
                        self.download_file(sftp, remote_path, local_path)
                        self.logger.info(f"Downloaded file: {file}")

                        # Add file to imported files set
                        self.imported_files.add(file)

                        # Delete the file from the remote directory
                        try:
                            sftp.remove(remote_path)
                            self.logger.info(f"Deleted file: {file} from remote directory")
                        except Exception as e:
                            self.logger.error(f"Error deleting file: {file} from remote directory - {e}")

                # Close SFTP connection
                sftp.close()
                self.logger.info("Disconnected from SFTP server")

                # Call the attack.py script after all new files have been processed
                if files:
                    subprocess.run(["python", "2_import_attack/attack.py"])
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")

    def connect_to_sftp(self, sftp_config):
        transport = paramiko.Transport((sftp_config['hostname'], sftp_config['port']))
        transport.connect(username=sftp_config['username'], password=sftp_config['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp

    def download_file(self, sftp, remote_path, local_path):
        # Download the file from the SFTP server to the local directory
        sftp.get(remote_path, local_path)

    def check_for_new_files(self, local_dir):
        files = os.listdir(local_dir)
        return files

if __name__ == '__main__':
    sftp_monitor = SftpMonitor()
    sftp_monitor.main()

import os
import subprocess
import sqlite3
from utils.config_utils import load_config
from utils import db_utils

def install_dependencies():
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        raise FileNotFoundError("requirements.txt not found")

    # Install dependencies if not already installed
    with open("requirements.txt", "r") as f:
        dependencies = f.read().splitlines()

def create_database():
    # Create a new SQLite database file
    database_file = os.path.join("database", "report.db")
    try:
        conn = sqlite3.connect(database_file)
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to create database: {e}")

def install_database():
    # Create database folder if it doesn't exist
    if not os.path.exists("database"):
        os.makedirs("database")

    # Check if the database file exists
    database_file = os.path.join("database", "report.db")
    if not os.path.exists(database_file):
        # If the database file doesn't exist, create a new one
        create_database()

# Call the install_database function during initialization
install_database()

def establish_connection():
    return sqlite3.connect('database/report.db')

def start_token_manager():
    # Start token manager script
    try:
        subprocess.check_call(["python", "token/token_manager.py"])
    except subprocess.CalledProcessError as e:
        raise Exception("Failed to start token manager") from e

def start_sftp_monitor():
    # Start SFTP monitor script
    try:
        subprocess.check_call(["python", "1_monitoring_sftp/sftp_monitor.py"])
    except subprocess.CalledProcessError as e:
        raise Exception("Failed to start SFTP monitor") from e

def start_monitor():
    # Start monitor script
    try:
        subprocess.check_call(["python", "3_reporting/monitor.py"])
    except subprocess.CalledProcessError as e:
        raise Exception("Failed to start monitoring") from e

def start_smtp_monitor():
    # Start SMTP monitor script
    try:
        subprocess.check_call(["python", "3_reporting/email_monitor.py"])
    except subprocess.CalledProcessError as e:
        raise Exception("Failed to start SMTP monitor") from e

def test_attack():
    # Testin attack
    try:
        subprocess.check_call(["python", "2_import_attack/attack.py"])
    except subprocess.CalledProcessError as e:
        raise Exception("Failed to start SMTP monitor") from e

if __name__ == "__main__":
    try:
        install_dependencies()
        install_database()
        #start_token_manager()
        #start_sftp_monitor()
        config = load_config()  # Load configuration

        if config.get('smtp', {}).get('smtp_enable', False):
            start_smtp_monitor()  # Start SMTP monitor if smtp_enable is True

        # Other tasks
        #test_attack()
        start_monitor()
    except Exception as e:
        print("An error occurred:", e)




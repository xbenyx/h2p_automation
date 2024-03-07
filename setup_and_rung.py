import os
import sys
import subprocess

def check_dependencies():
    # Read required packages from requirements.txt
    with open("requirements.txt") as f:
        required_packages = [line.strip() for line in f]

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_service_status(service_name):
    # Check if the service is installed
    try:
        subprocess.check_output(["sc", "query", service_name])
        return True
    except subprocess.CalledProcessError:
        return False

def start_service(service_script):
    print(f"Starting service: {service_script}...")
    subprocess.check_call(["python", service_script, "start"])

def stop_service(service_name):
    print(f"Stopping service: {service_name}...")
    subprocess.check_call(["sc", "stop", service_name])

def uninstall_service(service_name):
    print(f"Uninstalling service: {service_name}...")
    subprocess.check_call(["sc", "delete", service_name])

if __name__ == "__main__":
    check_dependencies()

    # Uninstall SFTP monitoring service
    sftp_service_name = "SftpMonitorService"
    if check_service_status(sftp_service_name):
        stop_service(sftp_service_name)
        uninstall_service(sftp_service_name)
    else:
        print("SFTP monitoring service is not installed.")

    # Uninstall token manager service
    token_manager_service_name = "TokenManagerService"
    if check_service_status(token_manager_service_name):
        stop_service(token_manager_service_name)
        uninstall_service(token_manager_service_name)
    else:
        print("Token manager service is not installed.")

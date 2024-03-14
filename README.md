# SFTP Hashtopolis Attack

Project description goes here.

# Automatic Setup and Running

This project provides a convenient way to automatically install dependencies and start the application using the `__init__.py` file. By running this file, users can quickly set up the environment and launch the application without manually installing dependencies.

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
        "remote_directory": "/home/...."
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

- **backend**: Configuration details for the backend server. Includes username, password, and URL.
- **sftp**: Configuration details for the SFTP server. Includes hostname, port, username, password, and remote directory.
- **local_directory**: Local directory path for file operations.
- **multiple_hashlists_perfile**: Boolean indicating whether multiple hashlists are allowed per file. i.e if its true it will read each file and create one hashlist for each hash
- **sftp_interval**: Interval in seconds for SFTP operations.
- **smtp_enable**: Boolean indicating whether SMTP email notifications are enabled.
- **smtp_interval**: Interval in seconds for SMTP operations. The time for check changes and report back.
- **smtp**: Configuration details for SMTP email. Includes sender email, receiver email, SMTP server details, username, and password.

Ensure that you provide accurate values for each key in the configuration file to avoid errors and ensure smooth operation of the project.

4. **Run the `__init__.py` File**: Execute the `__init__.py` file to automatically install dependencies and start the application. Use the following command:

    ```bash
    python __init__.py
    ```

This command will trigger the setup process, which includes installing dependencies specified in the `requirements.txt` file and starting the application.

## Usage

Once the setup process is complete, the application will be launched automatically. You can now interact with the application as usual.

## Additional Notes

- **Dependencies**: The `__init__.py` file utilizes `pip` to install project dependencies listed in the `requirements.txt` file. Make sure to keep this file up to date with any new dependencies required by the project.

- **Customization**: If you need to customize the setup process or the application launch behavior, you can modify the `__init__.py` file accordingly. You can add additional setup steps or change the way the application is launched based on your specific requirements.

- **Error Handling**: In case of any errors during the setup or application launch process, error messages will be displayed in the terminal. Make sure to review these messages for troubleshooting purposes.

## Contributing

Hey there! 👋 We're thrilled that you're considering contributing to our project! Here are a few guidelines to help you get started:

### How Can I Contribute?

1. **Report Bugs**: If you come across any bugs or issues while using our project, please report them on our [Issue Tracker](link-to-issue-tracker). Be sure to include detailed information about the problem and steps to reproduce it.

2. **Submit Feature Requests**: Have a great idea for a new feature or improvement? Let us know by opening an issue. We'd love to hear your suggestions and feedback!

3. **Contribute Code**: We welcome contributions of all sizes, from small bug fixes to major feature enhancements. Fork our repository, make your changes, and submit a pull request.

4. **Spread the Word**: Enjoying our project? Help us spread the word by sharing it with your friends and colleagues. You can also star our repository on GitHub to show your support!

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE.md](LICENSE.md) file for details.

The MIT License is a permissive open-source license that allows for unrestricted use, modification, distribution, and sublicensing of the software. It is suitable for collaborative projects and encourages contributions from the community.
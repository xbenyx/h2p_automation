import subprocess
import sqlite3
import requests
import json
import smtplib
import sys
sys.path.append('./utils')
from config_utils import load_config, load_token
import db_utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configparser import ConfigParser

def read_html_template(file_path, message):
    with open(file_path, 'r') as file:
        html_content = file.read()
        html_content = html_content.replace("{message}", message)
        return html_content

def send_email(subject, message):
    config = load_config()
    smtp_config = config.get('smtp')
    sender_email = smtp_config.get('sender_email')
    receiver_email = smtp_config.get('receiver_email')
    smtp_server = smtp_config.get('smtp_server')
    smtp_port = smtp_config.get('smtp_port')
    smtp_username = smtp_config.get('smtp_username')
    smtp_password = smtp_config.get('smtp_password')

    html_content = read_html_template('3_reporting/email_template.html', message)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)
    finally:
        server.quit()

# Function to monitor cracked hashlists
def monitor_hashlists(conn):
    config = load_config()
    token = load_token()
    # Connect to the database
    cursor = conn.cursor()

    # Fetch rows from Hashlists table where Cracked is 0 or 1
    cursor.execute("SELECT * FROM Hashlists WHERE HashlistId > 1")
    rows = cursor.fetchall()

    # Iterate over the rows and make API calls
    for row in rows:
        hashlist_id = row[1]  # Assuming hashlist_id is at index 1, adjust accordingly
        url = config['backend']['backend_url'] + f'/ui/hashlists/{hashlist_id}'
        headers = {'Authorization': f'Bearer {load_token()}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            cracked = data.get('cracked')
            send_email("Hashlist Cracked", f"Hashlist with ID {hashlist_id} has been cracked.")
            if cracked == 1:
                # Send email notification
                send_email("Hashlist Cracked", f"Hashlist with ID {hashlist_id} has been cracked.")
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


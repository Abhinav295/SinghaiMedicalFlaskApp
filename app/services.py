import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


def validate_contact_number(contact_number):
    """
    Validate the contact number to ensure it is exactly 10 digits.

    :param contact_number: The contact number to validate.
    :return: True if valid, False otherwise.
    """
    if contact_number.isdigit() and len(contact_number) == 10:
        return True
    return False

def prepare_body(data):
    """
    Prepare the body of the email with the contact information.

    :param data: Dictionary containing contact information.
    :return: Formatted string for the email body.
    """
    body = f"""
    New contact query received:

    Name: {data['First Name']} {data['Last Name']}
    Contact Number: {data['Contact Number']}
    Gender: {data['Gender']}
    Query: {data['Query']}

    """
    return body

def save_contact_to_csv(data, filename="contacts.csv"):
    """
    Save contact information to a CSV file.

    :param data: Dictionary containing contact information.
    :param filename: Name of the CSV file.
    """

    if not validate_contact_number(data["Contact Number"]):
        print("Invalid contact number. It must be exactly 10 digits.")
        return

    # Define the file path
    file_path = os.path.join(os.getcwd(),"mysite", "app", "static", "data", filename)

    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # Open the file in append mode
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["First Name", "Last Name", "Contact Number", "Gender", "Query"])

        # Write the header if the file is new
        if not file_exists:
            writer.writeheader()

        # Write the contact data
        writer.writerow(data)
        print("data is written to the file successfully.")
        send_email(subject="New Contact Query Received",body=prepare_body(data),to_email="jainajain32@gmail.com")

def send_email(subject, body, to_email):
    """
    Send an email with the specified subject and body to the given email address.

    :param subject: Subject of the email.
    :param body: Body of the email.
    :param to_email: Recipient's email address.
    """
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "abhinavjain295@gmail.com"  # Replace with your email
    sender_password = "xrcl zqzd wlsa bvzv"      # Replace with your email password
    recipient_email = to_email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def login_check(username, password):
    """
    Check if the provided username and password match the stored credentials.

    :param username: Username to check.
    :param password: Password to check.
    :return: True if credentials are valid, False otherwise.
    """
    # For simplicity, using hardcoded credentials. In a real application, use a secure method to store and verify credentials.
    file_path = os.path.join(os.getcwd(),"mysite", "app", "static", "data", "login.json")

    with open(file_path, 'r') as file:
        users = json.load(file)

    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False


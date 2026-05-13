from flask import Blueprint, render_template, request, session
from app.services import save_contact_to_csv
from app.services import login_check
import json
import urllib.parse

main = Blueprint('main', __name__)

@main.route('/')
def home():
    whatsapp_number = "917869582580"

    # A pre-filled message to save the customer time
    raw_message = "Hello Singhai Medical Store, I want to inquire about a medicine."

    # URL encode the message so it passes safely through the web link
    whatsapp_message = urllib.parse.quote(raw_message)

    if not session:
        return render_template('index.html', message=None, message_type=None,wa_number=whatsapp_number,
                           wa_message=whatsapp_message)
    else :
        return render_template('index.html', message=None, message_type=None,username='admin',wa_number=whatsapp_number,
                           wa_message=whatsapp_message)

@main.route('/about')
def about():
    return render_template('about.html', message=None, message_type=None)

@main.route('/products')
def products():
    with open('./app/static/data/products.json', 'r') as file:
        products = json.load(file)
    if not products:
        message = "No products available at the moment."
        return render_template('products.html', message=message, message_type="warning")
    return render_template('products.html', products=products)

def validate_contact_number(contact_number):
    """
    Validate the contact number to ensure it is exactly 10 digits.

    :param contact_number: The contact number to validate.
    :return: True if valid, False otherwise.
    """
    return contact_number.isdigit() and len(contact_number) == 10

@main.route('/submit-query', methods=['POST'])
def submit_query():
    # Get form data
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    gender = request.form.get('gender')
    query = request.form.get('query')

    # Validate the contact number
    if not validate_contact_number(contact_number):
        message = "Invalid contact number. It must be exactly 10 digits."
        return render_template('index.html', message=message, message_type="danger")

    # Save contact information to CSV
    contact_data = {
        "First Name": first_name,
        "Last Name": last_name,
        "Contact Number": contact_number,
        "Gender": gender,
        "Query": query
    }
    save_contact_to_csv(contact_data)

    # Success message
    message = "Your query has been submitted successfully!"
    return render_template('index.html', message=message, message_type="success")

@main.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check login credentials
    if login_check(username, password):
        message = "Login successful!"
        session['username'] = username
        return render_template('index.html', message=message, message_type="success", username=username)
    else:
        message = "Invalid username or password."
        return render_template('index.html', message=message, message_type="danger")

@main.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html', message=None, message_type=None)

@main.route('/removeProducts',methods=['POST'])
def removeProducts():
    header = request.form.get("dheaders")
    description = request.form.get("ddescriptions")
    with open('./app/static/data/products.json', 'r') as file:
        products = json.load(file)
        for entry in products:
            if entry["heading"] == header :
                entry["items"] = [item for item in entry["items"] if item.get("description") != description]
                break;
        json.dumps(products, indent=4)
    if not products:
        message = "No products available at the moment."
        return render_template('products.html', message=message, message_type="warning")
    return render_template('products.html', products=products)

@main.route('/addProducts', methods=['POST'])
def addProducts():
    header = request.form.get("headers")

    new_item = {
    "imageUrl": request.form.get("img-url"),
    "description": request.form.get("desc"),
    "price": request.form.get("MRP")
    }

    try:
        with open('./app/static/data/products.json', 'r+') as file:
            products = json.load(file)

            for entry in products:
                if entry["heading"] == header:
                    new_item["id"] = len(entry["items"]) + 1
                    entry["items"].append(new_item)
                    break
            file.seek(0)
            json.dump(products, file, indent=4)
            file.truncate()

        if not products:
            message = "No products available at the moment."
            return render_template('products.html', message=message, message_type="warning")

    except FileNotFoundError:
        print("File is Not available ")
    message = "Item added successfully!"
    return render_template('products.html', products=products,message=message,message_type="Success")






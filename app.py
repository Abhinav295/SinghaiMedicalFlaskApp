from app import create_app

app = create_app()
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a unique and secure key
app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files

if __name__ == '__main__':
    app.run(debug=True)
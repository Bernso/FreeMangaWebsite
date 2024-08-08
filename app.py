try:
    from flask import Flask, render_template, request, jsonify, session, send_file
    import os
    import re  
    import random
    import requests
    import json
    from dotenv import load_dotenv  
except ImportError as e:
    input(f"Error importing: {e}")


port = '1111'
debug = True
host = '127.0.0.1' # could be 127.0.0.1 or 0.0.0.0 or your ip


def sendToDiscord(message):
    load_dotenv()
    webhookURL = os.getenv("WEBHOOK_URL")
    data = {
        "content": message,
        "username": "Manga Website"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhookURL, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("Message sent to discord.")
    else:
        print(f"Message failed to send to discord. Status Code: {response.status_code}")

app = Flask(__name__)
currentPath = os.getcwd()

@app.route("/")
def welcomePage():
    return render_template('welcome.html')

@app.route("/home")
def homePage():
    return render_template('home.html')



if __name__ == '__main__':
    try:
        app.run(port=port, debug=debug, host=host)
    except Exception as e:
        input(f"Error running the app: {e}")
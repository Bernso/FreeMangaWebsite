try:
    from flask import Flask, render_template, request, jsonify, session, send_file, send_from_directory, abort
    import os
    import re  
    import random
    import requests
    import json
    from dotenv import load_dotenv  
except ImportError as e:
    input(f"Error importing: {e}")




port = '1111'       # any number you want (4 digits)
debug = True        # could be True or False
host = '127.0.0.1'  # could be 127.0.0.1 or 0.0.0.0 or your ip
app = Flask(__name__)
currentPath = os.getcwd()

MANGA_DIR = os.path.join(currentPath, 'manga')

# Load environment variables
load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")




# Function to send messages to Discord
def sendToDiscord(message):
    data = {
        "content": message,
        "username": "Manga Website"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("Message sent to discord.")
    else:
        print(f"Message failed to send to discord. Status Code: {response.status_code}")




# Function to get featured manga
def get_featured_manga():
    featured_manga = []

    # Iterate over each folder in the MANGA_DIR
    for manga_folder in os.listdir(MANGA_DIR):
        manga_path = os.path.join(MANGA_DIR, manga_folder)

        if os.path.isdir(manga_path):
            try:
                # Read the id, description, and cover image
                with open(os.path.join(manga_path, 'id.txt'), 'r') as f:
                    manga_id = f.read().strip()
                with open(os.path.join(manga_path, 'description.txt'), 'r') as f:
                    description = f.read().strip()

                # Truncate description to 50 characters if necessary
                if len(description) > 50:
                    description = description[:47] + '...'

                # Create a dictionary with the manga data
                manga_data = {
                    'id': manga_id,
                    'title': manga_folder,
                    'description': description
                }

                featured_manga.append(manga_data)
            except Exception as e:
                print(f"Error reading manga data from {manga_folder}: {e}")

    return featured_manga




# Route for the welcome page
@app.route("/")
def welcomePage():
    featured_manga = get_featured_manga()
    return render_template('welcome.html', featured_manga=featured_manga)




# Route for the home page
@app.route("/home")
def homePage():
    featured_manga = get_featured_manga()
    return render_template('home.html', featured_manga=featured_manga)




@app.route("/manga")
def manga_list():
    return render_template('manga.html')




@app.route("/search")
def search():
    return render_template("searchManga.html")




@app.route('/contact')
def contact():
    return render_template('contact.html')




# Route for manga detail page
@app.route("/manga/<int:manga_id>")
def manga_detail(manga_id):
    featured_manga = get_featured_manga()
    manga = next((m for m in featured_manga if m['id'] == str(manga_id)), None)
    if manga:
        return render_template('manga_detail.html', manga=manga)
    else:
        return "Manga not found", 404




@app.route('/manga/<manga_title>/chapter/<chapterName>')
def chapter_detail(manga_title, chapterName):
    chapter_dir = os.path.join(MANGA_DIR, manga_title, 'Chapters', chapterName)
    
    # List all images in the chapter directory
    try:
        images = [f for f in os.listdir(chapter_dir) if os.path.isfile(os.path.join(chapter_dir, f)) and re.match(r'.*\.(jpg|jpeg|gif)$', f, re.IGNORECASE)]
        return render_template('manhwaContent.html', images=images, manga_title=manga_title, chapterName=chapterName)
    except FileNotFoundError:
        return "Chapter not found", 404




@app.route('/images/<manga_title>/<chapterName>/<filename>')
def get_image(manga_title, chapterName, filename):
    image_dir = os.path.join(MANGA_DIR, manga_title, 'Chapters', chapterName)
    return send_from_directory(image_dir, filename)





# Route for serving cover images
@app.route("/cover/<manga_title>")
def serve_image(manga_title):
    possible_extensions = ['jpg', 'jpeg', 'gif']
    
    # Check for each extension if the file exists
    for ext in possible_extensions:
        image_path = os.path.join(MANGA_DIR, manga_title, f'cover_image.{ext}')
        if os.path.exists(image_path):
            return send_from_directory(os.path.join(MANGA_DIR, manga_title), f'cover_image.{ext}')
    
    return abort(404)




# Error handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e), 404




# Main entry point
if __name__ == '__main__':
    try:
        app.run(port=port, debug=debug, host=host)
    except Exception as e:
        print(f"Error running the app: {e}")
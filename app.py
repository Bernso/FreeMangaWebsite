try:
    from flask import Flask, render_template, request, jsonify, session, send_file, send_from_directory, abort, redirect, url_for
    import os
    import re  
    import random
    import requests
    import json
    from natsort import natsorted
    import logging
    import urllib.parse
    from replaceCode import replace_special_characters
    from dotenv import load_dotenv
    import urllib  
except ImportError as e:
    input(f"Error importing: {e}")





logging.basicConfig(level=logging.DEBUG)



port = '1111'       # any number you want (4 digits)
debug = True        # could be True or False
host = '127.0.0.1'  # could be 127.0.0.1 or 0.0.0.0 or your ip

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
currentPath = os.getcwd()
MANGA_DIR = os.path.join(currentPath, 'manga')




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


@app.route('/send_to_discord', methods=['POST'])
def send_to_discord():
    data = request.json
    
    email = data.get('email')
    subject = data.get('subject')
    body = data.get('body')
    
    if not (email and subject and body):
        return jsonify({"success": False, "error": "Missing data"}), 400
    
    # Create the message to be sent to Discord
    discord_message = {
        "content": f"**New Message from:** {email}\n\n**Subject:** {subject}\n\n**Message:**\n{body}"
    }
    
    # Send the message to the Discord webhook
    response = requests.post(WEBHOOK_URL, json=discord_message)
    
    if response.status_code == 204:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "error": "Failed to send message"}), 500


# Function to get featured manga
def get_featured_manga():
    featured_manga = []

    # Iterate over each folder in the MANGA_DIR
    for manga_folder in os.listdir(MANGA_DIR):
        manga_path = os.path.join(MANGA_DIR, manga_folder)

        if os.path.isdir(manga_path):
            try:
                # Read the id, description, and cover image
                with open(os.path.join(manga_path, 'id.txt'), 'r', encoding='utf-8') as f:
                    manga_id = f.read().strip()
                with open(os.path.join(manga_path, 'description.txt'), 'r', encoding='utf-8') as f:
                    description = f.read().strip()

                with open(os.path.join(manga_path, 'type.txt'), 'r', encoding='utf-8') as f:
                    manga_type = f.read().strip()
                    if manga_type.lower() == 'manga':
                        continue

                # Create a dictionary with the manga data
                manga_data = {
                    'id': manga_id,
                    'title': manga_folder,
                    'description': description,
                    'type': manga_type
                }

                featured_manga.append(manga_data)
            except Exception as e:
                print(f"Error reading manga data from {manga_folder}: {e}")

    return featured_manga



def get_featured_mangaTruncated():
    featured_manga = []

    # Iterate over each folder in the MANGA_DIR
    for manga_folder in os.listdir(MANGA_DIR):
        manga_path = os.path.join(MANGA_DIR, manga_folder)

        if os.path.isdir(manga_path):
            try:
                # Read the id, description, and cover image
                with open(os.path.join(manga_path, 'id.txt'), 'r', encoding='utf-8') as f:
                    manga_id = f.read().strip()

                with open(os.path.join(manga_path, 'description.txt'), 'r', encoding='utf-8') as f:
                    description = f.read().strip()

                with open(os.path.join(manga_path, 'type.txt'), 'r', encoding='utf-8') as f:
                    manga_type = f.read().strip()
                    if manga_type.lower() == 'manga':
                        continue


                if len(description) > 50:
                    description = description[:47] + '...'


                # Create a dictionary with the manga data
                manga_data = {
                    'id': manga_id,
                    'title': manga_folder,
                    'description': description,
                    'type': manga_type
                }

                featured_manga.append(manga_data)
            except Exception as e:
                print(f"Error reading manga data from {manga_folder}: {e}")

    return featured_manga

def get_featured_mangaTruncatedTitle():
    featured_manga = []

    # Iterate over each folder in the MANGA_DIR
    for manga_folder in os.listdir(MANGA_DIR):
        manga_path = os.path.join(MANGA_DIR, manga_folder)

        if os.path.isdir(manga_path):
            try:
                # Read the id, description, and cover image
                with open(os.path.join(manga_path, 'id.txt'), 'r', encoding='utf-8') as f:
                    manga_id = f.read().strip()

                with open(os.path.join(manga_path, 'description.txt'), 'r', encoding='utf-8') as f:
                    description = f.read().strip()

                with open(os.path.join(manga_path, 'type.txt'), 'r', encoding='utf-8') as f:
                    manga_type = f.read().strip()
                    if manga_type.lower() == 'manga':
                        continue

                manga_folder2 = manga_folder
                if len(manga_folder) > 15:
                    manga_folder2 = manga_folder2[:12] + '...'
                
                
                if len(description) > 50:
                    description = description[:47] + '...'


                # Create a dictionary with the manga data
                manga_data = {
                    'id': manga_id,
                    'title': manga_folder2,
                    'image_title': manga_folder,
                    'description': description,
                    'type': manga_type
                }

                featured_manga.append(manga_data)
            except Exception as e:
                print(f"Error reading manga data from {manga_folder}: {e}")

    return featured_manga

def getAllIds():
    allDirs = os.listdir(MANGA_DIR)
    for dir in allDirs:
        print(dir)
    MANGA_DIR
    pass



def natural_sort_key(s):
    """Sort key that splits strings into numeric and non-numeric parts for natural sorting."""
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def getTBATEid():
    file_path = 'manga/The Beginning After The End/id.txt'

    with open(file_path, 'r') as file:
        # Read the contents of the file
        content = file.read()
        # Print the contents
        print(content)
        file.close()
    return content


# Route for the welcome page
@app.route("/")
def welcomePage():
    featured_manga = get_featured_manga()
    return render_template('welcome.html', featured_manga=featured_manga)


@app.route("/tbate")
def redirectToTheGoat():
    tbateID = getTBATEid()
    return redirect(f"/manga/{tbateID}")

@app.route("/manga/tbate")
def redirectToTheGoat2():
    tbateID = getTBATEid()
    return redirect(f"/manga/{tbateID}")

# Route for the home page
@app.route("/home")
def homePage():
    featured_manga = get_featured_mangaTruncated()
    return render_template('home.html', featured_manga=featured_manga)


def findAllManga():
    manga_list = []
    manga_count = 0

    for manga_folder in os.listdir(MANGA_DIR):
        print(manga_folder)
        manga_path = os.path.join(MANGA_DIR, manga_folder)
        
        if os.path.isdir(manga_path):
            manga_count += 1  # Increment the manga count

            try:
                # Read the id, description, and cover image
                with open(os.path.join(manga_path, 'id.txt'), 'r', encoding='utf-8') as f:
                    manga_id = f.read().strip()

                with open(os.path.join(manga_path, 'description.txt'), 'r', encoding='utf-8') as f:
                    description = f.read().strip()

                with open(os.path.join(manga_path, 'type.txt'), 'r', encoding='utf-8') as f:
                    manga_type = f.read().strip()


                if len(description) > 50:
                    description = description[:47] + '...'

                # Create a dictionary with the manga data
                manga_data = {
                    'id': manga_id,
                    'title': manga_folder,
                    'description': description,
                    'type': manga_type
                }

                manga_list.append(manga_data)

            except Exception as e:
                print(f"Error reading manga data from {manga_folder}: {e}")

    return manga_list, manga_count


@app.route("/manga")
def manga_list():
    mangaList, mangaCount = findAllManga()
    return render_template('manga.html', manga=mangaList, manga_count=mangaCount)




@app.route("/search")
def search():
    return render_template("searchManga.html")




@app.route('/contact')
def contact():
    return render_template('contact.html')




def get_chapters_for_manga(manga_title):
    chapters = []
    chapters_path = os.path.join(MANGA_DIR, manga_title, 'Chapters')
    
    if os.path.isdir(chapters_path):
        for chapter_name in os.listdir(chapters_path):
            chapter_path = os.path.join(chapters_path, chapter_name)
            if os.path.isdir(chapter_path):
                chapters.append({'title': chapter_name})

        # Sort chapters numerically if they follow a pattern like "Chapter 1", "Chapter 2", etc.
        chapters.sort(key=lambda x: int(re.findall(r'\d+', x['title'])[0]) if re.findall(r'\d+', x['title']) else 0)
                
    return chapters




@app.route("/manga/<int:manga_id>")
def manga_detail(manga_id):
    featured_manga = get_featured_manga()
    reccomended_manga = get_featured_mangaTruncatedTitle()  # Correct variable name

    manga = next((m for m in featured_manga if m['id'] == str(manga_id)), None)
    
    if manga:
        chapters = get_chapters_for_manga(manga['title'])
        chapters.reverse()
        return render_template('manga_detail.html',
                               manga=manga,
                               chapters=chapters,           
                               reccomended_manga=reccomended_manga  # Use the correct variable name
                            )
    else:
        return 404




@app.route("/manga_reader")
def manga_reader_home():
    manga_folders = [folder for folder in os.listdir(MANGA_DIR) if os.path.isdir(os.path.join(MANGA_DIR, folder))]
    manga_list = []
    for manga in manga_folders:
        mangaLink = manga
        manga_id_path = os.path.join(MANGA_DIR, manga, 'type.txt')
        if os.path.isfile(manga_id_path):
            with open(manga_id_path, 'r', encoding='utf-8') as f:
                manga_id = f.read().strip()
                if manga_id == "Manga":
                    if len(manga) > 80:
                        manga = manga[:77] + '...'
                    manga_list.append((manga, manga_id, mangaLink))

    return render_template('manga_reader_home.html', manga_list=manga_list)




@app.route("/manga_reader/<manga_name>")
def manga_details(manga_name):
    manga_name = urllib.parse.unquote(manga_name)
    manga_path = os.path.join(MANGA_DIR, manga_name)

    if not os.path.isdir(manga_path):
        return "Manga not found", 404

    # Read manga details
    cover_image = None
    for ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
        potential_cover = os.path.join(manga_path, f'cover_image.{ext}')
        if os.path.isfile(potential_cover):
            cover_image = url_for('static', filename=os.path.relpath(potential_cover, 'static'))
            break

    description_path = os.path.join(manga_path, 'description.txt')
    if os.path.isfile(description_path):
        with open(description_path, 'r', encoding='utf-8') as f:
            description = f.read().strip()
    else:
        description = "No description available."

    # List chapters
    chapters_dir = os.path.join(manga_path, "Chapters")
    chapters = [folder for folder in os.listdir(chapters_dir) if os.path.isdir(os.path.join(chapters_dir, folder))]
    chapters.sort(key=natural_sort_key)
    chapters = chapters[::-1]

    return render_template('manga_details.html', manga_name=manga_name, cover_image=cover_image, description=description, chapters=chapters)




@app.route('/manga_reader/<manga_name>/<chapter_name>')
def manga_reader(manga_name, chapter_name):
    manga_name = urllib.parse.unquote(manga_name)
    chapter_name = urllib.parse.unquote(chapter_name)

    chapter_path = os.path.join(MANGA_DIR, manga_name, "Chapters", chapter_name)
    
    if not os.path.isdir(chapter_path):
        return "Chapter not found", 404
    
    images = sorted([img for img in os.listdir(chapter_path) if img.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'webp'))])
    images = [url_for('manga_reader_image', manga_name=manga_name, chapter_name=chapter_name, filename=img) for img in images]
    images.sort(key=natural_sort_key)

    # Retrieve the list of chapters
    chapters_path = os.path.join(MANGA_DIR, manga_name, "Chapters")
    chapters = sorted(os.listdir(chapters_path), key=natural_sort_key)

    # Find the current chapter index
    current_chapter_index = chapters.index(chapter_name)

    # Determine next and previous chapters
    next_chapter = chapters[current_chapter_index + 1] if current_chapter_index < len(chapters) - 1 else None
    previous_chapter = chapters[current_chapter_index - 1] if current_chapter_index > 0 else None

    # Get the saved height from session
    saved_height = session.get('mangaPanelHeight', 600)

    return render_template('manga_reader.html', images=images, chapter_name=chapter_name, manga_name=manga_name,
                           next_chapter=next_chapter, previous_chapter=previous_chapter, saved_height=saved_height)




@app.route('/save_height', methods=['POST'])
def save_height():
    height = request.json.get('height')
    session['mangaPanelHeight'] = height
    return jsonify({"status": "success"})





@app.route('/manga_reader_image/<manga_name>/<chapter_name>/<filename>')
def manga_reader_image(manga_name, chapter_name, filename):
    manga_name = urllib.parse.unquote(manga_name)
    chapter_name = urllib.parse.unquote(chapter_name)
    chapter_name = replace_special_characters(chapter_name)

    directory = os.path.join(MANGA_DIR, manga_name, "Chapters", chapter_name)
    file_path = os.path.join(directory, filename)
    if not os.path.isfile(file_path):
        abort(404)

    return send_from_directory(directory, filename)




@app.route('/manga/<manga_title>/chapter/<chapterName>')
def chapter_detail(manga_title, chapterName):
    chapter_dir = os.path.join(MANGA_DIR, manga_title, 'Chapters', chapterName)
    try:
        # Get all images in the chapter directory
        images = [f for f in os.listdir(chapter_dir) if os.path.isfile(os.path.join(chapter_dir, f)) and re.match(r'.*\.(jpg|jpeg|gif|webp|png)$', f, re.IGNORECASE)]
        
        # Sort images naturally
        images.sort(key=natural_sort_key)  # Using natsorted for natural sorting
        
        # Get and sort chapters for the manga
        chapters = get_chapters_for_manga(manga_title)
        chapters.sort(key=lambda x: natural_sort_key(x['title']))  # Sort using natural_sort_key
        
        # Find the current chapter's index
        current_index = next((i for i, chapter in enumerate(chapters) if chapter['title'] == chapterName), -1)
        
        # Determine the next and previous chapters
        next_chapter = chapters[current_index + 1]['title'] if current_index != -1 and current_index + 1 < len(chapters) else None
        previous_chapter = chapters[current_index - 1]['title'] if current_index > 0 else None
        
        # Debugging output
        print(f"Current Chapter: {chapterName}")
        print(f"Next Chapter: {next_chapter}")
        print(f"Previous Chapter: {previous_chapter}")
        
        return render_template(
            'manhwaContent.html',
            images=images,
            manga_title=manga_title,
            chapterName=chapterName,
            next_chapter=next_chapter,
            previous_chapter=previous_chapter  # This should be passed correctly
        )

    
    except FileNotFoundError:
        return "Chapter not found", 404




@app.route('/images/<manga_title>/<chapterName>/<filename>')
def get_image(manga_title, filename, chapterName):
    image_dir = os.path.join(MANGA_DIR, manga_title, 'Chapters', chapterName)
    return send_from_directory(image_dir, filename)




# Route for serving cover images
@app.route("/cover/<manga_title>")
def serve_image(manga_title):
    possible_extensions = ['jpg', 'jpeg', 'gif', 'webp', 'png']
    
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
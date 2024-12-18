try:
    from flask import Flask, render_template, request, jsonify, session, send_file, send_from_directory, abort, redirect, url_for
    #print("imported flask")
    import os
    #print("imported os")
    import re
    #print("imported re")
    import requests
    #print("imported requests")
    import json
    #print("imported json")
    import urllib.parse
    #print("imported urllib.parse")
    from dotenv import load_dotenv
    #print("imported load_dotenv")
    import urllib
    #print("imported urllib")
    
    
    import WebScrapers.OnSite.UPDATE
    #print("imported webscrapers.update")
    from WebScrapers.Required.replaceCode import replace_special_characters
    #print("imported replace_special_characters")
    
    
    import WebScrapers.OnSite.mangaReaderDotOrg
    #print("imported WebScrapers.OnSite.mangaReaderDotOrg")
    import WebScrapers.OnSite.manhwaClanDotCom
    #print('imported WebScrapers.OnSite.manhwaClan')
    import WebScrapers.OnSite.readBerserkDotCom
    #print('imported WebScrapers.OnSite.readBerserkDotCom')
    import WebScrapers.OnSite.mangaFireDotTo
    #print('imported WebScrapers.OnSite.mangaFireDotTo')
except ImportError as e:
    input(f"Error importing: {e}")


# Just realised I hadn't added this when I launched this on my laptop for the first time (fatal error)
if not os.path.exists(os.path.join(os.getcwd(), 'manga')):
    os.makedirs(os.path.join(os.getcwd(),'manga'), exist_ok=True)


port = '2222'       # any number you want (4 digits)
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
    """
    Sends a message to a Discord channel using a webhook URL.

    Parameters:
    message (str): The message to be sent to Discord.

    Returns:
    None. Prints a success message if the message is sent successfully,
    or an error message with the status code if the message fails to send.
    """
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
    """
    This function sends a message to a Discord channel using a webhook.
    
    Parameters:
    - request.json: A JSON object containing the email, subject, and body of the message.
    
    Returns:
    - A JSON response indicating whether the message was successfully sent.
    - HTTP status code 400 if any required data is missing.
    - HTTP status code 200 if the message is successfully sent.
    - HTTP status code 500 if the message fails to send.
    """
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
    """
    This function retrieves the featured manga from the MANGA_DIR directory.
    
    Parameters:
    None
    
    Returns:
    featured_manga (list): A list of dictionaries, where each dictionary represents a manga. 
                            Each dictionary contains the manga's id, title, description, and type.
    """
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

def get_featured_manga_and_manhwa():
    """
    This function retrieves the featured manga from the MANGA_DIR directory.
    
    Parameters:
    None
    
    Returns:
    featured_manga (list): A list of dictionaries, where each dictionary represents a manga. 
                            Each dictionary contains the manga's id, title, description, and type.
    """
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
    """
    Retrieve a list of featured manga with truncated descriptions.

    Iterates over each folder in the MANGA_DIR, reads the id, description, and type of each manga,
    and appends a dictionary with the manga data to the featured_manga list.

    Returns:
    featured_manga (list): A list of dictionaries, each containing the id, title, description, and type of a manga.
    """
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
    """
    This function retrieves a list of featured manga with truncated titles and descriptions.

    Parameters:
    None

    Returns:
    featured_manga (list): A list of dictionaries, where each dictionary represents a manga.
                           Each dictionary contains the manga's id, title, image title, description, and type.
    """
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
    """
    This function retrieves and prints all directory names in the MANGA_DIR.

    Parameters:
    None

    Returns:
    None. The function only prints the directory names and does not return any value.
    """
    allDirs = os.listdir(MANGA_DIR)
    for dir in allDirs:
        print(dir)
    print(MANGA_DIR)
    




def natural_sort_key(s):
    """Sort key that splits strings into numeric and non-numeric parts for natural sorting."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]




def getTBATEid():
    """
    This function retrieves the id of the manga 'The Beginning After The End' from a text file.

    Parameters:
    None

    Returns:
    str: The id of the manga 'The Beginning After The End'.

    The function reads the content of the file 'manga/The Beginning After The End/id.txt',
    prints the content, and then returns the content.
    """
    file_path = 'manga/The Beginning After The End/id.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the contents of the file
        content = file.read()
        # Print the contents
        print(content)
        file.close()
    return content




# Route for the welcome page
@app.route("/")
def welcomePage():
    """
    This function is the route for the welcome page. It retrieves the featured manga from the database
    and renders the welcome page with the featured manga.

    Parameters:
    None

    Returns:
    render_template: A rendered HTML template for the welcome page with the featured manga.
    """
    featured_manga = get_featured_manga_and_manhwa()
    return render_template('welcome.html', featured_manga=featured_manga)




@app.route("/tbate")
def redirectToTheGoat():
    """
    Redirects the user to the manga page of 'The Beginning After The End'.

    Parameters:
    None

    Returns:
    redirect: A redirect response to the manga page of 'The Beginning After The End'.
    The manga page URL is constructed using the id retrieved from the function getTBATEid().
    """
    tbateID = getTBATEid()
    return redirect(f"/manga/{tbateID}")




@app.route("/manga/tbate")
def redirectToTheGoat2():
    """
    Redirects the user to the manga page of 'The Beginning After The End'.

    Parameters:
    None

    Returns:
    redirect: A redirect response to the manga page of 'The Beginning After The End'.
    The manga page URL is constructed using the id retrieved from the function getTBATEid().
    """
    tbateID = getTBATEid()
    return redirect(f"/manga/{tbateID}")




# Route for the home page
@app.route("/home")
def homePage():
    """
    This function is the route for the home page. It retrieves the featured manga from the database
    and renders the home page with the featured manga.

    Parameters:
    None

    Returns:
    render_template: A rendered HTML template for the home page with the featured manga.
    The featured manga is obtained using the function `get_featured_mangaTruncated()`.
    """
    featured_manga = get_featured_mangaTruncated()
    return render_template('home.html', featured_manga=featured_manga)




def findAllManga():
    """
    This function retrieves all manga from the MANGA_DIR directory and returns a list of manga data.

    Parameters:
    None

    Returns:
    tuple: A tuple containing two elements:
        - list: A list of dictionaries, where each dictionary represents a manga and contains the manga's id, title, description, and type.
        - int: The total count of manga found.

    The function iterates through each folder in the MANGA_DIR directory. For each folder, it reads the id, description, and type from the respective files.
    It then creates a dictionary with the manga's data and appends it to the manga_list. Finally, it returns the manga_list and the manga_count.
    """
    manga_list = []
    manga_count = 0

    for manga_folder in os.listdir(MANGA_DIR):
        print(manga_folder)
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
                    manga_count += 1  # Increment the manga count
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
    """
    This function retrieves all manga from the MANGA_DIR directory and returns a list of manga data.

    Parameters:
    None

    Returns:
    tuple: A tuple containing two elements:
        - list: A list of dictionaries, where each dictionary represents a manga and contains the manga's id, title, description, and type.
        - int: The total count of manga found.

    The function iterates through each folder in the MANGA_DIR directory. For each folder, it reads the id, description, and type from the respective files.
    It then creates a dictionary with the manga's data and appends it to the manga_list. Finally, it returns the manga_list and the manga_count.
    """
    mangaList, mangaCount = findAllManga()
    return render_template('manga.html', manga=mangaList, manga_count=mangaCount)




@app.route("/search")
def search():
    """
    This function handles the search functionality of the web application.
    It renders the searchManga.html template, which allows users to search for manga.

    Parameters:
    None

    Returns:
    render_template: A rendered HTML template for the search page.
    """
    return render_template("searchManga.html")




@app.route('/contact')
def contact():
    """
    This function handles the contact page of the web application.
    It renders the 'contact.html' template, which displays the contact form and other relevant information.

    Parameters:
    None

    Returns:
    render_template: A rendered HTML template for the contact page.
    """
    return render_template('contact.html')




def get_chapters_for_manga(manga_title):
    """
    Retrieves a list of chapters for a given manga.

    Parameters:
    manga_title (str): The title of the manga for which to retrieve chapters.

    Returns:
    list: A list of dictionaries, where each dictionary represents a chapter.
          Each dictionary contains a 'title' key with the chapter's title.
          The chapters are sorted numerically if they follow a pattern like "Chapter 1", "Chapter 2", etc.
    """
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
    """
    This function retrieves the details of a specific manga based on its ID.
    It retrieves the featured manga and recommended manga, then finds the manga with the given ID.
    If the manga is found, it retrieves the chapters for the manga and renders the 'manga_detail.html' template.
    If the manga is not found, it returns a 404 status code.

    Parameters:
    manga_id (int): The ID of the manga to retrieve details for.

    Returns:
    render_template: If the manga is found, it renders the 'manga_detail.html' template with the manga details, chapters, and recommended manga.
                     If the manga is not found, it returns a 404 status code.
    """
    featured_manga = get_featured_manga()
    reccomended_manga = get_featured_mangaTruncatedTitle()  # Correct variable name

    manga = next((m for m in featured_manga if m['id'] == str(manga_id)), None)
    
    if manga:
        chapters = get_chapters_for_manga(manga['title'])
        chapters.reverse()
        return render_template('manga_detail.html',
                               mangaId = manga_id,
                               manga=manga,
                               chapters=chapters,           
                               reccomended_manga=reccomended_manga  # Use the correct variable name
                            )
    else:
        return 404







def buildURLFromID(search_id):
    """
    This function constructs a URL for a manga based on its ID.

    Parameters:
    search_id (str): The ID of the manga to search for.

    Returns:
    str: The constructed URL for the manga. If the file with the correct ID is not found, it returns None.
    """
    base_directory = 'manga/'

    # Walk through the directory tree
    for root, dirs, files in os.walk(base_directory):
        # Check if 'id.txt' file is in the current directory
        if 'id.txt' in files:
            # Construct the path to the 'id.txt' file
            file_path = os.path.join(root, 'id.txt')

            # Read the contents of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                file_id = file.read().strip()  # Read and strip any extra whitespace
                file_path = file_path[:-7]
                # Check if the ID in the file matches the search_id
                if file_id == search_id:
                    manga_name = file_path.lower()
                    manga_name = manga_name.replace(' ', '-')
                    print(manga_name)
                    # Construct the URL (you can adjust this format as needed)
                    url = f'https://www.mangaread.org/{manga_name}'

                    return url
    # Return None if the file with the correct ID is not found
    return None





@app.route('/updateManhwa', methods=['POST'])
def updateManhwaFunction():
    mangaID = request.json.get('mangaId')
    print(f"Manga ID recieved: {mangaID}")
    url = buildURLFromID(search_id=str(mangaID))
    print(f"URL created: {url}")
    WebScrapers.OnSite.mangaReaderDotOrg.main(url=url)
    
    return f"Updated {url}", 200




@app.route("/manga_reader")
def manga_reader_home():
    """
    This function retrieves a list of manga folders from the MANGA_DIR directory and prepares a list of manga data for the manga reader home page.

    Parameters:
    None

    Returns:
    render_template: A rendered HTML template for the manga reader home page, containing a list of manga data. The manga data includes the manga name, ID, and link.

    The function iterates through the manga folders in the MANGA_DIR directory. For each manga folder, it checks if the 'type.txt' file exists and if its content is "Manga".
    If the conditions are met, it appends a tuple containing the manga name, ID, and link to the manga_list. If the manga name is longer than 80 characters, it truncates it to 77 characters and appends an ellipsis.
    Finally, it returns the rendered HTML template for the manga reader home page with the manga_list.
    """
    manga_folders = [folder for folder in os.listdir(MANGA_DIR) if os.path.isdir(os.path.join(MANGA_DIR, folder))]
    manga_list = []
    for manga in manga_folders:
        mangaLink = manga
        manga_type_path = os.path.join(MANGA_DIR, manga, 'type.txt')
        manga_description_path = os.path.join(MANGA_DIR, manga, 'description.txt')
        if os.path.isfile(manga_type_path):
            with open(manga_type_path, 'r', encoding='utf-8') as f:
                manga_type = f.read().strip()
                if manga_type == "Manga":
                    
                    if os.path.isfile(manga_description_path):
                        with open(manga_description_path, 'r', encoding='utf-8') as f:
                            manga_description = f.read().strip()
                            if len(manga_description) > 424:
                                manga_description = manga_description[:397]
                                manga_description += "..."
                    
                    manga_list.append((manga, manga_type, mangaLink, manga_description))
                    total_manga = len(manga_list)
    return render_template('manga_reader_home.html', manga_list=manga_list, numOfManga=total_manga)

def berserk_sort_key(chapter_name):
    # Define your custom sorting logic here
    # Example: Extract numbers from chapter names to sort numerically
    numbers = re.findall(r'\d+', chapter_name)
    return int(numbers[0]) if numbers else float('inf')


@app.route("/manga_reader/<manga_name>")
def manga_details(manga_name):
    """
    This function retrieves the details of a specific manga based on its name.
    It retrieves the cover image, description, and a list of chapters for the manga.
    """
    manga_name = urllib.parse.unquote(manga_name)
    manga_path = os.path.join(MANGA_DIR, manga_name)
    
    if not os.path.isdir(manga_path):
        return "Manga not found", 404

    # Read manga cover image
    cover_image = None
    for ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
        potential_cover = os.path.join(manga_path, f'cover_image.{ext}')
        if os.path.isfile(potential_cover):
            cover_image = url_for('static', filename=os.path.relpath(potential_cover, 'static'))
            break

    # Read description
    description_path = os.path.join(manga_path, 'description.txt')
    if os.path.isfile(description_path):
        with open(description_path, 'r', encoding='utf-8') as f:
            description = f.read().strip()
    else:
        description = "No description available."

    # Read manga ID
    id_path = os.path.join(manga_path, 'id.txt')
    if os.path.isfile(id_path):
        with open(id_path, 'r', encoding='utf-8') as f:
            manga_id = f.read().strip()
    else:
        manga_id = "ID not found."

    # List chapters
    chapters_dir = os.path.join(manga_path, "Chapters")
    chapters = [folder for folder in os.listdir(chapters_dir) if os.path.isdir(os.path.join(chapters_dir, folder))]
    if manga_name == "Berserk":
        chapters.sort(key=berserk_sort_key)  # Custom sort function
    else:
        chapters.sort(key=natural_sort_key)
    chapters = chapters[::-1]

    # Generate URLs for chapter thumbnails
    images = [
        url_for('serve_thumbnail_chapter', manga_title=manga_name, chapterName=chapter)
        for chapter in chapters
    ]

    return render_template('manga_details.html', manga_name=manga_name, cover_image=cover_image, description=description, chapters=chapters, manga_id=manga_id, images=images)





@app.route('/manga_reader/<manga_name>/<chapter_name>')
def manga_reader(manga_name, chapter_name):
    """
    This function handles the display of a specific chapter in the manga reader.
    It retrieves the list of images in the chapter directory, sorts them naturally,
    and retrieves the list of chapters for the manga. It also determines the next
    and previous chapters.

    Parameters:
    manga_name (str): The name of the manga.
    chapter_name (str): The name of the chapter.

    Returns:
    render_template: A rendered HTML template for the manga reader, containing
                     the images, chapter name, manga name, next chapter, previous chapter,
                     and the saved height from the session. If the chapter directory
                     does not exist, it returns a 404 status code with the message "Chapter not found".
    """
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





@app.route('/update')
def update():
    return render_template('update.html')




@app.route('/update/<id>', methods=['POST'])
def update_id(id):
    print(f"Received ID from URL: {id}")
    WebScrapers.OnSite.UPDATE.main(str(id))
    return jsonify({"id": id})


@app.route('/scrape')
def scrapers():
    return render_template('scrapers.html')


@app.route('/scrape/mangaReaderOrg')
def scrapemangaReaderOrg():
    return render_template('scrapemangaReaderOrg.html')


@app.route('/scrape/manhwaClanCom')
def scrapemanhwaClanCom():
    return render_template('scrapemanhwaClanCom.html')


@app.route('/scrape/Berserk')
def scrapeBerserkPage():
    return render_template('scrapeBerserk.html')

@app.route('/scrape/mangaFireDotTo')
def scrapemangaFireDotTo():
    return render_template('scrapemangaFireDotTo.html')


@app.route('/real/scrape/berserk', methods=['POST'])
def scrape_berserk():
    try:
        print(f"Scraping Berserk")
        WebScrapers.OnSite.readBerserkDotCom.main()
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error scraping mangaReaderOrg: {e}")
        return jsonify({"status": "error", "error": str(e)})


@app.route('/real/scrape/mangaReaderOrg', methods=['POST'])
def scrape_mangaReaderOrg():
    data = request.get_json()
    if data and 'link' in data:
        
        try:
            link = data['link']
            print(f"Starting Scraping mangaReaderOrg")
            WebScrapers.OnSite.mangaReaderDotOrg.main(link)
            return jsonify({"status": "success"})
        
        except Exception as e:
            print(f"Error scraping mangaReaderOrg: {e}")
            return jsonify({"status": "error", "error": str(e)})
        
    else:
        print("data not recieved /real/scrape/mangaReaderOrg")
        return jsonify({"status": "error", "error": str(e)})
    


@app.route('/real/scrape/manhwaClanDotCom', methods=['POST'])
def scrape_manhwaClanDotCom():
    data = request.get_json()
    if data and 'link' in data:
        
        try:
            link = data['link']
            print(f"Starting Scraping manhwaClanDotCom")
            WebScrapers.OnSite.manhwaClanDotCom.main(link)
            return jsonify({"status": "success"})
        
        except Exception as e:
            print(f"Error scraping manhwaClanDotCom: {e}")
            return jsonify({"status": "error", "error": str(e)})
        
    else:
        print("data not recieved /real/scrape/manhwaClanDotCom")
        return jsonify({"status": "error", "error": str(e)})

@app.route('/real/scrape/mangaFireDotTo', methods=['POST'])
def scrape_mangaFireDotTo():
    data = request.get_json()
    if data and 'link' in data:
        
        try:
            link = data['link']
            print(f"Starting Scraping mangaFireDotTo")
            manga = WebScrapers.OnSite.mangaFireDotTo.MangaFire(link)
            manga.scrape()
            return jsonify({"status": "success"})
        
        except Exception as e:
            print(f"Error scraping mangaFireDotTo: {e}")
            return jsonify({"status": "error", "error": str(e)})
        
    else:
        print("data not recieved /real/scrape/mangaFireDotTo")
        return jsonify({"status": "error", "error": str(e)})


@app.route('/save_height', methods=['POST'])
def save_height():
    """
    This function handles the POST request to save the height of the manga panel.
    It retrieves the height from the request JSON data, saves it in the session,
    and returns a JSON response with a status of "success".

    Parameters:
    None

    Returns:
    jsonify: A JSON response with a status of "success".
    """
    height = request.json.get('height')
    session['mangaPanelHeight'] = height
    return jsonify({"status": "success"})




@app.route('/manga_reader_image/<manga_name>/<chapter_name>/<filename>')
def manga_reader_image(manga_name, chapter_name, filename):
    """
    Serves an image file for a specific manga chapter.

    Parameters:
    manga_name (str): The name of the manga.
    chapter_name (str): The name of the chapter.
    filename (str): The name of the image file.

    Returns:
    send_from_directory: A response that sends the image file from the specified directory.
                         If the file does not exist, it returns a 404 status code.
    """
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
    """
    This function retrieves and displays the images for a specific chapter in a manga.
    It also retrieves the next and previous chapters for navigation.

    Parameters:
    manga_title (str): The title of the manga.
    chapterName (str): The name of the chapter.

    Returns:
    render_template: A response that renders the 'manhwaContent.html' template with the images, manga title, chapter name, next chapter, and previous chapter.
                     If the chapter directory does not exist, it returns a 404 status code with the message "Chapter not found".
    """
    chapter_dir = os.path.join(MANGA_DIR, manga_title, 'Chapters', chapterName)
    try:
        # Get all images in the chapter directory
        images = [f for f in os.listdir(chapter_dir) if os.path.isfile(os.path.join(chapter_dir, f)) and re.match(r'.*\.(jpg|jpeg|gif|webp|png)$', f, re.IGNORECASE)]
        
        # Get the manhwa id for the link in the page
        manhwaID = None
        manhwaPath = os.path.join(MANGA_DIR, manga_title)
        print(manhwaPath)
        if os.path.isdir(manhwaPath):
            id_path = os.path.join(manhwaPath, 'id.txt')
            print(id_path)
            try:
                with open(id_path, 'r') as f:
                    manhwaID = f.read()
                    f.close()
            except FileNotFoundError as e:
                input(e)
        
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
            id=manhwaID,
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
    """
    Serves an image file from a specific manga chapter.

    Parameters:
    manga_title (str): The title of the manga.
    filename (str): The name of the image file.
    chapterName (str): The name of the chapter.

    Returns:
    send_from_directory: A response that sends the image file from the specified directory.
    """
    image_dir = os.path.join(MANGA_DIR, manga_title, 'Chapters', chapterName)
    return send_from_directory(image_dir, filename)

@app.route("/thumbnail/<manga_title>/<chapterName>")
def serve_thumbnail_chapter(manga_title, chapterName):
    possible_extensions = ['jpg', 'jpeg', 'gif', 'webp', 'png']
    chapter_dir = os.path.join(MANGA_DIR, manga_title, 'Chapters', chapterName)
    
    #print(f"Looking in directory: {chapter_dir}")
    
    for ext in possible_extensions:
        image_filename1 = f'image_1.{ext}'
        image_filename2 = f'image_01.{ext}'
        full_path1 = os.path.join(chapter_dir, image_filename1)
        full_path2 = os.path.join(chapter_dir, image_filename2)
        #print(f"Checking: {full_path}")
        
        if os.path.exists(full_path1):
            #print("Sending image:", full_path)
            return send_from_directory(chapter_dir, image_filename1)
        elif os.path.exists(full_path2):
            #print("Sending image:", full_path)
            return send_from_directory(chapter_dir, image_filename2)
    
    print("Image not found, failed")
    return abort(404)



# Route for serving cover images
@app.route("/cover/<manga_title>")
def serve_image(manga_title):
    """
    Serves an image file from a specific manga directory based on the given manga title.
    It checks for different image file extensions and returns the first existing file.
    If no image file is found, it returns a 404 status code.

    Parameters:
    manga_title (str): The title of the manga for which to serve the cover image.

    Returns:
    send_from_directory: If an image file is found, it sends the image file from the specified directory.
                         If no image file is found, it returns a 404 status code.
    """
    possible_extensions = ['jpg', 'jpeg', 'gif', 'webp', 'png']
    
    # Check for each extension if the file exists
    for ext in possible_extensions:
        image_path = os.path.join(MANGA_DIR, manga_title, f'cover_image.{ext}')
        if os.path.exists(image_path):
            return send_from_directory(os.path.join(MANGA_DIR, manga_title), f'cover_image.{ext}')
    
    return abort(404)




@app.errorhandler(404)
def page_not_found(e):
    """
    This function handles the 404 error and renders a custom 404 page.

    Parameters:
    e (Exception): The exception object that caused the 404 error.

    Returns:
    render_template: A response that renders the '404.html' template with the error message.
                     The status code of the response is set to 404.
    """
    return render_template('404.html', error=e), 404




if __name__ == '__main__':
    try:
        app.run(port=port, debug=debug, host=host)
    except Exception as e:
        print(f"Error running the app: {e}")
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re
from Required.replaceCode import replace_special_characters

# Constants
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
DIRECTORY_PATH = 'manga'
MAX_DIR_NAME_LENGTH = 255

def validDirName(text):
    # Replace invalid characters with underscores
    text = re.sub(r'[<>:"/\\|?*]', '', text).strip()
    return text[:MAX_DIR_NAME_LENGTH] 

def count_directories(base_path):
    try:
        entries = os.listdir(base_path)
        dir_count = sum([1 for entry in entries if os.path.isdir(os.path.join(base_path, entry))])
        return str(dir_count)
    except FileNotFoundError:
        print(f"The directory {base_path} does not exist.")
    except PermissionError:
        print(f"Permission denied to access the directory {base_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_links_in_reverse_order(url):
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_div = soup.find('div', class_='post-title')
        if title_div:
            title = title_div.find('h1').text.strip()
            safe_title = replace_special_characters(validDirName(title))
            directory_path = f'{DIRECTORY_PATH}/{safe_title}'
            os.makedirs(directory_path, exist_ok=True)
            print(f"Title Directory: {directory_path}")
        else:
            title = safe_title = "default_directory"
        
        links_div = soup.find('div', class_='listing-chapters_wrap cols-1 show-more')
        if links_div:
            links = [a['href'] for a in links_div.find_all('a', href=True)]
            links.reverse()
            for link in links:
                print(f"Link: {link}")
        else:
            print("The specified div was not found in the HTML.")
        
        img_div = soup.find('div', class_='summary_image')
        if img_div:
            img = img_div.find("img")
            img_url = urljoin(url, img.get('src'))
            if img_url:
                print(f'Found image URL: {img_url}')
                img_response = requests.get(img_url, headers={'User-Agent': USER_AGENT}, stream=True)
                if img_response.status_code == 200:
                    img_ext = os.path.splitext(img_url)[1]
                    img_name = os.path.join(directory_path, f'cover_image{img_ext}')
                    print(f"Image Path: {img_name}")
                    with open(img_name, 'wb') as handler:
                        for chunk in img_response.iter_content(chunk_size=1024):
                            if chunk:
                                handler.write(chunk)
                    print(f'Downloaded {img_name}')
                else:
                    print(f'Failed to download image from {img_url}. Status code: {img_response.status_code}')
        else:
            print("The specified div was not found in the HTML.")
        
        content_div = soup.find('div', class_='description-summary')
        if content_div:
            paragraphs = content_div.find_all('p')
            content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
            desc_path = os.path.join(directory_path, 'description.txt')
            print(f"Description Path: {desc_path}")
            with open(desc_path, 'w', encoding='utf-8') as descFile:
                descFile.write(content)
        else:
            print("The specified div was not found in the HTML.")
        
        post_content_div = soup.find('div', class_='post-content')
        type_value = None
        if post_content_div:
            for item in post_content_div.find_all('div', class_='post-content_item'):
                type_heading = item.find('div', class_='summary-heading').find('h5')
                if type_heading and type_heading.text.strip() == 'Type':
                    type_value = item.find('div', class_='summary-content').text.strip()
            type_path = os.path.join(directory_path, 'type.txt')
            print(f"Type Path: {type_path}")
            with open(type_path, 'w', encoding='utf-8') as typeFile:
                typeFile.write(type_value if type_value else '')
        
        id_path = os.path.join(directory_path, 'id.txt')
        if not os.path.exists(id_path):
            print(f"ID Path: {id_path}")
            with open(id_path, 'w', encoding='utf-8') as id_file:
                id_file.write(count_directories(DIRECTORY_PATH))
                id_file.close()
        
        websiteFrom = os.path.join(directory_path, 'website.txt')
        print(f"Website Path: {websiteFrom}")
        if not os.path.exists(websiteFrom):
            with open(websiteFrom, 'w', encoding='utf-8') as website_file:
                website_file.write('mangaReaderDotOrg')
                website_file.close()
        
        return links, title
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    



def webScrape(url, title):
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        container = soup.find(class_='reading-content')
        
        safe_title = replace_special_characters(validDirName(title))
        chapters_dir = os.path.join(DIRECTORY_PATH, safe_title, 'Chapters')
        os.makedirs(chapters_dir, exist_ok=True)
        
        chapter_name = soup.find('h1', id='chapter-heading').text.strip()
        if chapter_name and title in chapter_name:
            chapter_name = chapter_name[len(title)+3:]
        
        chapter_dir = os.path.join(chapters_dir, replace_special_characters(validDirName(chapter_name)))
        
        
        if container:
            img_tags = container.find_all('img')
            os.makedirs(chapter_dir, exist_ok=True)
            for i, img in enumerate(img_tags, start=1):
                img_url = urljoin(url, img.get('src'))
                if img_url:
                    print(f'Found image URL: {img_url}')
                    img_response = requests.get(img_url, headers={'User-Agent': USER_AGENT}, stream=True)
                    if img_response.status_code == 200:
                        img_ext = os.path.splitext(img_url)[1]
                        img_name = os.path.join(chapter_dir, f'image_{i}{img_ext}')
                        print(f"Image Path: {img_name}")
                        with open(img_name, 'wb') as handler:
                            for chunk in img_response.iter_content(chunk_size=1024):
                                if chunk:
                                    handler.write(chunk)
                        print(f'Downloaded {img_name}')
                    else:
                        print(f'Failed to download image from {img_url}. Status code: {img_response.status_code}')
        else:
            print("The specified class was not found in the HTML.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


def print_chapters(url):
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        chapters_div = soup.find('div', class_='listing-chapters_wrap cols-1 show-more')
        
        if chapters_div:
            chapters = [a.text.strip() for a in chapters_div.find_all('a')]
            chapters.reverse()
            for chapter in chapters:
                print(f"Chapter Name: {chapter}")
            return chapters  # Return a list of chapter names
        else:
            print("The specified div was not found in the HTML.")
            return []
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

def checkExistence(chapters, title):
    safe_title = replace_special_characters(validDirName(title))
    skips = 0
    
    chapters_dir = os.path.join(DIRECTORY_PATH, safe_title, 'Chapters')
    
    for chapter in chapters:
        chapter_dir = os.path.join(chapters_dir, replace_special_characters(validDirName(chapter)))
        
        if os.path.exists(chapter_dir):
            print(f"Chapter {chapter} already exists.")
            skips += 1
    if skips == 0:
        return False, 0
    else:
        return True, skips

def main(url):
    iteration = 0
    
    links, title = print_links_in_reverse_order(url)
    chapters = print_chapters(url)
    result, skips = checkExistence(chapters, title)
    
    if result:
        iteration += skips
        
    while iteration < len(links):
        webScrape(links[iteration], title)
        iteration += 1


if __name__ == '__main__':
    numberOfMangas = int(input("Enter the number of mangas: "))
    mangas = [input(f"Enter the URL of manga {i+1}: ") for i in range(numberOfMangas)]
    for manga in mangas:
        main(manga)

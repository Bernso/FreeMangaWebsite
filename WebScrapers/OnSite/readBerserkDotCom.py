import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re
from WebScrapers.Required.replaceCode import replace_special_characters

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
        
        title = "Berserk"
        safe_title = replace_special_characters(validDirName(title))
        directory_path = f'{DIRECTORY_PATH}/{safe_title}'
        os.makedirs(directory_path, exist_ok=True)
        print(f"Title Directory: {directory_path}")
        
        
        links_div = soup.find('table', class_='table table-striped table-borderless')
        if links_div:
            links = [a['href'] for a in links_div.find_all('a', href=True)]
            links.reverse()
            for link in links:
                print(f"Link: {link}")
        else:
            print("The specified div was not found in the HTML.")
        
        #quit()
        
        
        img_url = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/daa27cc0-d199-4cc7-a270-dcfc8e662ede/dbha85n-808a835f-2d17-4380-a15a-8646d4ef56fe.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi9kYWEyN2NjMC1kMTk5LTRjYzctYTI3MC1kY2ZjOGU2NjJlZGUvZGJoYTg1bi04MDhhODM1Zi0yZDE3LTQzODAtYTE1YS04NjQ2ZDRlZjU2ZmUuanBnIn1dXX0.iyM21niEMxVYLhuGxo27fDtBEyTga5zrKlpZPEJASkc"
        if img_url:
            print(f'Found image URL: {img_url}')
            img_response = requests.get(img_url, headers={'User-Agent': USER_AGENT}, stream=True)
            if img_response.status_code == 200:
                img_name = os.path.join(directory_path, f'cover_image.jpg')
                print(f"Image Path: {img_name}")
                with open(img_name, 'wb') as handler:
                    for chunk in img_response.iter_content(chunk_size=1024):
                        if chunk:
                            handler.write(chunk)
                print(f'Downloaded {img_name}')
            else:
                print(f'Failed to download image from {img_url}. Status code: {img_response.status_code}')
        
        #quit()
        
        content = """Berserk (Japanese: ベルセルク, Hepburn: Beruseruku) is a Japanese manga series written and illustrated by Kentaro Miura. Set in a medieval Europe-inspired dark fantasy world, the story centers on the characters of Guts, a lone swordsman, and Griffith, the leader of a mercenary band called the "Band of the Hawk". The series follows Guts' journey seeking revenge on Griffith, who betrayed him and sacrificed his comrades to become a powerful demonic being."""
        desc_path = os.path.join(directory_path, 'description.txt')
        print(f"Description Path: {desc_path}")
        with open(desc_path, 'w', encoding='utf-8') as descFile:
            descFile.write(content)
            descFile.close()
        
        #quit()
        
        type_value = "Manga"
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
                website_file.write('readBerserkDotCom')
                website_file.close()
        #quit()
        return links, title
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


def webScrape(url, title):
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        container = soup.find('div', class_='pages text-center')
        
        safe_title = replace_special_characters(validDirName(title))
        chapters_dir = os.path.join(DIRECTORY_PATH, safe_title, 'Chapters')
        os.makedirs(chapters_dir, exist_ok=True)
        
        chapter_name = soup.find('h1', class_='mb-3').text.strip()
        if chapter_name and title in chapter_name:
            chapter_name = chapter_name[len(title)+1:]
        
        chapter_dir = os.path.join(chapters_dir, replace_special_characters(validDirName(chapter_name)))
        if os.path.exists(chapter_dir):
            print(f"Chapter {chapter_name} already exists.")
            return
        #quit()
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
                        if '?' in img_ext:
                            img_ext = img_ext.split('?')[0]
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


def main():
    url = "https://readberserk.com/"
    links, title = print_links_in_reverse_order(url)
    for link in links:
        webScrape(link, title)

if __name__ == '__main__':
    main()

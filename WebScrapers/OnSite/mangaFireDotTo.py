try:
    import requests
    from bs4 import BeautifulSoup
    import os
    from urllib.parse import urljoin
    import re
    import time
    from WebScrapers.Required.replaceCode import replace_special_characters
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
except ImportError as e:
    input(e)
    quit()

class WebDriverManager:
    _instance = None
    _driver = None

    def __new__(cls, headless=True):
        if not cls._instance:
            cls._instance = super(WebDriverManager, cls).__new__(cls)
            cls._driver = cls._create_webdriver(headless)
        return cls._instance

    @classmethod
    def _create_webdriver(cls, headless=True):
        chrome_options = Options()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        if headless:
            chrome_options.add_argument('--headless')
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_window_size(1920, 1080)
        
        return driver

    @classmethod
    def get_driver(cls, headless=True):
        if not cls._driver or not cls._driver.service.is_connectable():
            cls._driver = cls._create_webdriver(headless)
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            try:
                cls._driver.quit()
            except Exception:
                pass
            cls._driver = None
            cls._instance = None

class MangaFireScraper:
    DEFAULT_URL = 'https://mangafire.to/read/hunter-x-hunter22.9onq/en/chapter-403'
    TEMP_DIR = os.path.join(os.getcwd(), 'temp')
    BASE_MANGA_DIR = os.path.join(os.getcwd(), 'manga')
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/536.36'
    }
    
    def __init__(
        self, 
        chapter_name="Chapter 403",
        manga_name="Hunter X Hunter",
        url="https://mangafire.to/read/hunter-x-hunter22.9onq/en/chapter-403",
        timeout=1,
        min_images=1,
        headless=True,
        driver=None
    ):
        self.url = url or self.DEFAULT_URL
        self.chapter_name = replace_special_characters(chapter_name.strip())
        self.manga_name = replace_special_characters(manga_name.strip())
        
        self.timeout = timeout
        self.min_images = min_images
        self.headless = headless
        
        self.total_pages = None
        self.driver = driver or WebDriverManager.get_driver(headless)
        
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        os.makedirs(os.path.join(self.BASE_MANGA_DIR, self.manga_name.strip(), 'Chapters', self.chapter_name.strip()), exist_ok=True)
    
    def wait_for_images_to_load(self, driver):
        try:
            WebDriverWait(driver, self.timeout).until(lambda d: len(d.find_elements(By.TAG_NAME, 'img')) >= self.min_images)
        except Exception:
            pass
    
    def find_total_pages(self, driver):
        try:
            total_pages_element = driver.find_element(By.CSS_SELECTOR, 'b.total-page')
            total_pages_text = total_pages_element.text.strip()
            return int(total_pages_text)
        except Exception as e:
            print(f"Could not find total pages: {e}")
            return 2
    
    def save_pages(self, driver, total_pages):
        page_number = 1
        
        while page_number <= total_pages:
            try:
                page_path = os.path.join(self.TEMP_DIR, f'page_{page_number}.html')
                with open(page_path, 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                
                next_page_button = driver.find_element(By.ID, 'page-go-right')
                next_page_button.click()
                page_number += 1
                
                time.sleep(0.5)
            
            except Exception as e:
                print(f"Error saving page {page_number}: {e}")
                break
    
    def extract_image_sources(self, max_page_path):
        with open(max_page_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        image_links = [img['src'] for img in soup.find_all('img', class_='fit-w') if 'src' in img.attrs]
        
        return image_links
    
    def download_images(self, image_links):
        chapter_dir = os.path.join(self.BASE_MANGA_DIR, self.manga_name.strip(), 'Chapters', self.chapter_name.strip())
        
        for index, link in enumerate(image_links, 1):
            try:
                response = requests.get(link, stream=True)
                response.raise_for_status()
                
                file_path = os.path.join(chapter_dir, f'{index:03d}.jpg')
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"Saved image {index}: {file_path}")
            
            except Exception as e:
                print(f"Error downloading image from {link}: {e}")
    
    def clean_temp_directory(self):
        if os.path.exists(self.TEMP_DIR):
            for filename in os.listdir(self.TEMP_DIR):
                file_path = os.path.join(self.TEMP_DIR, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    def scrape(self):
        try:
            self.driver.get(self.url)
            time.sleep(1)
            self.total_pages = self.find_total_pages(self.driver)
            self.save_pages(self.driver, self.total_pages)
            
            max_page_path = os.path.join(self.TEMP_DIR, f'page_{self.total_pages}.html')
            image_links = self.extract_image_sources(max_page_path)
            self.download_images(image_links)
            self.clean_temp_directory()
        
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
        return self.driver  # Return the driver for reuse

class MangaFire:
    def __init__(self, url='https://mangafire.to/manga/tensei-shitara-slime-datta-kenn.5kq'):
        self.url = url
        self.__headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/536.36'}
    
    def create_info(self, name):
        directory_path = os.path.join('manga', name.strip())
        with open(os.path.join(directory_path, 'website.txt'), 'w') as f:
            f.write("mangaFireDotTo")
            f.close()
        entries = os.listdir('manga')
        directories = str(sum([1 for entry in entries if os.path.isdir(os.path.join('manga', entry))]))
        with open(os.path.join(directory_path, 'id.txt'), 'w', encoding='utf-8') as id_file:
            id_file.write(directories)
            id_file.close()
        response = requests.get(self.url, headers=self.__headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            with open(os.path.join('temp.html'), 'w', encoding='utf-8') as f:
                descriptions = soup.find_all('div', class_='modal-content p-4')
                length = len(descriptions)
                description = descriptions[length - 1].text.strip()
                type_data = soup.find('div', class_='min-info')
                a_tag = type_data.find('a')
                if a_tag:
                    type_data = a_tag.text.strip()
                else:
                    type_data = 'N/A'
                f.write(soup.prettify())
                f.close()
        with open(os.path.join(directory_path, 'description.txt'), 'w', encoding='utf-8') as description_file:
            description_file.write(description)
            description_file.close()
        with open(os.path.join(directory_path, 'type.txt'), 'w', encoding='utf-8') as type_file:
            type_file.write(type_data)
            type_file.close()
        # Remove the temporary HTML file
        if os.path.exists('temp.html'):
            os.remove('temp.html')

    def get_links(self):
        response = requests.get(self.url, headers=self.__headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            chapterList = soup.find('ul', class_='scroll-sm')
            chapterLinks = chapterList.find_all('a')
            return [urljoin(self.url, link['href']) for link in chapterLinks]
    
    def get_image(self):
        print("Attempting to fetch image...")
        response = requests.get(self.url, headers=self.__headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            imgDiv = soup.find('div', class_='poster')
            poster = imgDiv.find('img')
            img_url = poster['src'] if 'src' in poster.attrs else None
            
            manga_folder = os.path.join('manga', poster['alt'].strip())
            os.makedirs(manga_folder, exist_ok=True)
            
            try:
                response = requests.get(img_url, headers=self.__headers)
                response.raise_for_status()
                
                cover_image_path = os.path.join(manga_folder, 'cover_image.jpg')
                with open(cover_image_path, 'wb') as f:
                    f.write(response.content)
                print(f"Poster image saved to {cover_image_path}")
                return poster['alt'].strip()
            except requests.RequestException as e:
                print(f"Error downloading poster image: {e}")

    def get_chapter_names(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  
            data = []
            soup = BeautifulSoup(response.text, 'html.parser')
            ul_element = soup.select_one('ul.scroll-sm')
            if ul_element:
                chapters = [li for li in ul_element.find_all('li')]
                for chapter in chapters:
                    name = chapter.find('span')
                    if name:
                        print(name.text)
                    data.append(name.text)
                return data
            else:
                print("No `ul.scroll-sm` element found on the page.")
                return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    
    def scrape(self):
        manga_name = self.get_image()
        self.create_info(manga_name)
        names = self.get_chapter_names()
        links = self.get_links()
        names = names[::-1]
        links = links[::-1]
        links_names = zip(links, names)
        driver = None
        for link, name in links_names:
            scraper = MangaFireScraper(name, manga_name, link, driver=driver)
            driver = scraper.scrape()
        print("\n\n\n\nCOMPLETE")

if __name__ == '__main__':
    url = str(input("Enter manga url: "))
    manga = MangaFire(url)
    manga.scrape()
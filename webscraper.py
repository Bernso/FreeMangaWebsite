try:
    import requests
    from bs4 import BeautifulSoup
    import os
    from urllib.parse import urljoin
    import re
except ImportError as e:
    print(f"Import Error: {e}")




# URL of the page to scrape
# https://www.mangaread.org/manga/the-beginning-after-the-end/


def validDirName(text):
    # Replace invalid characters with underscores
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    
    # Trim leading and trailing spaces
    text = text.strip()
    
    # Ensure directory name is not empty
    if not text:
        text = "default_directory"
    
    # Optionally, you can limit the length of the directory name
    max_length = 255
    if len(text) > max_length:
        text = text[:max_length]
    
    return text

def count_directories():
    try:
        directory_path = 'manga'
        # List all entries in the given directory
        entries = os.listdir(directory_path)
        
        # Count the number of directories
        dir_count = sum([1 for entry in entries if os.path.isdir(os.path.join(directory_path, entry))])
        
        print(dir_count)
        
        return str(dir_count)
    except FileNotFoundError:
        print(f"The directory {directory_path} does not exist.")
    except PermissionError:
        print(f"Permission denied to access the directory {directory_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
        

def print_links_in_reverse_order(url):
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    
    # Make a request to the webpage
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the div with the specific class
        div = soup.find('div', class_='listing-chapters_wrap cols-1 show-more')
        
        # If the div exists, find all links within it
        if div:
            links = div.find_all('a', href=True)  # Find all 'a' tags with 'href' attributes
            link_urls = [a['href'] for a in links]  # Extract the href attribute from each link
            
            
            # Reverse the order of the links
            link_urls.reverse()
            
            # Print each link URL
            for link in link_urls:
                print(link)
        else:
            print("The specified div was not found in the HTML.")
            
            
                
        div = soup.find('div', class_='post-title')
        if div:
            title = div.find('h1').text.strip()
            print(title)
        else:
            print("The specified div was not found in the HTML.")
        os.makedirs(f'manga/{validDirName(title)}', exist_ok=True)
            
        div = soup.find('div', class_='summary_image')
        if div:
            img = div.find("img")
            img_url = img.get('src')
            img_url = urljoin(url, img_url)
            
            if img_url:
                    print(f'Found image URL: {img_url}')
                    
                    # Download the image using stream to handle large files
                    img_response = requests.get(img_url, headers=headers, stream=True)
                    
                    # Check if the request was successful
                    if img_response.status_code == 200:
                        # Get the image file name and extension
                        img_extension = os.path.splitext(img_url)[1]  # Get the extension from the URL
                        img_name = os.path.join(f'manga/{validDirName(title)}', f'cover_image{img_extension}')
                        
                        # Open a file for writing the binary data
                        with open(img_name, 'wb') as handler:
                            # Write the image in chunks to avoid high memory usage
                            for chunk in img_response.iter_content(chunk_size=1024):
                                if chunk:
                                    handler.write(chunk)
                        
                        print(f'Downloaded {img_name}')
                    else:
                        print(f'Failed to download image from {img_url}. Status code: {img_response.status_code}')
            
            
            
        else:
            print("The specified div was not found in the HTML.")
            
        #summary__content show-more active
        
        
        
        
        mainPath = f'manga/{validDirName(title)}'

                    # Making the description category

        div = soup.find('div', class_='description-summary')
        if div:
            # Find all paragraph tags within the div
            paragraphs = div.find_all('p')

            # Extract the text from each paragraph and join them together with two new lines between paragraphs
            content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
            
            # Print the content to the console
            print(content)

            # Create the directory if it does not exist
            os.makedirs(mainPath, exist_ok=True)

            # Write the content to a text file
            file_path = os.path.join(mainPath, 'description.txt')
            with open(file_path, 'w', encoding='utf-8') as descFile:
                descFile.write(content)
            
        else:
            print("The specified div was not found in the HTML.")
        
        # making id file
        with open(f'{mainPath}/id.txt', 'w+') as id_file:
            id_file.write(count_directories())
            id_file.close()
            
        return link_urls, title
       
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

#summary_image


def webScrape(url, title):
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }

    # Make a request to the webpage
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the container with the specific class
        container = soup.find(class_='reading-content')
        
        os.makedirs(f'manga/{validDirName(title)}/Chapters', exist_ok=True)
        
        
        
        chapterName = soup.find('h1', id='chapter-heading').text.strip()
        if chapterName:
            print(chapterName)
            if title in chapterName:
                chapterName = chapterName[len(title)+3:]
            print(chapterName)
        
        if os.path.exists(f"manga/{validDirName(title)}/Chapters/{chapterName}"):
            print(f"Chapter {chapterName} already exists.")
            return
        
        # If the container exists, find all image tags inside it
        if container:
            img_tags = container.find_all('img')
            
            # Directory to save images
            os.makedirs(f'manga/{validDirName(title)}/Chapters/{chapterName}', exist_ok=True)
            
            # Loop through all img tags and download the images
            for i, img in enumerate(img_tags, start=1):
                img_url = img.get('src')
                
                # Ensure the image URL is absolute
                img_url = urljoin(url, img_url)
                
                # Make sure the img tag has a 'src' attribute
                if img_url:
                    print(f'Found image URL: {img_url}')
                    
                    # Download the image using stream to handle large files
                    img_response = requests.get(img_url, headers=headers, stream=True)
                    
                    # Check if the request was successful
                    if img_response.status_code == 200:
                        # Get the image file name and extension
                        img_extension = os.path.splitext(img_url)[1]  # Get the extension from the URL
                        img_name = os.path.join(f'manga/{validDirName(title)}/Chapters/{chapterName}', f'image_{i}{img_extension}')
                        
                        # Open a file for writing the binary data
                        with open(img_name, 'wb') as handler:
                            # Write the image in chunks to avoid high memory usage
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

def main(url):
    links, title = print_links_in_reverse_order(url)

    for link in links:
        webScrape(url=link, title=title)
    

if __name__ == '__main__':
    url = input("Enter URL: ")
    main(url)


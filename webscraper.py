import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# URL of the page to scrape
url = 'https://www.mangaread.org/manga/the-beginning-after-the-end/chapter-1-the-end-of-the-tunnel/'


def webScrape(url):
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
        
        # If the container exists, find all image tags inside it
        if container:
            img_tags = container.find_all('img')
            
            # Directory to save images
            os.makedirs('downloaded_images', exist_ok=True)
            
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
                        img_name = os.path.join('downloaded_images', f'image_{i}{img_extension}')
                        
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

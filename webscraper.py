import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# URL of the page to scrape
url = 'https://chapmanganato.to/manga-nb990510/chapter-1'

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
    container = soup.find(class_='container-chapter-reader')
    
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
                
                # Download the image
                img_data = requests.get(img_url, headers=headers).content
                
                # Get the image file name
                img_extension = os.path.splitext(img_url)[1]  # Get the extension from the URL
                img_name = os.path.join('downloaded_images', f'image_{i}{img_extension}')
                
                # Write the image to the file
                with open(img_name, 'wb') as handler:
                    handler.write(img_data)
                    
                print(f'Downloaded {img_name}')
    else:
        print("The specified class was not found in the HTML.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
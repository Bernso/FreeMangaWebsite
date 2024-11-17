import os
import requests
import shutil
import tempfile
import zipfile
from time import sleep

GITHUB_REPO = "https://github.com/Bernso/FreeMangaWebsite"
GITHUB_ZIP = f"{GITHUB_REPO}/archive/main.zip"

def download_repo():
    try:
        print("Downloading latest version...")
        response = requests.get(GITHUB_ZIP)
        response.raise_for_status()
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "repo.zip")
            
            # Save the zip file
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Get the extracted folder name
            extracted_folder = None
            for item in os.listdir(temp_dir):
                if os.path.isdir(os.path.join(temp_dir, item)) and item != '__MACOSX':
                    extracted_folder = item
                    break
            
            if not extracted_folder:
                raise Exception("Could not find extracted repository folder")
            
            source_dir = os.path.join(temp_dir, extracted_folder)
            
            # Copy files to current directory
            update_files(source_dir, os.getcwd())
            
        print("Update completed successfully!")
        sleep(2)
        return True
        
    except Exception as e:
        print(f"Error during update: {e}")
        input("Press Enter to continue...")
        return False

def update_files(src_dir, dst_dir):
    # Files/folders to preserve
    preserve = {'manga', '.env', '.git', '.gitignore', '__pycache__', '.idea'}
    
    # Copy all files and folders except preserved ones
    for item in os.listdir(src_dir):
        if item in preserve:
            continue
            
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        elif os.path.isdir(src_path):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)

def main():
    print("Starting update process...")
    if download_repo():
        print("Update completed. Restarting application...")
        sleep(1)
        os.system("python app.py")
    else:
        print("Update failed.")

if __name__ == "__main__":
    main()
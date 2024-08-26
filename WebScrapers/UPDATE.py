try:
    import os
except ImportError:
    print("The required module 'os' is not installed.")
    exit(1)

MANGA_DIR = os.path.join(os.getcwd(), "manga")

def get_manga_from_id(id: str):
    if os.path.isdir(MANGA_DIR):
        # Iterate over each folder in the "manga" directory
        for folder in os.listdir(MANGA_DIR):
            folder_path = os.path.join(MANGA_DIR, folder)
            if os.path.isdir(folder_path):  # Make sure it's a directory
                try:
                    with open(f"{folder_path}/id.txt", 'r', encoding='utf-8') as f:
                        folderID = f.read()
                        f.close()
                        if folderID == str(id):
                            #print(f"folder with id {folderID} found")
                    
                            with open(f"{folder_path}/website.txt", 'r', encoding='utf-8') as originFile:
                                origin = originFile.read()
                                #print(f"Found: {origin}")
                                originFile.close()
                                
                                
                                return folder, origin
                except Exception as e:
                    print(f"Error found: {e}")
                #print(f"{folder} Found")
    else:
        print(f"The path '{MANGA_DIR}' is not a valid directory")
        quit()
    


def manhwaClanDotCom_UrlBuilder(folder):
    manhwaTitle = folder.lower()
    manhwaTitle = manhwaTitle.replace(" ", "-")
    return f"https://www.manhwaclan.com/manga/{manhwaTitle}/"

def mangaDotCom_UrlBuilder(folder):
    manhwaTitle = folder.lower()
    manhwaTitle = manhwaTitle.replace(" ", "-")
    return f"https://mangaread.org/manga/{manhwaTitle}/"


def main(id):
    folder, origin = get_manga_from_id(id)
    if folder:
        print(f"Manga with ID {id} from {origin} found: {folder}")
        if origin.lower() == "readberserkdotcom":
            try:
                import WebScrapers.OnSite.readBerserkDotCom
                WebScrapers.OnSite.readBerserkDotCom.main()
                print(f"Successfully updated {folder}")
            except Exception as e:
                print(f"Error while scraping readBerserkDotCom: {e}")
        
        elif origin.lower() == "manhwaclandotcom":
            try:
                url = manhwaClanDotCom_UrlBuilder(folder=folder)
                import WebScrapers.OnSite.manhwaClanDotCom
                WebScrapers.OnSite.manhwaClanDotCom.main(url=url)
                print(f"Successfully updated {folder}")
            except Exception as e:
                print(f"Error while scraping manhwaClanDotCom: {e}")
        
        elif origin.lower() == "mangareaderdotorg":
            try:
                url = mangaDotCom_UrlBuilder(folder=folder)
                import WebScrapers.OnSite.mangaReaderDotOrg
                WebScrapers.OnSite.mangaReaderDotOrg.main(url=url)
                print(f"Successfully updated {folder}")
            except Exception as e:
                print(f"Error while scraping mangaReaderDotOrg: {e}")
        
        else:
            print(f"Error updating while finding origin: {origin}")
    else:
        print(f"Manga with ID {id} not found")

if __name__ == '__main__':
    main("2")
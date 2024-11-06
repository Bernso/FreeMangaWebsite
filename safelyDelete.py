import os
import shutil

def delete_manga(manga_id):
    manga_folder = "manga"
    manga_to_delete = None

    # Find the manga folder to delete
    for manga_folder_name in os.listdir(manga_folder):
        manga_folder_path = os.path.join(manga_folder, manga_folder_name)
        if os.path.isfile(os.path.join(manga_folder_path, "id.txt")):
            with open(os.path.join(manga_folder_path, "id.txt"), "r") as f:
                id = int(f.read().strip())
                if id == manga_id:
                    manga_to_delete = manga_folder_path
                    break

    if manga_to_delete is None:
        print("Manga with ID", manga_id, "not found.")
        return

    # Delete the manga folder
    for filename in os.listdir(manga_to_delete):
        file_path = os.path.join(manga_to_delete, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path, ignore_errors=True)
    # Delete subdirectories recursively

    # Now delete the empty manga folder
    os.rmdir(manga_to_delete)

    # Update the IDs of the remaining manga
    for manga_folder_name in os.listdir(manga_folder):
        manga_folder_path = os.path.join(manga_folder, manga_folder_name)
        if os.path.isfile(os.path.join(manga_folder_path, "id.txt")):
            with open(os.path.join(manga_folder_path, "id.txt"), "r") as f:
                id = int(f.read().strip())
                if id > manga_id:
                    with open(os.path.join(manga_folder_path, "id.txt"), "w") as f:
                        f.write(str(id - 1))

# Example usage
manga_to_delete = int(input("Enter the id of the manga you want to delete: "))
delete_manga(manga_to_delete)
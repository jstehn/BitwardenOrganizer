import os
import shutil

class FolderOrganizer:
    def __init__(self, categories):
        self.categories = categories

    def create_folders(self, base_directory):
        for category in self.categories:
            folder_path = os.path.join(base_directory, category)
            os.makedirs(folder_path, exist_ok=True)

    def move_login_entry(self, login_entry, category, base_directory):
        source_path = login_entry.file_path
        destination_path = os.path.join(base_directory, category, login_entry.file_name)
        shutil.move(source_path, destination_path)
        login_entry.file_path = destination_path
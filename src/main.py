from bitwarden_processor import BitwardenProcessor
from nlp_categorizer import NLPCategorizer
from folder_organizer import FolderOrganizer

def main():
    # Specify the path to the Bitwarden export JSON file
    bitwarden_file_path = "path/to/bitwarden_export.json"

    # Initialize the BitwardenProcessor
    bitwarden_processor = BitwardenProcessor(bitwarden_file_path)

    # Extract login entries from the Bitwarden export JSON
    login_entries = bitwarden_processor.extract_login_entries()

    # Initialize the NLPCategorizer
    nlp_categorizer = NLPCategorizer()

    # Categorize websites using natural language processing
    categorized_websites = nlp_categorizer.categorize_websites(login_entries)

    # Initialize the FolderOrganizer
    folder_organizer = FolderOrganizer()

    # Create folders for each category and assign login entries to their respective folders
    folder_organizer.create_folders(categorized_websites)
    folder_organizer.assign_login_entries(login_entries)

if __name__ == "__main__":
    main()
# BitwardenOrganizer

This project is designed to analyze Bitwarden export JSON files, categorize websites using natural language processing, and organize login entries into folders based on their categories.

## Project Structure

```
BitwardenOrganizer
├── src
│   ├── main.py
│   ├── bitwarden_processor.py
│   ├── nlp_categorizer.py
│   └── folder_organizer.py
├── requirements.txt
├── .env
└── README.md
```

## Files

### `src/main.py`

This file serves as the entry point of the application. It orchestrates the overall process of analyzing the Bitwarden export JSON, categorizing websites using natural language processing, and organizing the login entries into folders.

### `src/bitwarden_processor.py`

This file contains the `BitwardenProcessor` class, which is responsible for reading and parsing the Bitwarden export JSON file. It provides methods to extract login entries and their relevant information.

### `src/nlp_categorizer.py`

This file contains the `NLPCategorizer` class, which utilizes natural language processing techniques to categorize websites based on their names or URLs. It provides methods to analyze and categorize websites.

### `src/folder_organizer.py`

This file contains the `FolderOrganizer` class, which handles the creation of folders for each category and assigns the login entries to their respective folders. It provides methods to create folders and move login entries.

### `requirements.txt`

This file lists the dependencies required for the project. You can use it to install the necessary packages using a package manager like pip.

### `.env`

This file is used for environment variable configuration. It may contain sensitive information like API keys or credentials for Google Cloud services.

## Usage

1. Install the required dependencies listed in `requirements.txt` using a package manager like pip.

2. Set up the necessary environment variables in the `.env` file.

3. Run the `main.py` script to start the BitwardenOrganizer.

4. Follow the prompts and provide the path to the Bitwarden export JSON file.

5. The script will analyze the login entries, categorize the websites using natural language processing, and organize them into folders.

6. Check the output folders to find the organized login entries based on their categories.

```
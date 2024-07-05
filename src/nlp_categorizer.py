from typing import List, Dict
from google.cloud import language_v1
import requests
from collections import defaultdict
from urllib.parse import urlparse, urlunparse
import requests
from itertools import chain
from logger import configure_logger 

CAT_LOGGER = configure_logger("categorizer")

class NLPCategorizer:
    def __init__(self):
        # Initialize the Google Cloud NLP client
        self.client = language_v1.LanguageServiceClient()
        self.categories = defaultdict(list)

        # All entries by their ID and their website URL
        self.entries: Dict[str, list] = defaultdict(lambda: "")

    def categorize_websites(self) -> List[str]:
        for id, websites in self.entries.items():
            if not websites:
                # Skip if there are no websites
                continue
            base_urls = set(self.get_base_url(website) for website in websites)
            website_content = ""
            for website in chain(base_urls, websites):
                website_content = "\n".join(
                    (website_content, self.fetch_website_content(website))
                )
            # Use the classifyText method to categorize the content
            if not website_content:
                # Skip if there is no content
                continue
            CAT_LOGGER.info(f"Classifying content for ID: {id}")
            response = self.client.classify_text(document=website_content)
            # Assuming one category per website for simplicity
            if response.categories:
                category = max(
                    response.categories, key=lambda x: x.confidence
                ).name
                # Get the name of the base category                
                category = category.split("/")[1]
                CAT_LOGGER.info(f"{id} classification: {category}")
                self.categories[category].append(id)
            else:
                CAT_LOGGER.info(f"No categories found for ID: {id}")
        return self.categories

    def get_base_url(self, website_url: str) -> str:
        website_url = self.add_url_scheme(website_url)
        parsed_url = urlparse(website_url)
        # Construct the base URL using the scheme and netloc
        return f"{parsed_url.scheme}://{parsed_url.netloc}"

    def add_url_scheme(self, website_url: str) -> str:
        """Adds http:// to the URL if a scheme is missing."""
        if not website_url.startswith(("http://", "https://")):
            website_url = "http://" + website_url
        return website_url

    def clean_url(self, website_url: str) -> str:
        """Cleans the URL and removes any query parameters."""
        website_url = self.add_url_scheme(website_url)
        parsed_url = urlparse(website_url)
        # Remove any query parameters from the URL
        cleaned_url = parsed_url._replace(query="").geturl()
        cleaned_url = urlunparse(cleaned_url)
        return cleaned_url

    def fetch_website_content(self, website_url: str) -> str:
        try:
            # Check if the URL starts with http:// or https://
            website_url = self.clean_url(website_url)
            # Set the user agent to a modern version of Google Chrome
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
            }
            # Send a GET request to the cleaned website URL with the specified headers
            response = requests.get(website_url, headers=headers)
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()
            # Return the raw HTML content of the page
            return response.text
        except requests.RequestException as e:
            # Handle any errors that occur during the request
            CAT_LOGGER.error(f"An error occurred: {e}")
            return ""

    def classify_html(
        self, html_content: str
    ) -> List[language_v1.ClassificationCategory]:
        """
        Classifying Content in a String

        Args:
        text_content The text content to analyze.
        """

        type_ = language_v1.Document.Type.HTML
        document = {"content": html_content, "type_": type_}

        content_categories_version = (
            language_v1.ClassificationModelOptions.V2Model.ContentCategoriesVersion.V2
        )
        response = self.client.classify_text(
            request={
                "document": document,
                "classification_model_options": {
                    "v2_model": {
                        "content_categories_version": content_categories_version
                    }
                },
            }
        )
        # Loop through classified categories returned from the API
        response.categories = sorted(
            response.categories, key=lambda x: x.confidence, reverse=True
        )
        for category in response.categories:
            # Get the name of the category representing the document.
            # See the predefined taxonomy of categories:
            # https://cloud.google.com/natural-language/docs/categories
            CAT_LOGGER.debug(f"Category name: {category.name}")
            # Get the confidence. Number representing how certain the classifier
            # is that this category represents the provided text.
            CAT_LOGGER.debug(f"Confidence: {category.confidence}")

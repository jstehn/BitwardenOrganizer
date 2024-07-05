from typing import List
from google.cloud import language_v1
import requests
from collections import defaultdict


class NLPCategorizer:
    def __init__(self):
        # Initialize the Google Cloud NLP client
        self.client = language_v1.LanguageServiceClient()
        self.categories = defaultdict(list)

    def categorize_websites(self, websites: List[str]) -> List[str]:
        for website in websites:
            # Placeholder for fetching website content
            website_content = self.fetch_website_content(website)
            # Use the classifyText method to categorize the content
            response = self.client.classify_text(document=website_content)
            # Assuming one category per website for simplicity            
            if response.categories:
                category = max(response.categories, key=lambda x: x.confidence).name
                category = category.split("/")[1]
                self.categories[category].append(website)
        return self.categories

    def fetch_website_content(self, website_url: str) -> str:
        try:
            # Set the user agent to a modern version of Google Chrome
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
            }
            # Send a GET request to the website URL with the specified headers
            response = requests.get(website_url, headers=headers)
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()
            # Return the raw HTML content of the page
            return response.text
        except requests.RequestException as e:
            # Handle any errors that occur during the request
            print(f"An error occurred: {e}")
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
            print(f"Category name: {category.name}")
            # Get the confidence. Number representing how certain the classifier
            # is that this category represents the provided text.
            print(f"Confidence: {category.confidence}")

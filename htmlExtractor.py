import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import shutil
from PIL import Image
from io import BytesIO


class ImageDownloader:
    def __init__(self):
        self.driver = None

    def setup_driver(self, url):
        # Set up Selenium WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def create_folder(self, folder_name):
        # Clear the folder if it already exists
        if os.path.exists(folder_name):
            for file_name in os.listdir(folder_name):
                file_path = os.path.join(folder_name, file_name)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        else:
            os.makedirs(folder_name)

    def extract_images(self, exclude_keywords=("icon",)):
        """Extract all image URLs from the HTML content using BeautifulSoup, with filters."""
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        images = soup.find_all("img")
        img_urls = [
            img["src"]
            for img in images
            if "src" in img.attrs
            and not any(keyword in img["src"] for keyword in exclude_keywords)
        ]
        return img_urls

    def filter_image_by_size(self, img_data, min_size=(0, 0)):
        """Filter images based on size using Pillow."""
        try:
            img = Image.open(BytesIO(img_data))
            width, height = img.size
            print(f"Image size: {width}x{height}")  # Debugging info
            return width >= min_size[0] and height >= min_size[1]
        except Exception as e:
            print(f"Failed to check image size: {e}")
            return False

    def extract_text(self):
        """Extract all text content from the HTML and return it as a string."""
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return text

    def save_text_to_file(self, text, file_name="article.txt"):
        """Save the extracted text to a .txt file."""
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Text saved to {file_name}")

    def image_download(
        self,
        url,
        folder_name="imagesCache",
        valid_extensions=(".png", ".jpeg"),
        exclude_keywords=("icon",),
        min_size=(0, 0),  # Min width and height
    ):
        # Set up the driver and navigate to the URL
        self.setup_driver(url)

        # Create the folder to save images
        self.create_folder(folder_name)

        # Extract all image URLs from the page
        img_urls = self.extract_images(exclude_keywords=exclude_keywords)

        # Download and save each image
        for i, img_url in enumerate(img_urls):
            # Handle cases where src might be empty or None
            if not img_url:
                continue

            # Only download images that end with the specified extensions
            if img_url.endswith(valid_extensions):
                try:
                    # Get the image content
                    response = requests.get(img_url, stream=True)
                    img_data = response.content
                    print(f"Downloading image from {img_url}")  # Debugging info

                    # Check the image size
                    if not self.filter_image_by_size(img_data, min_size):
                        print(f"Skipped image due to size: {img_url}")
                        continue

                    img_extension = img_url.split(".")[-1].split("?")[
                        0
                    ]  # Remove query parameters
                    img_name = os.path.join(folder_name, f"image_{i+1}.{img_extension}")

                    # Save the image
                    with open(img_name, "wb") as img_file:
                        img_file.write(img_data)
                    print(f"Downloaded: {img_name}")
                except Exception as e:
                    print(f"Failed to download {img_url}: {e}")

        # Save the extracted text to a file
        text = self.extract_text()
        self.save_text_to_file(text)

        # Close the browser
        self.driver.quit()

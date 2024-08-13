import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class HTMLExtractor:
    def __init__(self):
        self.driver = None

    def setup_driver(self, url):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize the WebDriver
        self.driver = webdriver.Chrome()

        # Navigate to the URL
        self.driver.get(url)

    def extract_html(self):
        # Return the full HTML content of the page
        return self.driver.page_source

    def get_html(self, url):
        # Set up the driver and navigate to the URL
        self.setup_driver(url)

        # Extract the HTML content
        html_content = self.extract_html()

        # Close the browser
        self.driver.quit()

        return html_content

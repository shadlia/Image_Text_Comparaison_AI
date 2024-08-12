import os
import requests


class ShutterstockImageFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.shutterstock.com/v2/images/search"

    def fetch_images(self, query, per_page=10):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        params = {
            "query": query,
            "per_page": per_page,
        }
        response = requests.get(self.base_url, headers=headers, params=params)

        if response.status_code == 200:
            images = response.json()["data"]
            return [image["assets"]["preview"]["url"] for image in images]
        else:
            print(f"Failed to fetch images: {response.status_code}")
            return []

    def download_images(self, image_urls, folder_name="shutterstock_images"):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for i, img_url in enumerate(image_urls):
            img_data = requests.get(img_url).content
            img_name = os.path.join(folder_name, f"image_{i+1}.jpg")
            with open(img_name, "wb") as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {img_name}")


# Example usage
if __name__ == "__main__":
    api_key = "v2/VjFRZDhpQVdMWjhTc1JlcTJHZ3R6N3FwNUc4QUtBMFovNDM4MTE1NzgxL2N1c3RvbWVyLzQvMlhYYkQzdW1OMVRWdTFWUUFuVXlGeTJfdGJfUHQwU0VLLVFZQnNKaUdBSkp3QlFzZGxtX0doR0h6WjNadXFMTnhfTDJoMzhOdUtvS2c3TWtyaG9pd2FfdW5lOXQxWUtqbzhtTG0yVUFYTXhVMGVvbHQtVC13d1ZYdjBseG9DSEMwRTBZYjlDcTZPNWNhMFdQc1Z5Q18zbThXWDlMYnJ0eW5qWExQM05jU0x6M2IyZ2FwVU5iUVNDUTdMSU1ma3c5eTFsZFRGZ18wMkg1UE10cjV0N2prdy9hZWVEQ0NaRkE1U1RLbGxGek1tbml3"
    fetcher = ShutterstockImageFetcher(api_key)

    topic = "Donald trump"
    image_urls = fetcher.fetch_images(query=topic, per_page=5)
    fetcher.download_images(image_urls)

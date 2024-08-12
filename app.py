import os
import time
from htmlExtractor import ImageDownloader
from ImageTextComparator import ImageTextComparator


def are_images_downloaded(folder_name, valid_extensions):
    """Check if images have been downloaded in the specified folder."""
    files = os.listdir(folder_name)
    return any(file.lower().endswith(valid_extensions) for file in files)


def main():
    url = "https://www.purepeople.com/article/gabriel-attal-retrouve-son-ex-aux-jo-de-paris-une-celebre-chanteuse-avec-qui-il-a-garde-une-jolie-proximite-video_a525751/1"
    folder_name = "imagesCache"
    valid_extensions = (".png", ".jpeg", ".jpg", ".gif")

    # Create an instance of ImageDownloader
    downloader = ImageDownloader()

    # Call the image_download function
    downloader.image_download(
        url,
        folder_name,
        valid_extensions,
        exclude_keywords=("icon",),
        min_size=(100, 100),  # Minimum width and height
    )

    # Wait until images are downloaded
    while not are_images_downloaded(folder_name, valid_extensions):
        print("Waiting for images to be downloaded...")
        time.sleep(5)  # Wait for 5 seconds before checking again

    # Set up API key and paths
    api_key = "AIzaSyCfT12LpddN3ZNmYffPiTwEwp-WiKkILMo"
    text_file_path = "article.txt"
    comparator = ImageTextComparator(api_key)
    comparator.generate_response(text_file_path, folder_name)

    """# Create an instance of the comparator
        comparator = ImageTextComparator(api_key)

        # Compare images with text
        response_text = comparator.image_download_and_compare(text_file_path, folder_name)
        print(response_text)

    """


if __name__ == "__main__":
    main()

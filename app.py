import os
import time
from htmlExtractor import ImageDownloader
from ImageTextComparator import ImageTextComparator
from HTMLextractor import HTMLExtractor
from modelExtraction import ArticleExtractor


def are_images_downloaded(folder_name, valid_extensions):
    """Check if images have been downloaded in the specified folder."""
    files = os.listdir(folder_name)
    return any(file.lower().endswith(valid_extensions) for file in files)


def main():
    url = "https://www.purepeople.com/article/en-plein-divorce-avec-luana-paul-belmondo-partage-un-beau-moment-avec-leur-fils-victor-et-l-immortalise-en-photo_a526200/1"
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
    # ---------------------------------------------------------------------------------------------------#
    """    api_key = "AIzaSyCfT12LpddN3ZNmYffPiTwEwp-WiKkILMo"
    text_file_path = "article.txt"
    comparator = ImageTextComparator(api_key)
    comparator.generate_response(text_file_path, folder_name)
    
    # Create an instance of the comparator
        comparator = ImageTextComparator(api_key)

        # Compare images with text
        response_text = comparator.image_download_and_compare(text_file_path, folder_name)
        print(response_text)

    """
    # -------------------------------------------------------------------------------------------------------------#
    html_extractor = HTMLExtractor()
    print("-------------------extracting HTML------------------...")
    html_content = html_extractor.get_html(url)
    print(html_content)
    print("---------------END EXTRACTING HTML-----------------------")
    llm = ArticleExtractor()
    llm.extract_content(html_content=html_content, image_folder_path=folder_name)


if __name__ == "__main__":
    main()

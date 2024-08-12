import os
import google.generativeai as genai

from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.multi_modal_llms.generic_utils import load_image_urls
from llama_index.core import SimpleDirectoryReader
import time
from threading import Thread


class ImageTextComparator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
        )

    def upload_to_gemini(self, path, mime_type=None):
        """Uploads the given file to Gemini."""
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    def get_text_from_file(self, file_path):
        """Reads text from a file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Text file not found: {file_path}")
        with open(file_path, "r") as file:
            return file.read()

    def image_download_and_compare(self, text_file_path, image_folder_path):
        """Upload images and text, then compare using Gemini."""
        # Read the text from the file
        try:
            text = self.get_text_from_file(text_file_path)
        except Exception as e:
            print(f"Error reading text file: {e}")
            return

        # Upload all images from the folder
        files = []
        if not os.path.exists(image_folder_path):
            raise FileNotFoundError(f"Image folder not found: {image_folder_path}")

        for img_name in os.listdir(image_folder_path):
            img_path = os.path.join(image_folder_path, img_name)
            if os.path.isfile(img_path) and img_name.lower().endswith(
                (".png", ".jpeg", ".jpg")
            ):
                mime_type = (
                    "image/jpeg"
                    if img_name.lower().endswith((".jpeg", ".jpg"))
                    else "image/png"
                )
                try:
                    file = self.upload_to_gemini(img_path, mime_type=mime_type)
                    files.append(file)
                except Exception as e:
                    print(f"Error uploading file {img_path}: {e}")

        if not files:
            print("No valid images were uploaded.")
            return

        # Define the prompt with the text and image URIs
        prompt = (
            "I have the following text and images. Please determine if the images are related to the text and explain how. "
            f"Text: {text} "
            "Images: " + ", ".join([f.uri for f in files])
        )
        print(files)
        # Start the chat session with a custom prompt
        try:
            chat_session = self.model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [
                            prompt,
                        ],
                    }
                ]
            )

            # Send a message and get the response
            response = chat_session.send_message(
                "Are these images contextually related to the text?"
            )
            return response.text
        except Exception as e:
            print(f"Error during chat session: {e}")
            return

    def generate_response(self, text_file_path, image_folder_path):
        # load image documents from local directory
        image_documents = SimpleDirectoryReader(image_folder_path).load_data()

        mm_llm = GeminiMultiModal(
            model_name="models/gemini-1.5-flash",
            api_key="AIzaSyCfT12LpddN3ZNmYffPiTwEwp-WiKkILMo",
        )
        # Read the text from the file
        try:
            text = self.get_text_from_file(text_file_path)
        except Exception as e:
            print(f"Error reading text file: {e}")
            return

        start = time.time()
        prompt = (
            "I have the following text and images. Please determine if the images are related to the text and explain how. "
            f"Text: {text} "
        )
        response = mm_llm.complete(prompt=prompt, image_documents=image_documents).text
        end = time.time()
        print(f"Response: {response}")

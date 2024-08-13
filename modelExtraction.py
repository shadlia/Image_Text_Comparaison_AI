import google.generativeai as genai

from llama_index.multi_modal_llms.gemini import GeminiMultiModal

from llama_index.core import SimpleDirectoryReader


class ArticleExtractor:

    def extract_content(self, html_content, image_folder_path):
        # Define the prompt to send to the LLM
        prompt = (
            "As an expert in analyzing articles for speech synthesis, your task is to extract and structure the text of the article. REMOVE ALL  the HTML BALISES like href or <a> or anything start with < , i want it to be only Text to read like News and make sure each picture is related to the context of its paraphraph"
            "Please split the text into paragraphs and identify the picture from the site that is most related to each paragraph. "
            "Make sure each paragraph is readable and understandable when its read as a speech in news "
            "The response should be formatted as follows:\n\n"
            "[Paragraph 1: <Text of paragraph 1> : Picture related to it: <URL of picture 1> , "
            "Paragraph 2: <Text of paragraph 2> : Picture related to it: <URL of picture 2>, ...]\n\n"
            "Keep the text in its original French language.\n\n"
            f"HTML Content:\n{html_content}"
        )

        mm_llm = GeminiMultiModal(
            model_name="models/gemini-1.5-flash",
            api_key="AIzaSyCfT12LpddN3ZNmYffPiTwEwp-WiKkILMo",
        )
        image_documents = SimpleDirectoryReader(image_folder_path).load_data()

        response = mm_llm.complete(prompt=prompt, image_documents=image_documents)
        print(response)
        with open("lll_reponse.txt", "w", encoding="utf-8") as file:
            file.write(str(response))
        return response

    # Define the prompt to send to the LLM

import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash"
        )

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set in the .env file."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str
    ) -> str:

        prompt = f"""
You are a professional legal document drafting assistant.

Create a clear and professionally structured {document_type}.

Document Type:
{document_type}

Parties:
{parties}

Key Terms:
{terms}

Effective Date:
{effective_date}

Instructions:
1. Create a professional legal document.
2. Use clear headings and sections.
3. Include the provided parties, terms, and effective date.
4. Do not invent important personal or legal information.
5. Use placeholders where necessary information is missing.
6. Make the document easy to read and edit.
7. Return only the document content.
"""

        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )

                generated_text = response.text

                if not generated_text:
                    raise ValueError(
                        "Gemini returned an empty response."
                    )

                return generated_text.strip()

            except Exception as error:
                error_message = str(error)

                if "503" in error_message or "UNAVAILABLE" in error_message:
                    if attempt < max_attempts - 1:
                        time.sleep(2 ** attempt)
                        continue

                raise error
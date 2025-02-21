from openai import OpenAI
from PyPDF2 import PdfReader
import json
from django.conf import settings
import os
from .models import Education, Resume, Experience

# Initialize OpenAI API
def get_openai_api_key():
    try:
        with open(os.path.join(settings.BASE_DIR, 'openai_key.txt'), 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading API key: {e}")
        return None

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def parse_resume(file_path):
    try:
        resume_text = extract_text_from_pdf(file_path)
        api_key = get_openai_api_key()
        if not api_key:
            return "API key not found."

        client = OpenAI(
            api_key=api_key
        )

        user_message = f"""Give the extact details and only degrees in eductaion, company worked for experience with years, main skills like 'name': '',
        'email': '',
        'phone': '',
        'skills': [],
        'education': '',
        'experience': '' Name:, Education, Skills, from the resume: Name, Email, Phone, Skills, Education, Experience. In education fields are degree, specialization, institution and year, In experience give position, company and years \n\nResume Text: {resume_text}"""

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        bottext = completion.choices[0].message.content.strip()
        trimmed_str = bottext.replace('```json\n', '').replace('```', '')
        resume_dict = json.loads(trimmed_str.strip())
        return resume_dict
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"Error during resume parsing: {e}")
        return None

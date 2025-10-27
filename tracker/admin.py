from django.contrib import admin
from .models import JobApplication
import fitz  # PyMuPDF
import os
from django.conf import settings
from dotenv import load_dotenv
import requests
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

@admin.action(description="Generate Resume Feedback (Dolphin Mistral via OpenRouter)")
def generate_resume_feedback(modeladmin, request, queryset):
    for obj in queryset:
        if obj.resume:
            file_path = os.path.join(settings.MEDIA_ROOT, obj.resume.name)
            print("File path:", file_path)  # DEBUG

            resume_text = extract_text_from_pdf(file_path)
            print("Extracted text length:", len(resume_text))  # DEBUG

            prompt = f"""You are a professional resume coach.
Please provide clear, specific, and actionable feedback to improve the following resume:

Resume:
{resume_text}
"""

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }

            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(data)
                )

                if response.status_code == 200:
                    result = response.json()
                    feedback_text = result["choices"][0]["message"]["content"].strip().replace("\n", "\n\n")
                    print("FEEDBACK:", feedback_text)
                    obj.feedback = feedback_text
                    obj.save()
                else:
                    print(f"Failed API call: {response.status_code}\n{response.text}")

            except Exception as e:
                import traceback
                print(f"Error generating feedback for JobApplication ID {obj.id}:\n{traceback.format_exc()}")

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "resume", "feedback")
    fields=("position", "resume", "feedback")
    actions = [generate_resume_feedback]
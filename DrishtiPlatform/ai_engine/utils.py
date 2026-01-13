import random
import os
from django.conf import settings
from openai import OpenAI

# Initialize OpenAI client with OpenRouter configuration
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
    default_headers={
        "HTTP-Referer": "https://drishti-platform.com",
        "X-Title": "Drishti Platform",
    }
)

def predict_category(text):
    """
    Predict category using OpenRouter API.
    Supports 6 Categories: Water Supply, Roads & Transport, Sanitation, Electricity, Traffic, Public Safety.
    """
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", # Use a cost-effective model available on OpenRouter
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant for a civic grievance platform. Categorize the following complaint into EXACTLY one of these categories: 'Water Supply', 'Roads & Transport', 'Sanitation', 'Electricity', 'Traffic', 'Public Safety'. If it doesn't fit well, use 'General'. Return ONLY the category name."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        category = completion.choices[0].message.content.strip()
        
        # Validate category
        valid_categories = ['Water Supply', 'Roads & Transport', 'Sanitation', 'Electricity', 'Traffic', 'Public Safety', 'General']
        if category not in valid_categories:
            # Fallback if AI returns something else
            return 'General', 0.50
            
        return category, 0.90 # Mock confidence for now as API doesn't always give it easily without logprobs
    except Exception as e:
        print(f"Error in predict_category: {e}")
        # Fallback to keyword matching if API fails
        text = text.lower()
        if 'water' in text or 'leak' in text or 'pipe' in text:
            return 'Water Supply', 0.85
        elif 'road' in text or 'pothole' in text:
            return 'Roads & Transport', 0.80
        elif 'garbage' in text or 'trash' in text:
            return 'Sanitation', 0.90
        elif 'light' in text or 'electricity' in text:
            return 'Electricity', 0.88
        elif 'traffic' in text:
            return 'Traffic', 0.85
        elif 'safety' in text or 'crime' in text:
            return 'Public Safety', 0.92
        else:
            return 'General', 0.50

def predict_priority(text, category):
    """
    Predict priority using OpenRouter API.
    """
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant. Determine the priority of this complaint based on urgency and potential danger. Return ONLY one of: 'low', 'medium', 'high', 'critical'."
                },
                {
                    "role": "user",
                    "content": f"Category: {category}\nComplaint: {text}"
                }
            ]
        )
        priority = completion.choices[0].message.content.strip().lower()
        
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if priority not in valid_priorities:
            return 'medium', 0.70
            
        return priority, 0.85
    except Exception as e:
        print(f"Error in predict_priority: {e}")
        # Fallback
        text = text.lower()
        if 'urgent' in text or 'danger' in text or 'fire' in text:
            return 'critical', 0.95
        elif 'blocked' in text or 'broken' in text:
            return 'high', 0.80
        else:
            return 'medium', 0.70

def suggest_department(category_name):
    """
    Suggest department based on category.
    """
    if category_name == 'Water Supply':
        return 'Water Board'
    elif category_name == 'Roads & Transport':
        return 'Public Works'
    elif category_name == 'Sanitation':
        return 'Sanitation Dept'
    elif category_name == 'Electricity':
        return 'Public Works' # Or Electricity Board if it existed
    elif category_name == 'Traffic':
        return 'Traffic Police'
    elif category_name == 'Public Safety':
        return 'Police Dept'
    else:
        return 'General Administration'

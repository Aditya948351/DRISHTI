import random

def predict_category(text):
    """
    Mock AI function to predict category based on keywords.
    """
    text = text.lower()
    if 'water' in text or 'leak' in text or 'pipe' in text:
        return 'Water Supply', 0.85
    elif 'road' in text or 'pothole' in text or 'street' in text:
        return 'Roads & Transport', 0.80
    elif 'garbage' in text or 'trash' in text or 'clean' in text:
        return 'Sanitation', 0.90
    elif 'light' in text or 'dark' in text:
        return 'Streetlights', 0.88
    else:
        return 'General', 0.50

def predict_priority(text, category):
    """
    Mock AI function to predict priority.
    """
    text = text.lower()
    if 'urgent' in text or 'danger' in text or 'accident' in text or 'fire' in text:
        return 'critical', 0.95
    elif 'blocked' in text or 'broken' in text:
        return 'high', 0.80
    elif 'delay' in text:
        return 'medium', 0.70
    else:
        return 'low', 0.60

def suggest_department(category_name):
    """
    Mock AI function to suggest department based on category.
    """
    # In a real system, this would query the database or use a mapping
    # For now, we return a string that matches Department names we might create
    if category_name == 'Water Supply':
        return 'Water Department'
    elif category_name == 'Roads & Transport':
        return 'Roads Department'
    elif category_name == 'Sanitation':
        return 'Sanitation Department'
    elif category_name == 'Streetlights':
        return 'Electricity Department'
    else:
        return 'General Administration'

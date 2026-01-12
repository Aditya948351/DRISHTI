import random

def predict_category(text):
    """
    Mock AI function to predict category based on keywords.
    Supports 6 Categories: Water, Roads, Sanitation, Electricity, Traffic, Public Safety.
    """
    text = text.lower()
    if 'water' in text or 'leak' in text or 'pipe' in text or 'pressure' in text:
        return 'Water Supply', 0.85
    elif 'road' in text or 'pothole' in text or 'street' in text or 'construction' in text:
        return 'Roads & Transport', 0.80
    elif 'garbage' in text or 'trash' in text or 'clean' in text or 'dustbin' in text or 'drain' in text:
        return 'Sanitation', 0.90
    elif 'light' in text or 'dark' in text or 'wire' in text or 'pole' in text or 'electricity' in text:
        return 'Electricity', 0.88
    elif 'traffic' in text or 'signal' in text or 'jam' in text or 'parking' in text:
        return 'Traffic', 0.85
    elif 'safety' in text or 'crime' in text or 'theft' in text or 'suspicious' in text or 'animal' in text:
        return 'Public Safety', 0.92
    else:
        return 'General', 0.50

def predict_priority(text, category):
    """
    Mock AI function to predict priority.
    """
    text = text.lower()
    if 'urgent' in text or 'danger' in text or 'accident' in text or 'fire' in text or 'critical' in text or 'death' in text or 'spark' in text:
        return 'critical', 0.95
    elif 'blocked' in text or 'broken' in text or 'overflow' in text or 'no water' in text:
        return 'high', 0.80
    elif 'delay' in text or 'slow' in text or 'bad' in text:
        return 'medium', 0.70
    else:
        return 'low', 0.60

def suggest_department(category_name):
    """
    Mock AI function to suggest department based on category.
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

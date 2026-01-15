import spacy
import random

# Load SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if model is not found (e.g., during build)
    print("SpaCy model 'en_core_web_sm' not found. Please download it.")
    nlp = None

def predict_category(text):
    """
    Predict category using SpaCy NLP (Keyword & Similarity based).
    """
    if not nlp:
        return 'General', 0.50

    doc = nlp(text.lower())
    
    # Define keywords for each category
    categories = {
        'Water Supply': ['water', 'leak', 'pipe', 'supply', 'drinking', 'sewage', 'drain', 'tap'],
        'Roads & Transport': ['road', 'pothole', 'street', 'transport', 'bus', 'traffic', 'highway', 'pavement'],
        'Sanitation': ['garbage', 'trash', 'waste', 'dump', 'litter', 'dustbin', 'clean', 'smell'],
        'Electricity': ['light', 'electricity', 'power', 'pole', 'wire', 'current', 'voltage', 'lamp'],
        'Traffic': ['traffic', 'jam', 'signal', 'congestion', 'parking', 'vehicle'],
        'Public Safety': ['safety', 'crime', 'theft', 'danger', 'police', 'security', 'harassment']
    }

    scores = {cat: 0 for cat in categories}

    # Lemmatize and match keywords
    for token in doc:
        lemma = token.lemma_
        for cat, keywords in categories.items():
            if lemma in keywords:
                scores[cat] += 1

    # Find category with max score
    best_category = max(scores, key=scores.get)
    max_score = scores[best_category]

    if max_score > 0:
        # Calculate pseudo-confidence
        confidence = min(0.5 + (max_score * 0.1), 0.95)
        return best_category, confidence
    else:
        return 'General', 0.50

def predict_priority(text, category):
    """
    Predict priority using SpaCy NLP.
    """
    if not nlp:
        return 'medium', 0.70
        
    doc = nlp(text.lower())
    
    urgent_keywords = ['urgent', 'danger', 'critical', 'emergency', 'immediately', 'severe', 'accident', 'fire', 'threat']
    high_keywords = ['blocked', 'broken', 'heavy', 'serious', 'major', 'stuck']
    
    score = 0
    for token in doc:
        if token.lemma_ in urgent_keywords:
            score += 2
        elif token.lemma_ in high_keywords:
            score += 1
            
    if score >= 2:
        return 'critical', 0.90
    elif score == 1:
        return 'high', 0.80
    else:
        return 'medium', 0.70

def suggest_department(category_name):
    """
    Suggest department based on category.
    """
    mapping = {
        'Water Supply': 'Water Board',
        'Roads & Transport': 'Public Works',
        'Sanitation': 'Sanitation Dept',
        'Electricity': 'Electricity Board',
        'Traffic': 'Traffic Police',
        'Public Safety': 'Police Dept'
    }
    return mapping.get(category_name, 'General Administration')

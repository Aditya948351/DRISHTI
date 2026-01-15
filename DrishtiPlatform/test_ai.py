import os
import django
from django.conf import settings

# Configure Django settings manually for the script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

from ai_engine.utils import predict_category, predict_priority

def test_ai():
    print("Testing AI Categorization...")
    test_text = "There is a huge pothole on the main road causing traffic jams."
    print(f"Input: {test_text}")
    
    try:
        category, conf = predict_category(test_text)
        print(f"Predicted Category: {category} (Confidence: {conf})")
    except Exception as e:
        print(f"Categorization Failed: {e}")

    print("\nTesting AI Priority...")
    try:
        priority, conf = predict_priority(test_text, category)
        print(f"Predicted Priority: {priority} (Confidence: {conf})")
    except Exception as e:
        print(f"Priority Prediction Failed: {e}")

if __name__ == "__main__":
    test_ai()

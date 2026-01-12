import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

from django.contrib.auth.forms import UserCreationForm

form = UserCreationForm()
print("UserCreationForm Fields:")
for name in form.fields:
    print(f"- {name}")

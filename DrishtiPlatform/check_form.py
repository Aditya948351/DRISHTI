import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

from accounts.forms import UserRegistrationForm

form = UserRegistrationForm()
print("Form Fields:")
for name, field in form.fields.items():
    print(f"- {name}: {field.__class__.__name__} (required={field.required})")

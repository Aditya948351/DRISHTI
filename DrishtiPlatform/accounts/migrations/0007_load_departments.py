from django.db import migrations
from django.core.management import call_command

def load_fixture(apps, schema_editor):
    call_command('loaddata', 'departments.json')

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_load_officers'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]

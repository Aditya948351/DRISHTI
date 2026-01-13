from django.db import migrations
from django.core.management import call_command

def load_fixture(apps, schema_editor):
    call_command('loaddata', 'initial_data_officers.json')

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_load_data'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]

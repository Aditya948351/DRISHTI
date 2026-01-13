from django.db import migrations
from django.core.management import call_command

def load_fixture(apps, schema_editor):
    call_command('loaddata', 'initial_data.json')

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_points_user_rank'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]

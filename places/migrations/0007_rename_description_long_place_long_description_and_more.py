# Generated by Django 4.2.5 on 2023-10-08 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0006_alter_place_description_short'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='description_long',
            new_name='long_description',
        ),
        migrations.RenameField(
            model_name='place',
            old_name='description_short',
            new_name='short_description',
        ),
    ]

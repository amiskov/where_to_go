# Generated by Django 4.2.5 on 2023-10-08 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_alter_placeimage_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='description_short',
            field=models.CharField(max_length=256, verbose_name='Короткое описание'),
        ),
    ]

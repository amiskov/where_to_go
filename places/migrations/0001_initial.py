# Generated by Django 4.2.5 on 2023-09-18 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description_short', models.CharField(max_length=256)),
                ('description_long', models.TextField()),
                ('lat', models.DecimalField(decimal_places=14, max_digits=16)),
                ('lon', models.DecimalField(decimal_places=14, max_digits=16)),
            ],
        ),
    ]

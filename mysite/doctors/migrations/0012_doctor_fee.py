# Generated by Django 4.1.2 on 2023-05-16 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0011_rename_picture_specialties_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='fee',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 4.1.2 on 2023-06-05 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_remove_doctor_is_auth'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='is_auth',
            field=models.BooleanField(default=False),
        ),
    ]

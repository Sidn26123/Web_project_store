# Generated by Django 4.1.2 on 2023-05-12 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0008_doctor_position_doctor_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='income',
            field=models.FloatField(default=0),
        ),
    ]

# Generated by Django 4.1.2 on 2023-06-10 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0006_alter_doctor_time_per_appoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='bookable_time',
            field=models.TextField(default='[{"day":1,"time":[]},{"day":2,"time":[]},{"day":3,"time":[]},{"day":4,"time":[]},{"day":5,"time":[]}{"day":6,"time":[]},{"day":7,"time":[]}]'),
        ),
    ]

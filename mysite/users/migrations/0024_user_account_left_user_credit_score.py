# Generated by Django 4.1.2 on 2023-05-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_remove_user_time_join'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_left',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='credit_score',
            field=models.FloatField(default=0),
        ),
    ]

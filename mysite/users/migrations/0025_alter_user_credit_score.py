# Generated by Django 4.1.2 on 2023-05-25 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_user_account_left_user_credit_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='credit_score',
            field=models.IntegerField(default=100),
        ),
    ]

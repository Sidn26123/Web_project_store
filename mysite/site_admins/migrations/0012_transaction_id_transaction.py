# Generated by Django 4.1.2 on 2023-04-12 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_admins', '0011_transaction_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='id_transaction',
            field=models.IntegerField(default=1),
        ),
    ]

# Generated by Django 4.1.2 on 2023-05-19 20:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0028_alter_mypaient_last_time_alter_review_id_send'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypaient',
            name='last_time',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]

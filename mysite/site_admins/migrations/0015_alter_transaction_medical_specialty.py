# Generated by Django 4.1.2 on 2023-04-26 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0005_remove_specialties_id_alter_specialties_name'),
        ('site_admins', '0014_transaction_spec_alter_transaction_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='medical_specialty',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='doctors.specialties'),
        ),
    ]

# Generated by Django 4.1.2 on 2023-05-16 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_remove_patient_age'),
        ('doctors', '0013_doctor_money_left'),
        ('site_admins', '0024_alter_transaction_state_invoice_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='receiver_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='sender_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient'),
        ),
    ]

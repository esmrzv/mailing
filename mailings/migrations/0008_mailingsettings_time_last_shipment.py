# Generated by Django 4.2.13 on 2024-08-11 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0007_client_owner_mailingsettings_owner_message_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingsettings',
            name='time_last_shipment',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время последней отправки сообщения'),
        ),
    ]

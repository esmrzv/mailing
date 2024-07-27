# Generated by Django 4.2.13 on 2024-07-26 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0004_alter_log_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingsettings',
            name='end_time',
            field=models.DateTimeField(verbose_name='Время окончания рассылки'),
        ),
        migrations.AlterField(
            model_name='mailingsettings',
            name='start_time',
            field=models.DateTimeField(verbose_name='Время начала рассылки'),
        ),
    ]

# Generated by Django 4.2.13 on 2024-07-26 18:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0002_client_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='Тема', max_length=150, verbose_name='Тема письма')),
                ('body', models.TextField(default='Письмо', verbose_name='Тело письма')),
            ],
            options={
                'verbose_name': 'Письмо',
                'verbose_name_plural': 'Письма',
            },
        ),
        migrations.RemoveField(
            model_name='mailingsettings',
            name='text',
        ),
        migrations.RemoveField(
            model_name='mailingsettings',
            name='title',
        ),
        migrations.AlterField(
            model_name='log',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата и время последней попытки'),
        ),
        migrations.AlterField(
            model_name='mailingsettings',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время окончания рассылки'),
        ),
        migrations.AlterField(
            model_name='mailingsettings',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время начала рассылки'),
        ),
        migrations.AddField(
            model_name='mailingsettings',
            name='message',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mailings.message', verbose_name='письмо'),
            preserve_default=False,
        ),
    ]

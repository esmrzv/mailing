from django.db import models
from django.forms import EmailField
from django.utils import timezone

from users.models import User

NULLABLE = {
    'blank': True,
    'null': True
}


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name='email', unique=True, **NULLABLE)
    full_name = models.CharField(max_length=100, verbose_name='Полное имя')
    comment = models.TextField(verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(verbose_name='Тема письма', max_length=150, default='Тема')
    body = models.TextField(verbose_name='Тело письма', default='Письмо')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.subject} - {self.body}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingSettings(models.Model):
    DAILY = 'Раз в день'
    WEEKLY = 'Раз в неделю'
    MONTHLY = 'Раз в месяц'

    CREATED = 'Создана'
    STATED = 'Запушена'
    COMPLETED = 'Завершена'

    PERIODICITY = [
        (DAILY, 'Раз вдень'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        (COMPLETED, 'Завершена'),
        (CREATED, 'Создана'),
        (STATED, 'Запушена')
    ]

    start_time = models.DateTimeField(verbose_name='Время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Время окончания рассылки')
    periodicity = models.CharField(choices=PERIODICITY, max_length=50, verbose_name='Периодичность')
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, verbose_name='Статус')
    client = models.ManyToManyField(Client, verbose_name='Клиент')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='письмо')
    time_last_shipment = models.DateTimeField(verbose_name='время последней отправки сообщения', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return (f'time: {self.start_time} - {self.end_time}, periodicity: {self.periodicity},'
                f' status:{self.status}')

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройка рассылок'
        permissions = [
            ('change_status', 'Can change status'),
        ]


class Log(models.Model):
    time = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now=True)
    status = models.BooleanField(verbose_name='статус попытки')
    server_response = models.CharField(verbose_name='ответ почтового сервера', **NULLABLE)

    mailing_list = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент', **NULLABLE)
    comments = models.TextField(max_length=50, verbose_name='Комментарии', **NULLABLE)

    def __str__(self):
        return f'{self.time} {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'

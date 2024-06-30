from django.db import models
from django.forms import EmailField

NULLABLE = {
    'blank': True,
    'null': True
}


class Client(models.Model):
    email = EmailField(max_length=100)
    full_name = models.CharField(max_length=100, verbose_name='Полное имя')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


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
    title = models.CharField(max_length=100, verbose_name='Название темы')
    text = models.TextField(verbose_name='Письмо')
    client = models.ManyToManyField(Client, verbose_name='Клиент')

    def __str__(self):
        return (f'{self.title} time: {self.start_time} - {self.end_time}, periodicity: {self.periodicity},'
                f' status:{self.status}')

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройка рассылок'


class Log(models.Model):
    time = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    status = models.BooleanField(verbose_name='статус попытки')
    server_response = models.CharField(verbose_name='ответ почтового сервера', **NULLABLE)

    mailing_list = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент', **NULLABLE)

    def __str__(self):
        return f'{self.time} {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'


import smtplib
from datetime import datetime, timezone

import pytz
from django.conf import settings
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailings.models import Log, MailingSettings, Message, Client
from django.utils import timezone


def send_mailing():
    """
    :return:
    """
    sorted_mailings()  # Проверка статусов рассылки на актуальность
    checking_date()  # Отправка писем


def sorted_mailings():
    """
    Проверка статусов рассылки на актуальность
    """
    time_zone = pytz.timezone(settings.TIME_ZONE)
    time_now = datetime.now(time_zone)
    mailings = MailingSettings.objects.filter(status__in=['created', 'launched'])
    if len(mailings) > 0:
        for mailing in mailings:
            if mailing.status == 'CREATED' and mailing.start_time <= time_now:
                mailing.status = 'STATED'
                mailing.save()
            elif mailing.status == 'STATED' and mailing.end_time <= time_now:
                mailing.status = 'COMPLETED'
                mailing.save()


def checking_date():
    """
    Отправка писем
    """
    time_zone = pytz.timezone(settings.TIME_ZONE)
    time_now = datetime.now(time_zone)
    mailings = MailingSettings.objects.filter(status='STATED')
    for mailing in mailings:
        # Проверяем количество дней для новой отправки
        if mailing.periodicity == 'DAILY':
            days = 1
        elif mailing.periodicity == 'WEEKLY':
            days = 7
        elif mailing.periodicity == 'MONTHLY':
            days = 30
        # Если пришло время отправлять сообщение (отправений сообщений еще не было, или пришло время отправки)
        if mailing.time_last_shipment == None or mailing.time_last_shipment + timezone.timedelta(days=days) <= time_now:
            mailing.time_last_shipment = time_now
            mailing.save()
            send_emails(mailing)  # передаем 1 рассылку для отправки сообщений


def send_emails(mailing):
    """
    Отправка письма
    """
    number_clients = 0  # количество клиетов
    sent_successfully = 0  # количество успешно отправленных соощений
    response = []  # ответ сервера

    message = mailing.message

    clients = mailing.client.all()
    for client in clients:
        number_clients += 1

        try:
            send_mail(
                subject=message.subject,  # тема письма
                message=message.body,  # сообщение
                from_email=EMAIL_HOST_USER,  # с какого мейла отправляем
                recipient_list=[client.email],  # список имейлов на которые отправляем
                fail_silently=False,
            )
            sent_successfully += 1
            # response.append(str(send_mail))


        except smtplib.SMTPException as e:
            response.append(str(e))

    logs(mailing, number_clients, sent_successfully, response)


def logs(mailing, number_clients, sent_successfully, response):
    clients = mailing.client.all()
    time_zone = pytz.timezone(settings.TIME_ZONE)
    time_now = datetime.now(time_zone)  # время отправки
    # высчитываем статус рассылки
    if number_clients > 0 and sent_successfully > 0 and number_clients / sent_successfully <= 2:
        status = 'успешно'  # доставлено более 50% клиентам

    else:
        status = 'не успешно'

    if len(response) == 0:
        response.append('Нет ответа от сервера')

    Log.objects.create(
        mailing_list=mailing,
        time=time_now,
        client=clients,
        status=status,
        comments=f'Успешно доставлено {sent_successfully} клиентам из {number_clients}',
        server_response=f"{''.join(response)}",

    )

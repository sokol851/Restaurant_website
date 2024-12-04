from django.core.mail import send_mail

from config.celery import app


@app.task
def task_send_mail(subject, message, from_email, recipient_list):
    """ Задача отправки писем через celery """
    send_mail(subject, message, from_email, recipient_list)

from . import mail, db
from flask_mail import Message
from .models import Reminder
from celery import shared_task

import os

SENDER_EMAIL = os.getenv('SENDER_EMAIL')

@shared_task()
def send_reminder_email(reminder_id):
  reminder = Reminder.query.get(reminder_id)
  if reminder and not reminder.is_sent:
    msg = Message(
      subject='Reminder',
      sender=os.getenv('MAIL_USERNAME'),
      recipients=[reminder.email]
    )
    msg.body = f'Reminder for your note: scheduled at {reminder.reminder_time}.'
    mail.send(msg)

    reminder.is_sent = True
    db.session.commit()

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from habits.models import Habit
import requests


@shared_task
def send_habit_reminders():
    now = timezone.now()
    current_time = now.time()

    habits = Habit.objects.filter(time__hour=current_time.hour, time__minute=current_time.minute)

    for habit in habits:
        if habit.user.telegram_chat_id:
            send_telegram_message.delay(
                chat_id=habit.user.telegram_chat_id, text=f"Напоминание: {habit.action} в {habit.place}"
            )


@shared_task
def send_telegram_message(chat_id, text):
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=5)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

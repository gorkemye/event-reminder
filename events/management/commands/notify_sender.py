from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event, NotificationMethodsChoices
from datetime import timedelta, datetime
import time


class Command(BaseCommand):
    help = 'Continuously send notifications for events when their reminder time is exactly 5 minutes before the event time.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting the event reminder notification service..."))

        while True:
            now = timezone.now()

            events_to_remind = Event.objects.filter(
                event_date=now.date(),
                event_time__gt=now.time(),
            )

            for event in events_to_remind:
                event_datetime = timezone.make_aware(
                    datetime.combine(event.event_date, event.event_time),
                    timezone.get_current_timezone()
                )

                reminder_time = event_datetime - timedelta(minutes=5)

                if reminder_time <= now < event_datetime:
                    methods = event.notification_methods
                    self.stdout.write(self.style.SUCCESS(f"Sending notifications for event: {event.event_title}"))

                    if NotificationMethodsChoices.EMAIL in methods:
                        self.stdout.write(self.style.SUCCESS(f"Simulated email notification for: {event.event_title}"))
                    if NotificationMethodsChoices.SMS in methods:
                        self.stdout.write(self.style.SUCCESS(f"Simulated SMS notification for: {event.event_title}"))
                    if NotificationMethodsChoices.APP in methods:
                        self.stdout.write(self.style.SUCCESS(f"Simulated in-app notification for: {event.event_title}"))
                    if NotificationMethodsChoices.PUSH in methods:
                        self.stdout.write(self.style.SUCCESS(f"Simulated push notification for: {event.event_title}"))

            self.stdout.write(self.style.SUCCESS(f"Successfully sent reminders for {events_to_remind.count()} events."))

            self.stdout.write(self.style.SUCCESS("Sleeping for 1 minute..."))
            time.sleep(60)

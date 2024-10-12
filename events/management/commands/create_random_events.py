from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event, ReminderSettings
import random
from datetime import timedelta, datetime

CATEGORY_CHOICES = [
    'Work', 'Personal', 'Social', 'Concert', 'Entertainment', 'Travel',
    'Health', 'Education', 'Finance', 'Other'
]

EVENT_TITLES = [
    "Team Meeting", "Doctor Appointment", "Project Planning", "Lunch with Client", "Yoga Session",
    "Online Course: Python", "Budget Review", "Business Presentation", "Team Building Activity",
    "Hiking Trip", "Webinar on AI", "Finance Consultation", "Health Checkup", "Book Club Meeting",
    "Workshop on Time Management", "Strategy Meeting", "1:1 Meeting", "Project Demo", "Product Launch",
    "Tech Conference", "Rock Concert", "Classical Music Night", "Jazz Festival", "Music Band Rehearsal",
    "Choir Practice", "Open Mic Night", "Songwriting Workshop", "Orchestra Performance",
    "Guitar Practice Session", "Piano Recital", "Karaoke Night", "DJ Live Performance",
    "Indie Music Concert", "Music Album Release Party"
]

EVENT_DESCRIPTIONS = [
    "Discuss project updates and milestones.", "Regular health checkup appointment.",
    "Planning the next steps for the project.", "Meeting to discuss potential business opportunities.",
    "Morning yoga session to relax and start the day.", "Join the course to learn Python programming.",
    "Review monthly budget and expenses.", "Present the business plan to potential investors.",
    "Outdoor activities to improve team morale.", "Hiking trip to enjoy the nature with friends.",
    "Webinar on the latest trends in AI technology.", "Consultation on financial investments.",
    "Health checkup for maintaining wellness.", "Meeting to discuss the latest book.",
    "Time management techniques for better productivity.", "Strategy planning for upcoming projects.",
    "One-on-one meeting to discuss performance.", "Demonstration of the new project features.",
    "Launch event for the new product line.", "Attend the conference to learn about tech innovations.",
    "Enjoy live music with the best rock bands in the city.", "A night of soothing classical music.",
    "Attend the Jazz Festival and enjoy great performances.", "Join the band rehearsal for upcoming events.",
    "Weekly choir practice session for all members.", "Show off your talents at the Open Mic Night.",
    "Learn songwriting techniques from professionals.", "Experience a live orchestra performance.",
    "Improve your guitar skills in this practice session.", "Watch a live piano recital by top musicians.",
    "Have fun singing your favorite songs at Karaoke Night.", "Enjoy the DJ's live performance.",
    "Experience the unique sounds of the indie music scene.", "Join the music album release party and meet the artists."
]

NOTIFICATION_METHODS_CHOICES = ['Email', 'SMS', 'In-App Notification', 'Push Notification']


class Command(BaseCommand):
    help = 'Create 50 random events within the next 10 days from today.'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        for i in range(50):
            event_date = today + timedelta(days=random.randint(0, 10))
            event_hour = random.randint(8, 17)
            event_minute = random.choice([0, 15, 30, 45])
            event_time = datetime.strptime(f"{event_hour}:{event_minute}:00", "%H:%M:%S").time()

            event_datetime = timezone.make_aware(
                datetime.combine(event_date, event_time), timezone.get_current_timezone()
            )
            reminder_minutes_before = random.randint(5, 60)
            reminder_time = event_datetime - timedelta(minutes=reminder_minutes_before)

            is_canceled = i >= 45

            event = Event(
                title=random.choice(EVENT_TITLES),
                description=random.choice(EVENT_DESCRIPTIONS),
                event_date=event_date,
                event_time=event_time,
                category=random.choice(CATEGORY_CHOICES),
                is_canceled=is_canceled
            )
            event.save()

            notification_methods = random.sample(NOTIFICATION_METHODS_CHOICES, k=random.randint(1, 4))
            reminder_settings = ReminderSettings(
                event=event,
                reminder_time=reminder_time,
                notification_methods=notification_methods,
                reminder_note=f"Reminder for {event.title}"
            )
            reminder_settings.save()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created 50 random events, with the last 5 marked as canceled."))

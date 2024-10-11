import datetime

from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField


class CategoryChoices(models.TextChoices):
    """
    Choices for the category of the event. The first value is stored in the database, the second value is displayed.
    """
    WORK = 'Work', 'Work'
    PERSONAL = 'Personal', 'Personal'
    SOCIAL = 'Social', 'Social'
    CONCERT = 'Concert', 'Concert'
    ENTERTAINMENT = 'Entertainment', 'Entertainment'
    TRAVEL = 'Travel', 'Travel'
    HEALTH = 'Health', 'Health'
    EDUCATION = 'Education', 'Education'
    FINANCE = 'Finance', 'Finance'
    OTHER = 'Other', 'Other'


class NotificationMethodsChoices(models.TextChoices):
    EMAIL = 'Email'
    SMS = 'SMS'
    APP = 'In-App Notification'
    PUSH = 'Push Notification'


class Event(models.Model):
    event_title = models.CharField(max_length=200, help_text="Enter the title of the event.",
                                   verbose_name="Event Title")
    event_description = models.TextField(help_text="Enter the description of the event.",
                                         verbose_name="Event Description")
    event_date = models.DateField(help_text="Enter the date of the event.",
                                  verbose_name="Event Date")
    event_time = models.TimeField(help_text="Enter the time of the event.",
                                  verbose_name="Event Time")
    event_category = models.CharField(max_length=50, choices=CategoryChoices,
                                      help_text="Select the category of the event.", verbose_name="Event Category")
    notification_methods = MultiSelectField(choices=NotificationMethodsChoices, default=NotificationMethodsChoices.SMS,
                                            max_length=100,
                                            help_text="Select how you want to be notified about this event.",
                                            verbose_name="Notification Methods")

    event_reminder_time = models.TimeField(null=True, blank=True,
                                           help_text="Set a specific reminder time if different from event time.",
                                           verbose_name="Event Reminder Time")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At",
                                      help_text="The date and time the event was created.")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At",
                                      help_text="The date and time the event was last updated.")

    class Meta:
        ordering = ['event_date', 'event_time']

        verbose_name_plural = "All Events"

    def __str__(self):
        return self.event_title

    @property
    def is_upcoming(self):
        """ Check if the event is in the upcoming 24 hours """
        now = timezone.now()
        event_datetime = timezone.make_aware(datetime.datetime.combine(self.event_date, self.event_time),
                                             timezone.get_current_timezone())
        return now <= event_datetime <= now + datetime.timedelta(days=1)


class UpcomingEventManager(models.Manager):
    """
    Custom Manager for filtering upcoming events only.
    """

    def get_queryset(self):
        now = timezone.now()
        next_day = now + datetime.timedelta(days=1)

        return super().get_queryset().filter(
            models.Q(
                event_date__gt=now.date()
            ) |
            models.Q(
                event_date=now.date(),
                event_time__gte=now.time()
            )
        ).filter(
            models.Q(
                event_date__lt=next_day.date()
            ) |
            models.Q(
                event_date=next_day.date(),
                event_time__lte=next_day.time()
            )
        )


class UpcomingEvent(Event):
    """Proxy model for upcoming events only."""
    objects = UpcomingEventManager()

    class Meta:
        proxy = True
        verbose_name = "Upcoming Event"
        verbose_name_plural = "Upcoming Events"

    def __str__(self):
        return f"Upcoming: {self.event_title} on {self.event_date} at {self.event_time}"


class ExpiredEventManager(models.Manager):
    """
    Custom Manager for filtering expired (past) events only.
    """

    def get_queryset(self):
        now = timezone.now()
        return super().get_queryset().filter(
            models.Q(event_date__lt=now.date()) |
            models.Q(event_date=now.date(), event_time__lt=now.time())
        )


class ExpiredEvent(Event):
    """Proxy model for expired (past) events only."""
    objects = ExpiredEventManager()

    class Meta:
        proxy = True
        verbose_name = "Expired Event"
        verbose_name_plural = "Expired Events"

    def __str__(self):
        return f"Expired: {self.event_title} on {self.event_date} at {self.event_time}"

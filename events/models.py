import datetime
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField

from events.constants import CategoryChoices, NotificationMethodsChoices


class Event(models.Model):
    """Model to handle events."""

    category = models.CharField(max_length=50, choices=CategoryChoices,
                                help_text="Select the category of the event.", verbose_name="Event Category")

    title = models.CharField(max_length=200, help_text="Enter the title of the event.",
                             verbose_name="Event Title")
    description = models.TextField(help_text="Enter the description of the event.",
                                   verbose_name="Event Description")
    event_date = models.DateField(help_text="Enter the date of the event.",
                                  verbose_name="Event Date")
    event_time = models.TimeField(help_text="Enter the time of the event.",
                                  verbose_name="Event Time")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At",
                                      help_text="The date and time the event was created.")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At",
                                      help_text="The date and time the event was last updated.")
    is_canceled = models.BooleanField(default=False, verbose_name="Is Canceled",
                                      help_text="Check this box if you want a soft delete.")

    class Meta:
        ordering = ['event_date', 'event_time']

        verbose_name_plural = "All Events"

    def __str__(self):
        return self.title

    def soft_delete(self):
        """Soft delete the event by marking it as canceled."""
        self.is_canceled = True
        self.save()

    @property
    def is_upcoming(self):
        """ Check if the event is in the upcoming 24 hours """
        now = timezone.now()
        event_datetime = timezone.make_aware(datetime.datetime.combine(self.event_date, self.event_time),
                                             timezone.get_current_timezone())
        return now <= event_datetime <= now + datetime.timedelta(days=1)


class UpcomingEventManager(models.Manager):
    """Custom Manager for filtering upcoming events only."""

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
        return f"Upcoming: {self.title} on {self.event_date} at {self.event_time}"


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
        return f"Expired: {self.title} on {self.event_date} at {self.event_time}"


class CanceledEventManager(models.Manager):
    """Custom Manager for filtering soft deleted events."""

    def get_queryset(self):
        return super().get_queryset().filter(is_canceled=True)


class CanceledEvent(Event):
    """Proxy model for soft deleted events only."""
    objects = CanceledEventManager()

    class Meta:
        proxy = True
        verbose_name = "Canceled Event"
        verbose_name_plural = "Canceled Events"

    def __str__(self):
        return f"Canceled: {self.title} on {self.event_date} at {self.event_time}"


class ReminderSettings(models.Model):
    """Model to handle reminders setting for an event."""
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="reminder_settings", )

    notification_methods = MultiSelectField(choices=NotificationMethodsChoices, default=NotificationMethodsChoices.SMS,
                                            max_length=100,
                                            help_text="Select how you want to be notified about this event.")

    reminder_time = models.DateTimeField(null=True, blank=True,
                                         help_text="Set a specific reminder time if different from event time.",
                                         verbose_name="Reminder Time",
                                         )

    reminder_note = models.TextField(null=True, blank=True,
                                     help_text="Contextual message based on the event's category.",
                                     verbose_name="Reminder Note")

    def __str__(self):
        return f"Reminder settings for {self.event.title}"

    class Meta:
        verbose_name = "Event Reminder Settings"
        verbose_name_plural = "Event Reminder Settings"

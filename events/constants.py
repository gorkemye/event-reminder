from django.db import models


class CategoryChoices(models.TextChoices):
    """Choices for the category of the event."""
    WORK = 'Work'
    PERSONAL = 'Personal'
    SOCIAL = 'Social'
    CONCERT = 'Concert'
    ENTERTAINMENT = 'Entertainment'
    TRAVEL = 'Travel'
    HEALTH = 'Health'
    EDUCATION = 'Education'
    FINANCE = 'Finance'
    OTHER = 'Other'


class NotificationMethodsChoices(models.TextChoices):
    """ Choices for the notification methods."""
    EMAIL = 'Email'
    SMS = 'SMS'
    APP = 'In-App Notification'
    PUSH = 'Push Notification'

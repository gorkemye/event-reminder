from django.contrib import admin
from .models import Event, UpcomingEvent, ExpiredEvent, ReminderSettings, CanceledEvent


class ReminderSettingsInline(admin.StackedInline):
    model = ReminderSettings
    can_delete = False
    verbose_name_plural = 'Reminder Settings'
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'event_date', 'event_time', 'category', 'is_upcoming',
        'get_notification_methods'
    )

    list_display_links = ('title',)

    inlines = (ReminderSettingsInline,)

    search_fields = ('title', 'description', 'category')

    list_filter = ('event_date', 'category', 'created_at', 'is_canceled')

    ordering = ('event_date', 'event_time')

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Event Info', {
            'fields': (
                'title', 'description', ('event_date', 'event_time'), 'category')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    date_hierarchy = 'event_date'

    list_editable = ('category',)

    def is_upcoming(self, obj):
        return obj.is_upcoming

    is_upcoming.boolean = True
    is_upcoming.short_description = 'Upcoming in 24 Hours?'

    def get_notification_methods(self, obj):
        """Retrieve notification methods from ReminderSettings."""
        if hasattr(obj, 'reminder_settings'):
            return ', '.join(obj.reminder_settings.notification_methods)
        return 'No Notification Methods'

    get_notification_methods.short_description = 'Notification Methods'


@admin.register(UpcomingEvent)
class UpcomingEventAdmin(EventAdmin):
    pass


@admin.register(ExpiredEvent)
class ExpiredEventAdmin(EventAdmin):
    pass


@admin.register(CanceledEvent)
class DeletedEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'event_time', 'category', 'created_at', 'updated_at')
    ordering = ['event_date', 'event_time']


@admin.register(ReminderSettings)
class ReminderSettingsAdmin(admin.ModelAdmin):
    list_display = ('event', 'reminder_time', 'notification_methods', 'reminder_note')
    list_filter = ('reminder_time', 'notification_methods')
    search_fields = ('event__title', 'reminder_note')


admin.site.site_header = "Event Reminder Administration"
admin.site.site_title = "Event Reminder Admin Portal"
admin.site.index_title = "Welcome to the Event Reminder Management Portal"

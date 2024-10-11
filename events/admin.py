from django.contrib import admin
from .models import Event, UpcomingEvent, ExpiredEvent


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'event_title', 'event_date', 'event_time', 'event_category', 'is_upcoming', 'created_at', 'updated_at',
        'notification_methods')

    list_display_links = ('event_title',)

    search_fields = ('event_title', 'event_description', 'event_category')

    list_filter = ('event_date', 'event_category', 'created_at')

    ordering = ('event_date', 'event_time')

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Event Info', {
            'fields': (
                'event_title', 'event_description', ('event_date', 'event_time'), 'event_category',
                'event_reminder_time', 'notification_methods')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    date_hierarchy = 'event_date'

    list_editable = ('event_category',)

    def is_upcoming(self, obj):
        return obj.is_upcoming

    is_upcoming.boolean = True
    is_upcoming.short_description = 'Upcoming in 24 Hours?'

    admin.site.site_header = "Event Reminder Administration"
    admin.site.site_title = "Event Reminder Admin Portal"
    admin.site.index_title = "Welcome to the Event Reminder Management Portal"


@admin.register(UpcomingEvent)
class UpcomingEventAdmin(EventAdmin):
    pass


@admin.register(ExpiredEvent)
class ExpiredEventAdmin(EventAdmin):
    pass

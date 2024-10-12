from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Event
from .serializers import EventSerializer
import datetime


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Cancel an event by setting is_canceled to True."""
        try:
            event = self.get_object()
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if event.is_canceled:
            return Response(
                {"detail": "This event is already canceled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        event.is_canceled = True
        event.save()
        return Response({"detail": "Event successfully canceled."}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Override the destroy method to perform hard delete."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Event successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        """List upcoming events within a specified timeframe, with optional filtering by category and the option to include canceled events."""

        now = timezone.now()
        next_hours = request.query_params.get('next_hours', 24)
        show_canceled = request.query_params.get('show_canceled', 'false').lower() == 'true'
        category = request.query_params.get('category', None)

        try:
            next_hours = int(next_hours)
        except ValueError:
            return Response({'error': 'Invalid next_hours parameter, must be an integer.'}, status=400)

        end_time = now + datetime.timedelta(hours=next_hours)

        upcoming_events = Event.objects.filter(
            Q(event_date__gt=now.date()) |
            Q(event_date=now.date(), event_time__gte=now.time())
        ).filter(
            Q(event_date__lt=end_time.date()) |
            Q(event_date=end_time.date(), event_time__lte=end_time.time())
        )

        if category:
            upcoming_events = upcoming_events.filter(category=category)

        if not show_canceled:
            upcoming_events = upcoming_events.exclude(is_canceled=True)

        upcoming_events = upcoming_events.order_by('event_date', 'event_time')

        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='category/(?P<category_name>[^/.]+)')
    def by_category(self, request, category_name=None):
        """Retrieve events by category."""
        events = Event.objects.filter(category=category_name)
        if not events.exists():
            return Response({"error": "No events found in this category."}, status=400)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reminder(self, request, pk=None):
        """Retrieve personalized reminder time for an event."""
        event = self.get_object()

        if hasattr(event, 'reminder_settings'):
            reminder_settings = event.reminder_settings

            return Response({
                "event_title": event.title,
                "reminder_time": reminder_settings.reminder_time,
                "notification_methods": reminder_settings.notification_methods,
                "contextual_message": reminder_settings.contextual_message
            })

        return Response({"error": "Notification settings not found for this event."}, status=404)

    @action(detail=False, methods=['get'], url_path='category/(?P<category_name>[^/.]+)')
    def by_category(self, request, category_name=None):
        """Retrieve events by category.
        :param category_name: Category name to filter events
        :return: Response object with serialized event data
        """
        events = Event.objects.filter(category=category_name)
        if not events.exists():
            return Response({"error": "No events found in this category."}, status=400)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reminder(self, request, pk=None):
        """Retrieve personalized reminder time for an event."""
        event = self.get_object()

        if hasattr(event, 'reminder_settings'):
            reminder_settings = event.reminder_settings

            return Response({
                "event_id": event.id,
                "event_title": event.title,
                "reminder_time": reminder_settings.reminder_time,
                "notification_methods": reminder_settings.notification_methods,
                "reminder_note": reminder_settings.reminder_note
            })

        return Response({"error": "Notification settings not found for this event."}, status=404)

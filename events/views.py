from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Event
from .serializers import EventSerializer
import datetime


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        """
        List upcoming events within a specified timeframe.
        The timeframe is set using the 'next_hours' query parameter.
        If 'next_hours' is not provided, default to 24 hours.
        """
        now = timezone.now()
        next_hours = request.query_params.get('next_hours', 24)

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
        ).order_by('event_date', 'event_time')

        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='category/(?P<category_name>[^/.]+)')
    def by_category(self, request, category_name=None):
        """ Retrieve events by category """
        events = Event.objects.filter(event_category=category_name)
        if not events:
            return Response({"error": "No events found."}, status=400)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reminder(self, request, pk=None):
        """ Retrieve personalized reminder time for an event """
        event = self.get_object()
        reminder_time = event.event_reminder_time or event.event_time
        return Response({"reminder_time": reminder_time})

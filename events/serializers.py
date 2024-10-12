from rest_framework import serializers

from .models import Event, ReminderSettings, NotificationMethodsChoices


class ReminderSettingsSerializer(serializers.ModelSerializer):
    notification_methods = serializers.ListField(
        child=serializers.ChoiceField(choices=NotificationMethodsChoices.choices)
    )

    class Meta:
        model = ReminderSettings
        fields = ['reminder_time', 'notification_methods',
                  'reminder_note']


class EventSerializer(serializers.ModelSerializer):
    reminder_settings = ReminderSettingsSerializer()

    class Meta:
        model = Event
        fields = ['id', 'category', 'title', 'description', 'is_upcoming', 'event_date', 'event_time', 'is_canceled',
                  'reminder_settings']

    def create(self, validated_data):
        reminder_settings_data = validated_data.pop('reminder_settings', None)
        event = Event.objects.create(**validated_data)

        if reminder_settings_data:
            ReminderSettings.objects.create(event=event, **reminder_settings_data)

        return event

    def update(self, instance, validated_data):
        reminder_settings_data = validated_data.pop('reminder_settings', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if reminder_settings_data:
            if hasattr(instance, 'reminder_settings'):
                reminder_settings = instance.reminder_settings
                for attr, value in reminder_settings_data.items():
                    setattr(reminder_settings, attr, value)
                reminder_settings.save()
            else:
                ReminderSettings.objects.create(event=instance, **reminder_settings_data)

        return instance

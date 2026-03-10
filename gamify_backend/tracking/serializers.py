from rest_framework import serializers

from users.models import Character
from .models import Activity, ActivityType

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ['id', 'name', 'category', 'icon', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'character', 'activity_type', 'duration_minutes', 'satisfaction', 'notes', 'xp_earned', 'created_at']
        read_only_fields = ['id', 'xp_earned', 'created_at']

    def create(self, validated_data):
        activity = Activity(**validated_data)
        activity.save()  # Appelle la méthode save() du modèle
        return activity

from rest_framework import serializers
from .models import Activity, ActivityType

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ['id', 'name', 'category', 'icon', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    activity_type = ActivityTypeSerializer(read_only=True)
    character = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'character', 'activity_type', 'duration_minutes', 'calories', 'satisfaction', 'notes', 'xp_earned', 'created_at']
        read_only_fields = ['xp_earned', 'created_at']
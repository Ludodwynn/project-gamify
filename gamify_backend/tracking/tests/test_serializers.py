from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.models import User, Character
from tracking.models import ActivityType, Activity
from tracking.serializers import ActivitySerializer

class ActivitySerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.character = Character.objects.create(user=self.user, name='Test Character', level=1)
        self.activity_type = ActivityType.objects.create(name='Test Activity', category='sport')
        self.activity = Activity.objects.create(
            character=self.character,
            activity_type=self.activity_type,
            duration_minutes=30,
            satisfaction=5
        )

    def test_activity_serializer(self):
        serializer = ActivitySerializer(self.activity)
        self.assertEqual(serializer.data['duration_minutes'], 30)
        self.assertEqual(serializer.data['satisfaction'], 5)
        self.assertEqual(serializer.data['activity_type']['name'], 'Test Activity')

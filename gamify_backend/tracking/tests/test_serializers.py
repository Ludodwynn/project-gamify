from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.models import User, Character, Race, CharacterClass
from tracking.models import Activity, ActivityType
from tracking.serializers import ActivitySerializer, ActivityTypeSerializer

class ActivityTypeSerializerTest(TestCase):
    def setUp(self):
        self.activity_type = ActivityType.objects.create(
            name="Running",
            category="Sport",
            icon="run"
        )

    def test_activity_type_serialization(self):
        """Test an activity type serialization."""
        serializer = ActivityTypeSerializer(self.activity_type)
        self.assertEqual(serializer.data['name'], "Running")
        self.assertEqual(serializer.data['category'], "Sport")
        self.assertEqual(serializer.data['icon'], "run")

    def test_activity_type_creation(self):
        """Test an activity type creation via the serializer."""
        data = {
            'name': "Swimming",
            'category': "Sport",
            'icon': "swim"
        }
        serializer = ActivityTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        activity_type = serializer.save()
        self.assertEqual(activity_type.name, "Swimming")

    def test_activity_type_update(self):
        """Teste la mise à jour d'un type d'activité."""
        update_data = {
            'name': "Updated Running",
            'icon': "updated-run"
        }
        serializer = ActivityTypeSerializer(
            self.activity_type,
            data=update_data,
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        updated_activity_type = serializer.save()
        self.assertEqual(updated_activity_type.name, "Updated Running")


class ActivitySerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        self.race = Race.objects.create(name="Human", description="Humans are versatile.")
        self.character_class = CharacterClass.objects.create(
            name="Warrior",
            description="Warriors are strong.",
            primary_attribute="Strength"
        )
        self.character = Character.objects.create(
            user=self.user,
            name="TestChar",
            race=self.race,
            character_class=self.character_class,
            level=1
        )
        self.activity_type = ActivityType.objects.create(
            name="Running",
            category="Sport"
        )
        self.activity = Activity.objects.create(
            character=self.character,
            activity_type=self.activity_type,
            duration_minutes=60,
            satisfaction=5,
            xp_earned=300
        )

    def test_activity_serialization(self):
        """Test an activity serialization."""
        serializer = ActivitySerializer(self.activity)
        self.assertEqual(serializer.data['duration_minutes'], 60)
        self.assertEqual(serializer.data['satisfaction'], 5)
        self.assertEqual(serializer.data['xp_earned'], 300)
        self.assertEqual(serializer.data['activity_type']['name'], "Running")
        self.assertEqual(serializer.data['activity_type']['category'], "Sport")

    def test_activity_creation_with_xp_calculation(self):
        """Test an activity creation with XP calculus."""
        data = {
            'character': self.character,
            'activity_type': self.activity_type,
            'duration_minutes': 60,
            'satisfaction': 5
        }
        serializer = ActivitySerializer(data=data, context={'character': self.character})
        self.assertTrue(serializer.is_valid())
        activity = serializer.save()
        self.assertEqual(activity.xp_earned, 300)  # 60 * 5 = 300 XP
        self.character.refresh_from_db()
        self.assertEqual(self.character.current_xp, 300)
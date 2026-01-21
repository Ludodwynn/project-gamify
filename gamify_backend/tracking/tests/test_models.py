from django.test import TestCase
from users.models import User, Character, Race, CharacterClass
from tracking.models import Activity, ActivityType

class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.race = Race.objects.create(name="Human", description="Humans are versatile.")
        self.character_class = CharacterClass.objects.create(
            name="Warrior",
            description="Warriors are strong and brave.",
            primary_attribute="Strength"
        )
        self.character = Character.objects.create(
            user=self.user,
            name="TestChar",
            race=self.race,
            character_class=self.character_class,
            level=1,
            current_xp=0
        )
        self.activity_type = ActivityType.objects.create(
            name="Walking Pad",
            category="Sport"
        )

    def test_activity_xp_calculation(self):
        """Test XP calculus for an activity."""
        activity = Activity(
            character=self.character,
            activity_type=self.activity_type,
            duration_minutes=60,  # 60 * 5 = 300 XP
            satisfaction=5,
        )
        activity.save()
        self.character.refresh_from_db()
        self.assertEqual(self.character.current_xp, 0)  # current XP after leveling up
        self.assertEqual(self.character.total_xp, 300)  # total XP earned
        self.assertEqual(self.character.level, 3)  # Leveled up (-100 from 1 to 2, -200 for 2 to 3, total -300 XP, hence why current_xp is 0)

    def test_activity_requires_satisfaction(self):
        """Test that the 'satisfaction' field is mandatory."""
        with self.assertRaises(Exception):  # Error if the satisfaction field is None
            Activity.objects.create(
                character=self.character,
                activity_type=self.activity_type,
                duration_minutes=60,
                satisfaction=None,  # Mandatory field
            )

class ActivityTypeModelTest(TestCase):
    def test_activity_type_creation(self):
        """Test activity type creation."""
        activity_type = ActivityType.objects.create(
            name="Gaming",
            category="Leisure"
        )
        self.assertEqual(activity_type.name, "Gaming")
        self.assertEqual(activity_type.category, "Leisure")

    def test_activity_type_name_must_be_unique(self):
        """Test activity type's name's uniqueness ."""
        ActivityType.objects.create(name="Running", category="Sport")
        with self.assertRaises(Exception):  # Doit échouer si le nom est dupliqué
            ActivityType.objects.create(name="Running", category="Sport")
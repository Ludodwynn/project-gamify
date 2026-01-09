from django.test import TestCase
from users.models import User, Character, Race, CharacterClass
from tracking.models import Activity, ActivityType

class CharacterXPTestCase(TestCase):
    def setUp(self):
        """Create the datas for tests."""
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
            current_xp=0,
            total_xp=0
        )
        self.activity_type = ActivityType.objects.create(
            name="TestActivity",
            category="Sport"
        )



    def test_xp_gain_and_level_up(self):
        """Test XP gains and leveling up."""
        # Create an activity for 600 XP (120 minutes * 5 XP/minute)
        activity = Activity(
            character=self.character,
            activity_type=self.activity_type,
            duration_minutes=120,
            satisfaction=5,
        )
        activity.save()  # Save activity (which add the xp to the character)

        self.character.refresh_from_db()

        # Verify that the character leveled up (600 XP → level 4)
        self.assertEqual(self.character.level, 4)
        self.assertEqual(self.character.current_xp, 0)  # XP remaining after leveling up
        self.assertEqual(self.character.total_xp, 600)  # Total cumulated XP

    def test_slug_regeneration(self):
        """Test the new generation of the slug if the character name changes."""
        self.character.name = "NewName"
        self.character.save()

        # Check of the slug updated well
        self.character.refresh_from_db()
        self.assertEqual(self.character.slug, "newname")
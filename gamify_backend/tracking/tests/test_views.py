from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from users.models import User, Character, Race, CharacterClass
from tracking.models import ActivityType, Activity

class ActivityTypeListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.activity_type = ActivityType.objects.create(name="Running", category="Sport", icon="run")

    def test_activity_type_list(self):
        url = reverse('activity-type-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Running")

class ActivityListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123', email="test@example.com")
        self.client.force_authenticate(user=self.user)
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
        self.activity_type = ActivityType.objects.create(name="Running", category="Sport", icon="run")

    def test_activity_list(self):
        url = reverse('activity-list', kwargs={'character_pk': self.character.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_activity_creation(self):
        url = reverse('activity-list', kwargs={'character_pk': self.character.pk})
        data = {
            'character': self.character.id,
            'activity_type': self.activity_type.id,
            'duration_minutes': 60,
            'satisfaction': 5,
        }
        response = self.client.post(url, data)
        print("RES DATA: ", response.data)
        self.assertEqual(response.status_code, 201)
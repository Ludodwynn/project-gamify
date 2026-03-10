from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from adventures.models import Adventure, Scene
from users.models import User, Character, Race, CharacterClass

class AdventureListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.adventure = Adventure.objects.create(
            title="The Lost Crystal",
            description="Find the lost crystal in the ancient ruins.",
            min_level=1,
            base_xp_reward=200,
            difficulty="easy",
            is_published=True
        )

    def test_adventure_list(self):
        url = reverse('adventure-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "The Lost Crystal")


class SceneListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.adventure = Adventure.objects.create(
            title="The Lost Crystal",
            description="Find the lost crystal in the ancient ruins.",
            min_level=1,
            base_xp_reward=200,
            difficulty="easy",
            is_published=True
        )
        self.scene = Scene.objects.create(
            adventure=self.adventure,
            title="The Entrance",
            content="You stand at the entrance of the ancient ruins.",
            scene_order=1,
            is_starting_scene=True
        )

    def test_scene_list(self):
        url = reverse('scene-list', kwargs={'adventure_pk': self.adventure.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "The Entrance")


class AdventureProgressListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123', email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.race = Race.objects.create(name="Human", description="Humans are versatile.")
        self.character_class = CharacterClass.objects.create(name="Warrior", description="Warriors are strong and brave.", primary_attribute="Strength")
        self.character = Character.objects.create(
            user=self.user,
            name="TestChar",
            race=self.race,
            character_class=self.character_class,
            level=1,
            current_xp=0,
            total_xp=0
        )
        self.adventure = Adventure.objects.create(
            title="The Lost Crystal",
            description="Find the lost crystal in the ancient ruins.",
            min_level=1,
            base_xp_reward=200,
            difficulty="easy",
            is_published=True
        )
        self.scene = Scene.objects.create(
            adventure=self.adventure,
            title="The Entrance",
            content="You stand at the entrance of the ancient ruins.",
            scene_order=1,
            is_starting_scene=True
        )

    def test_adventure_progress_list(self):
        url = reverse('adventure-progress-list', kwargs={'character_pk': self.character.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_adventure_progress_creation(self):
        url = reverse('adventure-progress-list', kwargs={'character_pk': self.character.pk})
        data = {
            'adventure': self.adventure.id,
            'current_scene': self.scene.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
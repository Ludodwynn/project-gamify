from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from adventures.models import Adventure, Scene, SceneChoice, AdventureProgress
from adventures.serializers import AdventureProgressSerializer, AdventureSerializer, SceneChoiceSerializer, SceneSerializer
from users.models import Race, User, Character, CharacterClass
from game.models import Enemy, Skill, Equipment

class AdventureSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username="testuser", is_staff=False, email="test@example.com", password="testpass123")
        self.request = self.factory.get('/fake-path/')
        force_authenticate(self.request, user=self.user)

        self.adventure = Adventure.objects.create(
            title="Test Adventure",
            description="Test Description",
            min_level=1,
            base_xp_reward=100,
            difficulty="easy"
        )
        self.request = self.factory.get('/fake-path/')
        force_authenticate(self.request, user=self.user)

    def test_adventure_serializer(self):
        serializer = AdventureSerializer(self.adventure, context={'request': self.request})
        self.assertEqual(serializer.data['title'], "Test Adventure")
        self.assertNotIn('is_published', serializer.data)

class SceneSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpass123")
        self.adventure = Adventure.objects.create(
            title="Test Adventure",
            description="Test Description",
            min_level=1,
            base_xp_reward=100,
            difficulty="easy"
        )
        self.scene1 = Scene.objects.create(
            adventure=self.adventure,
            title="Test Scene 2",
            content="Test content for scene 2",
            scene_order=2,
            is_ending_scene=True
        )
        self.scene = Scene.objects.create(
            adventure=self.adventure,
            title="Test Scene",
            content="Test content for scene 1",
            scene_order=1,
            next_scene=self.scene1,
            is_starting_scene=True
        )


    def test_scene_serializer(self):
        serializer = SceneSerializer(self.scene)
        self.assertEqual(serializer.data['title'], "Test Scene")
        self.assertEqual(serializer.data['scene_order'], 1)
        self.assertEqual(serializer.data['next_scene']['title'], "Test Scene 2")

class SceneChoiceSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpass123")
        self.race = Race.objects.create(name="Human", description="The most polyvalent race")
        self.character_class = CharacterClass.objects.create(name="Warrior")
        self.character = Character.objects.create(
            user=self.user,
            name="Test Character",
            level=5,
            race = self.race,
            character_class=self.character_class
        )
        self.adventure = Adventure.objects.create(
            title="Test Adventure",
            description="Test Description",
            min_level=1,
            base_xp_reward=100,
            difficulty="easy"
        )
        self.scene1 = Scene.objects.create(
            adventure=self.adventure,
            title="Test Scene 1",
            content="Test content for scene 1",
            scene_order=1,
            is_starting_scene=True
        )
        self.scene2 = Scene.objects.create(
            adventure=self.adventure,
            title="Test Scene 2",
            content="Test content for scene 2",
            scene_order=2,
            is_ending_scene=True
        )
        self.choice = SceneChoice.objects.create(
            scene=self.scene1,
            text="Test Choice",
            order=1,
            next_scene=self.scene2,
            required_class=self.character_class
        )

    def test_is_available_with_character(self):
        serializer_context = {'character': self.character}
        serializer = SceneChoiceSerializer(self.choice, context=serializer_context)
        self.assertIn('is_available', serializer.data)
        self.assertTrue(serializer.data['is_available'])

    def test_is_available_without_character(self):
        serializer_context = {}
        serializer = SceneChoiceSerializer(self.choice, context=serializer_context)
        self.assertFalse(serializer.data['is_available'])

    def test_unavailable_reason(self):
        serializer_context = {}
        serializer = SceneChoiceSerializer(self.choice, context=serializer_context)
        self.assertFalse(serializer.data['is_available'])
        self.assertEqual(serializer.data['unavailable_reason'], "Character required")

    def test_unavailable_reason_with_character(self):
        self.choice.required_class = CharacterClass.objects.create(name="Mage") 
        self.choice.save()
        
        serializer_context = {'character': self.character}
        serializer = SceneChoiceSerializer(self.choice, context=serializer_context)
        self.assertFalse(serializer.data['is_available'])
        self.assertEqual(serializer.data['unavailable_reason'], f"Require class: {self.choice.required_class.name}")

class AdventureProgressSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpass123")
        self.request = self.factory.get('/fake-path/')
        force_authenticate(self.request, user=self.user)

        self.race = Race.objects.create(name="Human", description="The most polyvalent race")
        self.character_class = CharacterClass.objects.create(name="Warrior")
        self.character = Character.objects.create(
            user=self.user,
            name="Test Character",
            level=5,
            race = self.race,
            character_class=self.character_class
        )
        self.adventure = Adventure.objects.create(
            title="Test Adventure",
            description="Test Description",
            min_level=1,
            base_xp_reward=100,
            difficulty="easy"
        )
        self.scene = Scene.objects.create(
            adventure=self.adventure,
            content="This is a test",
            title="Test Scene",
            scene_order=1
        )
        self.scene1 = Scene.objects.create(
            adventure=self.adventure,
            title="Test Scene 2",
            content="Test content for scene 2",
            scene_order=2,
            is_ending_scene=True
        )
        self.progress = AdventureProgress.objects.create(
            character=self.character,
            adventure=self.adventure,
            current_scene=self.scene,
            completed=False,
            xp_earned=100
        )

    def test_adventure_progress_serializer(self):
        self.assertEqual(self.progress.current_scene.scene_order, 1)
        self.assertEqual(self.progress.adventure.scenes.count(), 2)
        serializer = AdventureProgressSerializer(self.progress, context={'request': self.request})
        self.assertEqual(serializer.data['progress_percentage'], 50)
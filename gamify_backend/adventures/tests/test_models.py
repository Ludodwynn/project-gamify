from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User, Character, Race, CharacterClass
from adventures.models import Adventure, Scene, SceneChoice, AdventureProgress

class AdventureModelTest(TestCase):
    def setUp(self):
        self.adventure = Adventure.objects.create(
            title="Test Adventure",
            description="Test Description",
            min_level=1,
            base_xp_reward=100,
            difficulty="easy"
        )

    def test_adventure_creation(self):
        """Test adventure creation."""
        self.assertEqual(self.adventure.title, "Test Adventure")
        self.assertEqual(self.adventure.description, "Test Description")
        self.assertEqual(self.adventure.min_level, 1)
        self.assertEqual(self.adventure.base_xp_reward, 100)
        self.assertEqual(self.adventure.difficulty, "easy")

    def test_adventure_validation(self):
        """Test field validation for an adventure."""
        with self.assertRaises(ValidationError):
            Adventure.objects.create(
                title="",  # Empty title
                description="Test Description",
                min_level=1,
                base_xp_reward=100,
                difficulty="easy"
            ).full_clean()


class SceneModelTest(TestCase):
    def setUp(self):
        self.adventure = Adventure.objects.create(
            title="Test Adventure",
            description="Test Description",
            min_level=1,
            base_xp_reward=100,
            difficulty="easy"
        )
        self.scene = Scene.objects.create(
            adventure=self.adventure,
            title="Test Scene",
            content="Test content for scene",
            scene_order=1,
            is_starting_scene=True
        )

    def test_scene_creation(self):
        """Test scene creation."""
        self.assertEqual(self.scene.title, "Test Scene")
        self.assertEqual(self.scene.content, "Test content for scene")
        self.assertEqual(self.scene.scene_order, 1)
        self.assertTrue(self.scene.is_starting_scene)

    def test_scene_validation(self):
        """Test field validation for a scene."""
        with self.assertRaises(ValidationError):
            Scene.objects.create(
                adventure=self.adventure,
                title="",  # Empty title
                content="Test content for scene",
                scene_order=1,
                is_starting_scene=True
            ).full_clean()


class SceneChoiceModelTest(TestCase):
    def setUp(self):
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
            next_scene=self.scene2
        )

    def test_scene_choice_creation(self):
        """Test scene choice creation."""
        self.assertEqual(self.choice.text, "Test Choice")
        self.assertEqual(self.choice.order, 1)
        self.assertEqual(self.choice.next_scene, self.scene2)

    def test_scene_choice_validation(self):
        """Test field validation for a scene choice."""
        with self.assertRaises(ValidationError):
            SceneChoice.objects.create(
                scene=self.scene1,
                text="",  # Empty text
                order=1,
                next_scene=self.scene2
            ).full_clean()

class AdventureProgressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.race = Race.objects.create(name="Human", description="The most polyvalent race")
        self.character_class = CharacterClass.objects.create(name="Warrior")
        self.character = Character.objects.create(
            user=self.user,
            name="Test Character",
            level=5,
            race=self.race,
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
            title="Test Scene",
            content="Test content for scene",
            scene_order=1,
            is_starting_scene=True
        )
        self.progress = AdventureProgress.objects.create(
            character=self.character,
            adventure=self.adventure,
            current_scene=self.scene,
            completed=False,
            xp_earned=100
        )

    def test_adventure_progress_creation(self):
        """Test adventure progress creation."""
        self.assertEqual(self.progress.character, self.character)
        self.assertEqual(self.progress.adventure, self.adventure)
        self.assertEqual(self.progress.current_scene, self.scene)
        self.assertFalse(self.progress.completed)
        self.assertEqual(self.progress.xp_earned, 100)

    def test_adventure_progress_validation(self):
        """Test field validation for an adventure progress."""
        progress = AdventureProgress(
            character=self.character,
            adventure=self.adventure,
            current_scene=None,  # Champ requis non fourni
            completed=False,
            xp_earned=100
        )
        with self.assertRaises(ValidationError) as context:
            progress.full_clean()
        self.assertIn('current_scene', str(context.exception))


class SceneChoiceMethodsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.race = Race.objects.create(name="Human", description="The most polyvalent race")
        self.character_class = CharacterClass.objects.create(name="Warrior")
        self.character = Character.objects.create(
            user=self.user,
            name="Test Character",
            level=5,
            race=self.race,
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

    def test_is_available_for_character(self):
        """Test is_available_for_character method."""
        self.assertTrue(self.choice.is_available_for_character(self.character))

    def test_is_not_available_for_character(self):
        """Test is_available_for_character method, with a different class."""
        other_class = CharacterClass.objects.create(name="Mage")
        other_character = Character.objects.create(
            user=self.user,
            name="Other Character",
            level=5,
            race=self.race,
            character_class=other_class
        )
        self.assertFalse(self.choice.is_available_for_character(other_character))
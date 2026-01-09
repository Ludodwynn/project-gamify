from django.test import TestCase
from rest_framework.test import APIRequestFactory
from adventures.models import Scene, SceneChoice
from users.models import Character
from adventures.serializers import SceneChoiceSerializer

class SceneChoiceSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.character = Character.objects.create(name="Test Character", level=5)
        self.scene = Scene.objects.create(title="Test Scene", scene_order=1)
        self.choice = SceneChoice.objects.create(
            scene=self.scene,
            text="Test Choice",
            required_class=self.character.character_class,  # Utilise l'objet CharacterClass, pas une chaîne
            required_level=3
        )

    def test_is_available_with_character(self):
        """Teste que `is_available` retourne True si le personnage a le niveau requis."""
        request = self.factory.get('/fake-path/')
        request.user = self.character.user
        serializer_context = {'request': request, 'character': self.character}
        serializer = SceneChoiceSerializer(self.choice, context=serializer_context)
        self.assertIn('is_available', serializer.data)
        self.assertTrue(serializer.data['is_available'])

    def test_is_available_without_character(self):
        """Teste que `is_available` retourne False si aucun personnage n'est fourni."""
        serializer_context = {}
        serializer = SceneChoiceSerializer(self.choice, context=serializer_context)
        self.assertFalse(serializer.data['is_available'])
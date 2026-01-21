# users/tests/test_views.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from users.models import Character, Race, CharacterClass

class UserDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user-detail')

    def test_retrieve_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_user(self):
        data = {'username': 'newusername'}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

class UserDeleteViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user-delete')

    def test_delete_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

class CharacterListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.race = Race.objects.create(name="Human", description="The most polyvalent race")
        self.character_class = CharacterClass.objects.create(name="Warrior")
        self.client.force_authenticate(user=self.user)
        self.url = reverse('character-list')

    def test_character_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_character_creation(self):
        data = {
            'name': 'Test Character',
            'race': self.race.id,
            'character_class': self.character_class.id,
            'level': 1,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)

class CharacterDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.race = Race.objects.create(name="Human", description="The most polyvalent race")
        self.character_class = CharacterClass.objects.create(name="Warrior")
        self.character = Character.objects.create(
            user=self.user,
            name="Test Character",
            level=5,
            race=self.race,
            character_class=self.character_class
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('character-detail', kwargs={'pk': self.character.pk})

    def test_retrieve_character(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Character')

    def test_update_character(self):
        data = {'name': 'New Character Name'}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.character.refresh_from_db()
        self.assertEqual(self.character.name, 'New Character Name')

    def test_delete_character(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

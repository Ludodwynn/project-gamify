from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.models import User, Character, Race, CharacterClass
from users.serializers import UserSerializer, CharacterSerializer

class UserSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'John',
            'last_name': 'Doe'
        }

    def test_user_creation_with_valid_data(self):
        """Test user creation with valid datas."""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())  
        user = serializer.save() 
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertNotEqual(user.password, 'testpassword123') 
        self.assertTrue(user.check_password('testpassword123')) 

    def test_user_creation_with_invalid_email(self):
        """Test email validation."""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_user_creation_with_duplicate_username(self):
        """Teste username uniqueness."""
        User.objects.create_user(username='testuser', email='existing@example.com', password='password')
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_user_update_with_password_change(self):
        """Test user update with password change."""
        user = User.objects.create_user(username='olduser', email='old@example.com', password='oldpassword')
        update_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword123',  # Nouveau mot de passe
            'first_name': 'Jane'
        }

        serializer = UserSerializer(user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, 'newuser')
        self.assertEqual(updated_user.first_name, 'Jane')
        self.assertTrue(updated_user.check_password('newpassword123'))


class CharacterSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.race = Race.objects.create(name='Elf', description='Agile and wise.')
        self.character_class = CharacterClass.objects.create(
            name='Mage',
            description='Casts spells.',
            primary_attribute='Intelligence'
        )
        self.character = Character.objects.create(
            user=self.user,
            name='Gandalf',
            race=self.race,
            character_class=self.character_class,
            level=1,
            current_xp=50
        )

    def test_character_serialization(self):
        serializer = CharacterSerializer(self.character)
        self.assertEqual(serializer.data['name'], 'Gandalf')
        self.assertEqual(serializer.data['race']['name'], 'Elf')

    def test_read_only_fields_cannot_be_modified(self):
        update_data = {'name': 'Gandalf Le Blanc', 'slug': 'custom-slug'}
        serializer = CharacterSerializer(self.character, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_character = serializer.save()
        self.assertNotEqual(updated_character.slug, 'custom-slug')
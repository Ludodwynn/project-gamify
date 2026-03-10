from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from users.models import User, Character, Race, CharacterClass
from game.models import CharacterSkill, Skill, Enemy, Equipment, CharacterEquipment

############################### SKILL

class SkillListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123', email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.character_class = CharacterClass.objects.create(name="Warrior", description="Warriors are strong and brave.", primary_attribute="Strength")
        self.skill = Skill.objects.create(name="Fireball", description="A powerful fire spell.", character_class=self.character_class, unlock_at_level=1)

    def test_skill_list(self):
        url = reverse('skill-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Fireball")


class SkillDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123', email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.character_class = CharacterClass.objects.create(name="Warrior", description="Warriors are strong and brave.", primary_attribute="Strength")
        self.skill = Skill.objects.create(name="Fireball", description="A powerful fire spell.", character_class=self.character_class, unlock_at_level=1)

    def test_skill_detail(self):
        url = reverse('skill-detail', kwargs={'pk': self.skill.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Fireball")


class CharacterSkillListViewTest(APITestCase):
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
        self.skill = Skill.objects.create(name="Fireball", description="A powerful fire spell.", character_class=self.character_class, unlock_at_level=1)

    def test_character_skill_list(self):
        url = reverse('character-skill-list', kwargs={'character_pk': self.character.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_character_skill_creation(self):
        url = reverse('character-skill-list', kwargs={'character_pk': self.character.pk})
        data = {
            'skill': self.skill.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)


class CharacterSkillDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123', email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.race = Race.objects.create(name="Human", description="Humans are versatile.")
        self.character_class = CharacterClass.objects.create(name="Mage", description="Mage are intelligent and cunning.", primary_attribute="Intelligence")
        self.character = Character.objects.create(
            user=self.user,
            name="TestChar",
            race=self.race,
            character_class=self.character_class,
            level=1,
            current_xp=0,
            total_xp=0
        )
        self.skill = Skill.objects.create(name="Fireball", description="A powerful fire spell.", character_class=self.character_class, unlock_at_level=1)
        self.character_skill = CharacterSkill.objects.create(character=self.character, skill=self.skill)

    def test_character_skill_detail(self):
        url = reverse('character-skill-detail', kwargs={'character_pk': self.character.pk, 'pk': self.character_skill.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['skill']['name'], "Fireball")

############################ ENEMY

class EnemyListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.enemy = Enemy.objects.create(
            name="Goblin",
            description="A small, green creature.",
            hp=50,
            min_damage=1,
            max_damage=5,
            is_boss=False,
            xp_reward=10
        )

    def test_enemy_list(self):
        url = reverse('enemy-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Goblin")


class EnemyDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.enemy = Enemy.objects.create(
            name="Goblin",
            description="A small, green creature.",
            hp=50,
            min_damage=1,
            max_damage=5,
            is_boss=False,
            xp_reward=10
        )

    def test_enemy_detail(self):
        url = reverse('enemy-detail', kwargs={'pk': self.enemy.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Goblin")

############################## EQUIPMENT

class EquipmentListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.character_class = CharacterClass.objects.create(name="Warrior", description="Warriors are strong and brave.", primary_attribute="Strength")
        self.equipment = Equipment.objects.create(
            name="Iron Sword",
            description="A basic sword made of iron.",
            slot="weapon",
            rarity="common",
            required_level=1,
            required_class=self.character_class
        )

    def test_equipment_list(self):
        url = reverse('equipment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Iron Sword")


class EquipmentDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.character_class = CharacterClass.objects.create(name="Warrior", description="Warriors are strong and brave.", primary_attribute="Strength")
        self.equipment = Equipment.objects.create(
            name="Iron Sword",
            description="A basic sword made of iron.",
            slot="weapon",
            rarity="common",
            required_level=1,
            required_class=self.character_class
        )

    def test_equipment_detail(self):
        url = reverse('equipment-detail', kwargs={'pk': self.equipment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Iron Sword")

class CharacterEquipmentListViewTest(APITestCase):
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
        self.equipment = Equipment.objects.create(
            name="Iron Sword",
            description="A basic sword made of iron.",
            slot="weapon",
            rarity="common",
            required_level=1,
            required_class=self.character_class
        )

    def test_character_equipment_list(self):
        url = reverse('character-equipment-list', kwargs={'character_pk': self.character.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_character_equipment_creation(self):
        url = reverse('character-equipment-list', kwargs={'character_pk': self.character.pk})
        data = {
            'equipment': self.equipment.id,
            'is_equipped': False,
            'acquired_from': 'test'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)


class CharacterEquipmentDetailViewTest(APITestCase):
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
        self.equipment = Equipment.objects.create(
            name="Iron Sword",
            description="A basic sword made of iron.",
            slot="weapon",
            rarity="common",
            required_level=1,
            required_class=self.character_class
        )
        self.character_equipment = CharacterEquipment.objects.create(
            character=self.character,
            equipment=self.equipment,
            is_equipped=False,
            acquired_from='test'
        )

    def test_character_equipment_detail(self):
        url = reverse('character-equipment-detail', kwargs={'character_pk': self.character.pk, 'pk': self.character_equipment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['equipment_details']['name'], "Iron Sword")
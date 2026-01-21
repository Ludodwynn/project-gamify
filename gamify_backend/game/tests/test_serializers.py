from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.models import User, Character, Race, CharacterClass
from game.models import Skill, CharacterSkill, Equipment, Enemy
from game.serializers import SkillSerializer, CharacterSkillSerializer, EquipmentSerializer, EnemySerializer

class SkillSerializerTest(TestCase):
    def setUp(self):
        self.character_class = CharacterClass.objects.create(
            name="Mage",
            description="Casts spells.",
            primary_attribute="Intelligence"
        )
        self.skill = Skill.objects.create(
            name="Fireball",
            description="Deals fire damage.",
            character_class=self.character_class,
            skill_type="combat",
            unlock_at_level=3,
            is_active=True,
            bonus_type="damage",
            bonus_value=10.00
        )

    def test_skill_serialization(self):
        """Test skill serialization."""
        serializer = SkillSerializer(self.skill)
        self.assertEqual(serializer.data['name'], "Fireball")
        self.assertEqual(serializer.data['skill_type'], "combat")
        self.assertEqual(serializer.data['unlock_at_level'], 3)
        self.assertEqual(serializer.data['bonus_type'], "damage")
        self.assertEqual(serializer.data['bonus_value'], "10.00")
    
    def test_skill_creation(self):
        """Test skill creation via the serializer."""
        data = {
            'name': "Ice Shard",
            'description': "Deals ice damage.",
            'skill_type': "combat",
            'unlock_at_level': 5,
            'is_active': True,
            'bonus_type': "damage",
            'bonus_value': 15.0
        }
        serializer = SkillSerializer(data=data, context={'character_class': self.character_class})
        self.assertTrue(serializer.is_valid())
        skill = serializer.save()
        self.assertEqual(skill.name, "Ice Shard")
        self.assertEqual(skill.unlock_at_level, 5)
    
    def test_is_usable_method(self):
        """Test`is_usable` method with a character."""
        user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        race = Race.objects.create(name="Elf", description="Agile and wise.")
        character = Character.objects.create(
            user=user,
            name="Gandalf",
            race=race,
            character_class=self.character_class,
            level=5
        )
        serializer_context = {'character': character}
        serializer = SkillSerializer(self.skill, context=serializer_context)
        self.assertTrue(serializer.data['is_usable'])

class EquipmentSerializerTest(TestCase):
    def setUp(self):
        self.character_class = CharacterClass.objects.create(
            name="Mage",
            description="Casts spells.",
            primary_attribute="Intelligence"
        )
        self.equipment = Equipment.objects.create(
            name="Staff of Power",
            description="A powerful staff for mages.",
            slot="weapon",
            rarity="legendary",
            primary_stat_type="Intelligence",
            primary_stat_value=10.0,
            required_level=5,
            required_class=self.character_class
        )
    
    def test_equipment_serialization(self):
        """Teste equipment serialization."""
        serializer = EquipmentSerializer(self.equipment)
        self.assertEqual(serializer.data['name'], "Staff of Power")
        self.assertEqual(serializer.data['slot'], "weapon")
        self.assertEqual(serializer.data['rarity'], "legendary")
        self.assertEqual(serializer.data['required_level'], 5)

    def test_is_equippable_method(self):
        """Test `is_equippable` method with a character."""
        user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        race = Race.objects.create(name="Elf", description="Agile and wise.")
        character = Character.objects.create(
            user=user,
            name="Gandalf",
            race=race,
            character_class=self.character_class,
            level=5
        )
        serializer = EquipmentSerializer(self.equipment, context={'character': character})
        self.assertTrue(serializer.data['is_equippable'])


class EnemySerializerTest(TestCase):
    def setUp(self):
        self.enemy = Enemy.objects.create(
            name="Goblin",
            description="A small, green creature.",
            hp=50,
            min_damage=1,
            max_damage=5,
            is_boss=False,
            xp_reward=10
        )

    def test_enemy_serialization(self):
        """Test an enemy serialization."""
        serializer = EnemySerializer(self.enemy)
        self.assertEqual(serializer.data['name'], "Goblin")
        self.assertEqual(serializer.data['hp'], 50)
        self.assertEqual(serializer.data['xp_reward'], 10)

    def test_damage_range_field(self):
        """Test calculated field `damage_range`."""
        serializer = EnemySerializer(self.enemy)
        self.assertEqual(serializer.data['damage_range'], "Damages range from 1 to 5")


class CharacterSkillSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.race = Race.objects.create(name="Elf", description="Agile and wise.")
        self.character_class = CharacterClass.objects.create(
            name="Mage",
            description="Casts spells.",
            primary_attribute="Intelligence"
        )
        self.character = Character.objects.create(
            user=self.user,
            name="Gandalf",
            race=self.race,
            character_class=self.character_class,
            level=5
        )
        self.skill = Skill.objects.create(
            name="Fireball",
            description="Deals fire damage.",
            character_class=self.character_class,
            skill_type="combat",
            unlock_at_level=3,
            is_active=True
        )
        self.character_skill = CharacterSkill.objects.create(
            character=self.character,
            skill=self.skill
        )

    def test_character_skill_serialization(self):
        """Test character skill serialization."""
        serializer = CharacterSkillSerializer(self.character_skill)
        self.assertEqual(serializer.data['skill']['name'], "Fireball")
        self.assertEqual(serializer.data['character'], self.character.id)
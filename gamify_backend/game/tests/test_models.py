from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User, Character, Race, CharacterClass
from game.models import Skill, CharacterSkill, Equipment, CharacterEquipment, Enemy

class SkillModelTest(TestCase):
    def setUp(self):
        self.character_class = CharacterClass.objects.create(
            name="Mage",
            description="Casts spells.",
            primary_attribute="Intelligence"
        )

    def test_skill_creation(self):
        """Test a skill creation."""
        skill = Skill.objects.create(
            name="Fireball",
            description="Deals fire damage.",
            character_class=self.character_class,
            skill_type="combat",
            unlock_at_level=3,
            is_active=True
        )
        self.assertEqual(skill.name, "Fireball")
        self.assertEqual(skill.skill_type, "combat")
        self.assertTrue(skill.is_active)

    def test_skill_uniqueness(self):
        """Test skill name uniqueness."""
        Skill.objects.create(
            name="Fireball",
            description="Deals fire damage.",
            character_class=self.character_class,
            skill_type="combat",
            unlock_at_level=3
        )
        with self.assertRaises(Exception):  # Doit échouer si le nom est dupliqué
            Skill.objects.create(
                name="Fireball",  # Même nom
                description="Another fireball.",
                character_class=self.character_class,
                skill_type="combat",
                unlock_at_level=5
            )
    
    def test_is_usable_method(self):
        """Test method `is_usable`."""
        user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        race = Race.objects.create(name="Elf", description="Agile and wise.")
        character = Character.objects.create(
            user=user,
            name="Gandalf",
            race=race,
            character_class=self.character_class,
            level=5
        )
        skill = Skill.objects.create(
            name="Fireball",
            description="Deals fire damage.",
            character_class=self.character_class,
            skill_type="combat",
            unlock_at_level=3,
            is_active=True
        )
        self.assertTrue(skill.is_usable(character))


class CharacterSkillModelTest(TestCase):
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

    def test_character_skill_creation(self):
        """Test skill creation for a character."""
        character_skill = CharacterSkill.objects.create(
            character=self.character,
            skill=self.skill
        )
        self.assertEqual(character_skill.character, self.character)
        self.assertEqual(character_skill.skill, self.skill)
        self.assertEqual(character_skill.acquired_level, 5)


    def test_character_skill_validation(self):
        """Test skill validation (required level and class)."""
        self.character.level = 2
        self.character.save()
        with self.assertRaises(ValidationError):
            CharacterSkill.objects.create(
                character=self.character,
                skill=self.skill
            ).full_clean()

        other_class = CharacterClass.objects.create(
            name="Warrior",
            description="Strong and brave.",
            primary_attribute="Strength"
        )
        other_character = Character.objects.create(
            user=self.user,
            name="Aragorn",
            race=self.race,
            character_class=other_class,
            level=5
        )
        with self.assertRaises(ValidationError):
            CharacterSkill.objects.create(
                character=other_character,
                skill=self.skill  # Classe requise = Mage
            ).full_clean()


class EquipmentModelTest(TestCase):
    def setUp(self):
        self.character_class = CharacterClass.objects.create(
            name="Mage",
            description="Casts spells.",
            primary_attribute="Intelligence"
        )

    def test_equipment_creation(self):
        """Test equipment creation."""
        equipment = Equipment.objects.create(
            name="Staff of Power",
            description="A powerful staff for mages.",
            slot="weapon",
            rarity="legendary",
            primary_stat_type="Intelligence",
            primary_stat_value=10.0,
            required_level=5,
            required_class=self.character_class
        )
        
        self.assertEqual(equipment.name, "Staff of Power")
        self.assertEqual(equipment.slot, "weapon")
        self.assertEqual(equipment.rarity, "legendary")

    def test_equipment_uniqueness(self):
        """Test an equipment's name uniqueness."""
        Equipment.objects.create(
            name="Staff of Power",
            description="A powerful staff for mages.",
            slot="weapon",
            rarity="legendary"
        )
        with self.assertRaises(Exception):  # Doit échouer si le nom est dupliqué
            Equipment.objects.create(
                name="Staff of Power",  # Même nom
                description="Another staff.",
                slot="weapon",
                rarity="rare"
            )

class CharacterEquipmentModelTest(TestCase):
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
        self.equipment = Equipment.objects.create(
            name="Staff of Power",
            description="A powerful staff for mages.",
            slot="weapon",
            rarity="legendary",
            required_level=5,
            required_class=self.character_class
        )

    def test_character_equipment_creation(self):
        """Test equipment creation for a character."""
        character_equipment = CharacterEquipment.objects.create(
            character=self.character,
            equipment=self.equipment,
            is_equipped=True
        )
        self.assertEqual(character_equipment.character, self.character)
        self.assertEqual(character_equipment.equipment, self.equipment)
        self.assertTrue(character_equipment.is_equipped)


    def test_character_equipment_validation(self):
        """Test equipment validation (required level and class)."""
        self.character.level = 4
        self.character.save()
        with self.assertRaises(ValidationError):
            CharacterEquipment.objects.create(
                character=self.character,
                equipment=self.equipment
            ).full_clean()

        other_class = CharacterClass.objects.create(
            name="Warrior",
            description="Strong and brave.",
            primary_attribute="Strength"
        )
        other_character = Character.objects.create(
            user=self.user,
            name="Aragorn",
            race=self.race,
            character_class=other_class,
            level=5
        )
        with self.assertRaises(ValidationError):
            CharacterEquipment.objects.create(
                character=other_character,
                equipment=self.equipment  # Classe requise = Mage
            ).full_clean()


class EnemyModelTest(TestCase):
    def test_enemy_creation(self):
        """Test enemy creation."""
        enemy = Enemy.objects.create(
            name="Goblin",
            description="A small, green creature.",
            hp=50,
            min_damage=1,
            max_damage=5,
            is_boss=False,
            xp_reward=10
        )
        self.assertEqual(enemy.name, "Goblin")
        self.assertEqual(enemy.hp, 50)
        self.assertEqual(enemy.xp_reward, 10)


    def test_enemy_damage_range(self):
        """Test `get_damage_range` method."""
        enemy = Enemy.objects.create(
            name="Goblin",
            description="A small, green creature.",
            hp=50,
            min_damage=1,
            max_damage=5,
            is_boss=False,
            xp_reward=10
        )
        self.assertEqual(enemy.get_damage_range(), "1-5")

    def test_enemy_random_damage(self):
        """Test `get_random_damage` method."""
        enemy = Enemy.objects.create(
            name="Goblin",
            description="A small, green creature.",
            hp=50,
            min_damage=1,
            max_damage=5,
            is_boss=False,
            xp_reward=10
        )
        random_damage = enemy.get_random_damage()
        self.assertTrue(1 <= random_damage <= 5)

    
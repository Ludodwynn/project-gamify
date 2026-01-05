from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from users.models import CharacterClass, Character

class Skill(models.Model):
    """
    Skills available in the game.
    """
    SKILL_TYPES = [
        ('combat', 'Combat'),
        ('env', 'Environment'),
        ('social', 'Social'),
        ('craft', 'Craft'),
        ('mystical', 'Mystical'),
        ('utility', 'Utility')
    ]
    name = models.CharField(max_length=100, unique=True, verbose_name="Skill name")
    description = models.TextField(verbose_name="Skill description")
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, related_name="skills", verbose_name="Required class")
    skill_type = models.CharField(max_length=10, choices=SKILL_TYPES, default='combat', verbose_name="Skill type")
    cooldown = models.IntegerField(default=0, validators=[MinValueValidator(0)], blank=True, null=True, verbose_name="Skill cooldown (in game turn)")
    is_active = models.BooleanField(default=False, verbose_name="active skills (contraty to a passive)")
    is_npc_skill = models.BooleanField(default=False, verbose_name="Skills available only to NPCs")
    unlock_at_level = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Required level to unlock")
    bonus_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Skill type (combat, dialog, environment...)")
    bonus_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Numerical value if needed (damages, skill bonus...)")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['character_class', 'unlock_at_level']

    def is_usable(self, character):
        return self.is_active and character.level >= self.unlock_at_level

    def __str__(self):
        return f"{self.name} ({self.character_class.name}, Lvl.{self.unlock_at_level})"

    # **Exemples :**
    # ```
    # Guerrier - Coup Puissant (Active, X DMG, Unlock Lvl 3)
    # Guerrier - Endurance (Passive, +10% HP, Unlock Lvl 5)
    # Mage - Boule de Feu (Active, X DMG, Unlock Lvl 3)
    # Voleur - Furtivité (Active, skip certain checks, Unlock Lvl 3)
    # ```

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class CharacterSkill(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="acquired_skills", verbose_name="Associated character" )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="characters", verbose_name="Skill")
    acquired_at = models.DateTimeField(auto_now_add=True, verbose_name="Acquisition date")
    acquired_level = models.IntegerField(default=0, verbose_name="Level at acquisition time")

    class Meta:
        unique_together = [['character', 'skill']]
        verbose_name = "Character skill"
        verbose_name_plural = "Character skills"
        ordering = ['acquired_level', 'skill__unlock_at_level']

    def clean(self):
        super().clean()

        if self.skill.character_class != self.character.character_class:
            raise ValidationError({
                'skill': f"The skill {self.skill.name} is reserved to {self.skill.character_class.name}, "
                         f"but you character is {self.character.character_class.name}."
            })
        
        if self.character.level < self.skill.unlock_at_level:
            raise ValidationError({
                'skill': f"You have to be level {self.skill.unlock_at_level} to unlock {self.skill.name}. "
                         f"You currently are level {self.character.level}."
            })

    def save(self, *args, **kwargs):
        if not self.pk:
            self.acquired_level = self.character.level
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.character.name} - {self.skill.name}"

class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Equipment name")
    description = models.TextField(verbose_name="Equipment description and lore")
    slot = models.CharField(max_length=20, verbose_name="Equipment type (weapon, relic, outfit)")
    rarity = models.CharField(max_length=20, verbose_name="Equipment rariry (common, rare, legendary)")
    primary_stat_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bonus type (xp bonus, narrative perk, combat bonus)")
    primary_stat_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Bonus value")
    secondary_stat_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Second bonus type (xp bonus, narrative perk, combat bonus)")
    secondary_stat_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Second bonus value")
    tertiary_stat_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Third bonus type (xp bonus, narrative perk, combat bonus)")
    tertiary_stat_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Third bonus value")
    required_level = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Level required wear the equipment")
    required_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, blank=True, null=True, related_name="equipments", verbose_name="Required class (NULL = all classes)")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"
        ordering = ['rarity', 'slot']

    def __str__(self):
        return f"{self.name} [{self.rarity}]"

    # **Slots :**
    # - `weapon` : Arme
    # - `armor` : Armure
    # - `relic` : Relique

    # **Rareté :**
    # - `common` : Commun (gris, 1 bonus)
    # - `rare` : Rare (bleu, 2 bonus)
    # - `legendary` : Légendaire (doré, 3 bonus)

    # Épée de Fer (weapon, common, Guerrier, +5% DMG)
    # Bâton Ancien (weapon, rare, Mage, +10% DMG)
    # Amulette du Sage (relic, legendary, Tous, +15% XP, +5% Stat principale)

class CharacterEquipment(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="owned_equipments", verbose_name="Character")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="characters", verbose_name="Equipment")
    is_equipped = models.BooleanField(default=False, verbose_name="Is currently equipped")
    acquired_at = models.DateTimeField(auto_now_add=True, verbose_name="Acquisition date")
    acquired_from = models.CharField(max_length=50, verbose_name="Source (level_up, adventure...)")

    class Meta:
        unique_together = [['character', 'equipment']]
        verbose_name = "Character equipment"
        verbose_name_plural = "Characters equipments"
        ordering = ['acquired_at']

    def __str__(self):
        status = "Equipped" if self.is_equipped else "Owned"
        return f"{self.character.name} - {self.equipment.name} [{status}]"

    def clean(self):
        super().clean()

        if self.character.level < self.equipment.required_level:
            raise ValidationError({
                'equipment': f"You have to be level {self.equipment.required_level} to equipe {self.equipment.name}. "
                             f"You are level {self.character.level}."
            })
        

        if self.equipment.required_class and self.equipment.required_class != self.character.character_class:
            raise ValidationError({
                'equipment': f"{self.equipment.name} is reserve to the {self.equipment.required_class.name} class, "
                             f"but you are {self.character.character_class.name}."
            })
        
        def save(self, *args, **kwargs):
            self.full_clean()
            super().save(*args, **kwargs)

        def __str__(self):
            status = "Equipped" if self.is_equipped else "In bags"
            return f"{self.character.name} - {self.equipment.name} [{status}]"


    # **Contraintes :**
    # - Paire `(character, equipment)` unique
    # - Un seul équipement équipé par slot (validation applicative)
    # - `equipment.required_level <= character.level`
    # - `equipment.required_class` compatible avec `character.character_class`


class Enemy(models.Model):
    name = models.CharField(max_length=100, verbose_name="Enemy name")
    description = models.TextField(blank=True, verbose_name="Description")
    hp = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Health points")
    min_damage = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Minimum damages")
    max_damage = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Maximum damages")
    skills = models.ManyToManyField(Skill, blank=True, related_name='enemies', verbose_name="Skills")
    is_boss = models.BooleanField(default=False, verbose_name="Is boss ?")
    reward = models.ForeignKey('adventures.Reward', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rewards")
    xp_reward = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="XP reward")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon")

    class Meta:
        verbose_name = "Enemy"
        verbose_name_plural = "Enemies"

    def __str__(self):
        return f"{self.name} ({'Boss' if self.is_boss else 'Ennemi'})"

    def get_damage_range(self):
        """Return a string describing the damage range."""
        return f"{self.min_damage}-{self.max_damage}"

    def get_random_damage(self):
        """Return random damages based on the damage range."""
        import random
        return random.randint(self.min_damage, self.max_damage)
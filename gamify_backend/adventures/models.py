from datetime import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint, Q

from users.models import CharacterClass, Character
from game.models import Enemy, Skill, Equipment, CharacterSkill

class Reward(models.Model):
    REWARD_TYPES = [
        ('xp', 'Experience Points'),
        ('item', 'Item'),
        ('skill', 'Skill'),
        ('currency', 'Currency'),
    ]

    type = models.CharField(max_length=10, choices=REWARD_TYPES, verbose_name="Reward type")
    value = models.IntegerField(verbose_name="Value (XP amount, item ID, etc.)")
    item = models.ForeignKey(Equipment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Item reward (if type=item)")
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Skill reward (if type=skill)")
    description = models.CharField(max_length=200, verbose_name="Reward description")

    def clean(self):
        if self.type == 'item' and not self.item:
            raise ValidationError("An item must be specified for item rewards.")
        if self.type == 'skill' and not self.skill:
            raise ValidationError("A skill must be specified for skill rewards.")

    def __str__(self):
        return f"{self.get_type_display()}: {self.description}"


class Adventure(models.Model):
    title = models.CharField(max_length=200, verbose_name="Adventure title")
    description = models.TextField(verbose_name="Adventure synopsis")
    min_level = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Level required")
    base_xp_reward = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Experience rewarded for completion")
    rewards = models.ManyToManyField(Reward, blank=True, related_name="adventures", verbose_name="Rewards for completing the adventure")
    difficulty = models.CharField(max_length=20, verbose_name="Difficulty (easy, medium, hard, legendary)")
    estimated_duration = models.IntegerField(blank=True, null=True, verbose_name="Estimated duration in minutes")
    is_published = models.BooleanField(default=False, verbose_name="Publish adventure")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last update")

    class Meta:
        verbose_name = "Aventure"
        verbose_name_plural = "Aventures"

    def save(self, *args, **kwargs):
        """Sauvegarde avec validation"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

#    **Exemple MVP :**
#     ```
#     Titre: "La Quête du Cristal Oublié"
#     Min Level: 1
#     XP Reward: 200
#     Difficulty: easy
#     Duration: 15 min
#     ``` 


class Scene(models.Model):
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE, related_name="scenes", verbose_name="Parent adventure")
    scene_order = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Order in adventure")
    title = models.CharField(max_length=200, verbose_name="Scene title")
    content = models.TextField(verbose_name="Narrative text")
    previous_scene = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Previous scene", related_name="next_scenes")
    next_scene = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Next scene (if no choice)", related_name="previous_scenes")
    is_starting_scene = models.BooleanField(default=False, verbose_name="Is opening scene")
    is_ending_scene = models.BooleanField(default=False, verbose_name="Is ending scene")
    is_fight_scene = models.BooleanField(default=False, verbose_name="Is combat scene")
    enemy = models.ForeignKey(Enemy, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Enemy (if fight scene)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    class Meta:
        ordering = ['scene_order']
        verbose_name = "Scene"
        verbose_name_plural = "Scenes"


    def clean(self):
        super().clean()

        if self.is_starting_scene:
            other_starting = Scene.objects.filter(
                adventure=self.adventure,
                is_starting_scene=True
            ).exclude(pk=self.pk)

            if other_starting.exists():
                other_scene = other_starting.first()
                raise ValidationError({
                    'is_starting_scene': f"A starting scene already exists: '{other_scene.title}'. "
                                        f"An adventure can only have one starting scene."
                })
            
        if self.scene_order is not None:
            other_scenes = Scene.objects.filter(
                adventure=self.adventure,
                scene_order=self.scene_order
            ).exclude(pk=self.pk)
        
            if other_scenes.exists():
                other_scene = other_scenes.first()  # Récupère la première scène en conflit
                raise ValidationError({
                    'scene_order': f"A scene with that order already exists: '{other_scene.title}'. "
                                  f"An adventure can only have one scene of that order."
                })

        if self.is_fight_scene and not self.enemy:
            raise ValidationError({
                'enemy': "A fight scene must have an enemy."
            })

        if self.is_fight_scene and self.is_ending_scene:
            raise ValidationError({
                'is_fight_scene': "Une scène de combat ne peut pas être une scène de fin."
            })

    # **Contraintes :**
    # - Une seule scène `is_starting_scene=True` par adventure
    # - Au moins une scène `is_ending_scene=True` par adventure

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        prefix = "✓ START" if self.is_starting_scene else ""
        prefix += " | END" if self.is_ending_scene else ""
        return f"{self.adventure.title} - {self.scene_order}: {self.title} {prefix}"
    

class SceneChoice(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="choices", verbose_name="Parent scene")
    text = models.CharField(max_length=500, verbose_name="Choice text")
    order = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Display order")
    next_scene = models.ForeignKey(Scene, blank=True, null=True, on_delete=models.SET_NULL, related_name="choices_leading_here", verbose_name="Next scene to play")
    required_class = models.ForeignKey(CharacterClass, blank=True, null=True, on_delete=models.SET_NULL, related_name="required_class_for_choices", verbose_name="Required class for choice")
    required_skill = models.ForeignKey(Skill, blank=True, null=True, on_delete=models.SET_NULL, related_name="required_skill_for_choices", verbose_name="Required skill")
    required_equipment = models.ForeignKey(Equipment, blank=True, null=True, on_delete=models.SET_NULL, related_name="required_equipment_for_choices", verbose_name="Equipment required")
    is_available = models.BooleanField(default=True, verbose_name="Is the choice available")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    class Meta:
        unique_together = [['scene', 'order']]
        ordering = ['scene', 'order']
        verbose_name = "Scene choice"
        verbose_name_plural = "Scene choices"
    
    def clean(self):
        super().clean()

        if self.scene.is_ending_scene and self.next_scene is not None:
            raise ValidationError({
                'next_scene': "A choice in an ending scene cannot have a next scene. "
                             "There is not next scene after an ending !"
            })
        
        if not self.scene.is_ending_scene and self.next_scene is None:
            raise ValidationError({
                'next_scene': "Vous devez spécifier une scène suivante (sauf si c'est une scène de fin)."
            })
        
        if self.next_scene and self.next_scene.adventure != self.scene.adventure:
            raise ValidationError({
                'next_scene': "La scène suivante doit être dans la MÊME adventure."
            })

    def is_available_for_character(self, character):
        """Check if the choice is available foir the character Useful to pass the information to the frontend to five visual feedback."""
        if self.required_class and self.required_class != character.character_class:
            return False
        if self.required_skill:
            has_skill = character.acquired_skills.filter(skill=self.required_skill).exists()
            if not has_skill:
                return False
        if self.required_equipment:
            has_equipment = character.owned_equipments.filter(equipment=self.required_equipment).exists()
            if not has_equipment:
                return False
        return True

    def unavailable_reason(self, character):
        """Return the reason as to why a choice is not available."""
        if self.required_class and self.required_class != character.character_class:
            return f"Require class : {self.required_class.name}"
        if self.required_skill:
            has_skill = character.acquired_skills.filter(skill=self.required_skill).exists()
            if not has_skill:
                return f"Require skill : {self.required_skill.name}"
        if self.required_equipment:
            has_equipment = character.owned_equipments.filter(equipment=self.required_equipment).exists()
            if not has_equipment:
                return f"Require equipment : {self.required_equipment.name}"
        return ""
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        next_label = self.next_scene.title if self.next_scene else "FIN"
        return f"{self.scene.title} → {self.text[:30]}... → {next_label}"


    # **Contraintes :**
    # - Paire `(scene, order)` unique
    # - Si `is_ending_scene=True` de la scène, `next_scene` doit être NULL

    # **Logique conditionnelle :**
    # - Si `required_class` défini : visible seulement si classe correspond
    # - Si `required_skill` défini : visible seulement si compétence acquise
    # - Si `required_equipment` défini : visible seulement si équipement possédé

class AdventureProgress(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="character_progressions", verbose_name="Character")
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE, related_name="progressions", verbose_name="Adventure")
    current_scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="progressed_scenes", verbose_name="Current scene")
    completed = models.BooleanField(default=False, verbose_name="Completed adventure")
    xp_earned = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Total xp earned")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Start date")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="Completion date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last update")

    class Meta:
        # Character can't have two simultaneous progression for a given adventure, once the adventure is over, the character can start it again
        constraints = [
            UniqueConstraint(
                fields=['character', 'adventure'],
                condition=Q(completed=False),  
                name='unique_active_progress_per_character'
            )
        ]

    def mark_as_completed(self):
        """Mark adventure as completed and update the associated field in the model."""
        if not self.current_scene.is_ending_scene:
            raise ValueError("Current scene is not the end scene.")

        self.completed = True
        self.completed_at = timezone.now()
        self.save()

    def clean(self):
        super().clean()
        if self.current_scene and self.current_scene.adventure != self.adventure:
            raise ValidationError({
                'current_scene': "Current scene must belong to the same adventure."
            })

    # **Contraintes :**
    # - Paire `(character, adventure)` unique si `completed=False`
    # - Permet plusieurs complétions (rejouabilité)

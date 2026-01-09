from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

# from users.models import Character

class ActivityType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Type name")
    category = models.CharField(max_length=50, verbose_name="Category(sport, leasure, work...)")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon name (lucide-react)")
    # requires_calories = models.BooleanField(default=False, verbose_name="Display calories field")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    class Meta:
        verbose_name = "Activity type"
        verbose_name_plural = "Activity types"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"
    
    # **Catégories MVP :**
    # - Sport
    # - Loisirs
    # - Créatif
    # - Vie quotidienne
    # - Travail
    # - Bricolages

    # **Exemples de types :**
    # - Sport : Musculation, Cardio, Yoga, Natation...
    # - Loisirs : Gaming, Lecture, Cinéma...
    # - Créatif : Dessin, Écriture, Photo...


class Activity(models.Model):
    """
    Activities registered by the Users
    """
    character = models.ForeignKey('users.Character', on_delete=models.CASCADE, related_name="activities", verbose_name="Associated character")
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT, verbose_name="Activity type", related_name="activity_logs")
    duration_minutes = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Duration in minutes")
    calories = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)],  verbose_name="Calories burned")
    satisfaction = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Satisfaction level")
    notes = models.TextField(blank=True, null=True, max_length=500, verbose_name="Optional commentary")
    xp_earned = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Experience earned")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['character', '-created_at']),
            models.Index(fields=['activity_type', '-created_at']),
        ]

    def clean(self):
        super().clean()
        if self.satisfaction < 1 or self.satisfaction > 10:
            raise ValidationError({
                'satisfaction': "Satisfaction must be between 1 and 10."
            })

    def __str__(self):
        return f"{self.character.name} - {self.activity_type.name} ({self.duration_minutes}min)"

    def calculate_xp(self):
        """Calc XP based on the duration and the character's multiplier"""
        base_xp = self.duration_minutes * 5
        return int(base_xp * self.character.xp_multiplier)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.xp_earned = self.calculate_xp()
        super().save(*args, **kwargs)
        
        if not self.pk:
            self.character.current_xp += self.xp_earned
            self.character.save()
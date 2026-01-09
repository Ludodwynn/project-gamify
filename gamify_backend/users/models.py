from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Create your models here.

class User(AbstractUser):
    """
    Utilisateur de l'application (extension Django User)
    """
    # Champs Django par défaut :
    # - username
    # - email
    # - password
    # - first_name
    # - last_name
    # - is_active
    # - is_staff
    # - is_superuser
    # - date_joined
    # - last_login
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Évite les conflits avec le modèle User par défaut
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permission_set',  # Évite les conflits avec le modèle User par défaut
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last update")

    def clean(self):
        super().clean()
        if not self.username:
            raise ValidationError("Username is mandatory.")
        if not self.email or not "@" in self.email:
            raise ValidationError("Email is mandatory and must be valid.")
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError("This email is already in use.")

    def can_create_character(self):
        """Verify if the user can create another character (max 3)."""
        return self.characters.count() < 3

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    

#########
class Race(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Race name")
    description = models.TextField(verbose_name="Race lore")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    class Meta:
        verbose_name = "Race"
        verbose_name_plural = "Races"
        ordering = ['name']

    def __str__(self):
        return self.name


#########
class CharacterClass(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Class name")
    description = models.TextField(verbose_name="Class description")
    primary_attribute = models.CharField(max_length=50, verbose_name="Primary attribute (Strength, Agility, Intelligence...)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    class Meta:
        verbose_name = "Character Class"
        verbose_name_plural = "Character Classes"
        ordering = ['name']

    def __str__(self):
        return self.name

#########
class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User related to character", related_name='characters')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    race = models.ForeignKey(Race, on_delete=models.PROTECT, verbose_name="Chosen race", related_name='race_characters')
    character_class = models.ForeignKey(CharacterClass, on_delete=models.PROTECT, verbose_name="Chosen class", related_name='class_characters')
    level = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Current level")
    hp = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Health points")
    mp = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Mana points")
    skill_points = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Skill points")
    current_xp = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Current experience")
    total_xp = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Total experience cumulated")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last update")
    is_active = models.BooleanField(default=True, verbose_name="Character currently selected")


    class Meta:
        unique_together = [['user', 'name']]
        ordering = ['-created_at']
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def clean(self):
        super().clean()
        
        # name can't be empty
        if not self.name or self.name.strip() == "":
            raise ValidationError({
                'name': 'Character name is mandatory.'
            })
        
        # verify unicity per user
        existing = Character.objects.filter(
            user=self.user,
            name=self.name
        ).exclude(pk=self.pk).exists()
        
        if existing:
            raise ValidationError({
                'name': f'You already have a character named "{self.name}"'
            })
        
        existing_characters = Character.objects.filter(user=self.user).count()
        if not self.pk and existing_characters >= 3:
            raise ValidationError("A user cannot have more than 3 characters.")

    def __str__(self):
        return f"{self.name} (Niv.{self.level})"

    @property
    def xp_for_next_level(self):
        """XP required for next level"""
        return self.level * 100

    @property
    def xp_multiplier(self):
        """Multiply XP gain based on currend level"""
        return 1.0 + (self.level - 1) * 0.1
    
    def toggle_active(self):
        self.is_active = not self.is_active
        self.save()
    
    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk:
            old_char = Character.objects.get(pk=self.pk)
            self.total_xp = old_char.total_xp + (self.current_xp - old_char.current_xp)
        else:
            self.total_xp = self.current_xp

        
        while self.current_xp >= self.xp_for_next_level:
            self.current_xp -= self.xp_for_next_level
            self.level += 1

        if self.pk:  # Si c'est une mise à jour
            old_char = Character.objects.get(pk=self.pk)
            if old_char.name != self.name:  # Si le nom a changé
                self.slug = self._generate_unique_slug()
        else:  # Nouvelle création
            if not self.slug:
                self.slug = self._generate_unique_slug()

        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        """Make a unique slug based on the character's name."""
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Character.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug


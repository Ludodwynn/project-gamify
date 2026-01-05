from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Activity

@receiver(post_save, sender=Activity)
def update_character_xp(sender, instance, created, **kwargs):
    """
    Met à jour l'XP du personnage après l'enregistrement d'une activité.
    """
    if created:  # Seulement pour les nouvelles activités
        character = instance.character
        character.current_xp += instance.xp_earned
        character.save()
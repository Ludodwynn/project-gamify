# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Character
# from .character_service import CharacterXPService

# @receiver(post_save, sender=Character)
# def handle_character_save(sender, instance, created, **kwargs):
#     """Signal : quand un Character est sauvegardé."""
    
#     if created:
#         print(f"Nouveau personnage créé : {instance.name}")
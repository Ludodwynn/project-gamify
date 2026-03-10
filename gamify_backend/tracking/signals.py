from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Activity

@receiver(post_save, sender=Activity)
def add_xp_to_character(sender, instance, created, **kwargs):
    if created:
        print(f"Signal triggered for Activity {instance.id}")
        print(f"Character XP before add: {instance.character.current_xp}")
        instance.character.add_xp(instance.xp_earned)
        print(f"Character XP after add: {instance.character.current_xp}")
        instance.character.refresh_from_db()
        print(f"Character XP after refresh: {instance.character.current_xp}")
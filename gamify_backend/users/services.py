from django.db.models.signals import post_save
from django.db import transaction
from users.models import Character

class CharacterService:
    @staticmethod
    def update_character_level(character, xp_amount):
        """Logique métier : ajouter XP et gérer level-up."""
        character.current_xp += int(xp_amount * character.xp_multiplier)
        
        while character.current_xp >= character.xp_for_next_level:
            character.current_xp -= character.xp_for_next_level
            character.level += 1
        
        character.save()
        return character
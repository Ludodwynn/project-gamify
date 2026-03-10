# from django.db import transaction
# from users.models import Character

# class CharacterXPService:
#     @staticmethod
#     @transaction.atomic
#     def add_xp(character, xp_gained):
#         """Ajoute de l'XP au personnage et gère les montées de niveau."""
#         character.current_xp += xp_gained
#         character.total_xp += xp_gained
#         CharacterXPService._check_level_up(character)
#         character.save(update_fields=['current_xp', 'total_xp', 'level'])

#     @staticmethod
#     def _check_level_up(character):
#         """Vérifie et applique les montées de niveau si nécessaire."""
#         while character.current_xp >= character.xp_for_next_level:
#             character.current_xp -= character.xp_for_next_level
#             character.level += 1
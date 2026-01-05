import random
from django.utils import timezone

from .models import CharacterEquipment, CharacterSkill

def resolve_fight(character, enemy):
    """
    Résout un combat entre un personnage et un ennemi.
    Retourne un dictionnaire avec le résultat du combat.
    """
    result = {
        'character_hp': character.hp,
        'enemy_hp': enemy.hp,
        'turns': 0,
        'winner': None,
        'xp_gained': 0,
        'rewards': [],
    }

    while result['character_hp'] > 0 and result['enemy_hp'] > 0:
        result['turns'] += 1

        # Tour du personnage
        damage_to_enemy = random.randint(1, character.level * 2)  # Exemple simple
        result['enemy_hp'] -= damage_to_enemy

        if result['enemy_hp'] <= 0:
            result['winner'] = 'character'
            result['xp_gained'] = enemy.xp_reward
            if enemy.reward:
                result['rewards'].append(enemy.reward)
            break

        # Tour de l'ennemi
        damage_to_character = enemy.get_random_damage()
        result['character_hp'] -= damage_to_character

        if result['character_hp'] <= 0:
            result['winner'] = 'enemy'
            break

    return result

def apply_fight_results(character, fight_result):
    """
    Applique les résultats du combat au personnage (XP, récompenses).
    """
    if fight_result['winner'] == 'character':
        character.xp += fight_result['xp_gained']
        character.save()

        # Appliquer les récompenses (ex: objets, compétences)
        for reward in fight_result['rewards']:
            if reward.type == 'xp':
                character.xp += reward.value
            elif reward.type == 'item':
                CharacterEquipment.objects.create(
                    character=character,
                    equipment=reward.item,
                    is_equiped=False
                )
            elif reward.type == 'skill':
                CharacterSkill.objects.create(
                    character=character,
                    skill=reward.skill,
                    acquired_level=character.level
                )

        character.save()
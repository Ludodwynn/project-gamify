from rest_framework import serializers
from .models import Enemy, Skill, CharacterSkill, Equipment, CharacterEquipment

class SkillSerializer(serializers.ModelSerializer):
    character_class = serializers.PrimaryKeyRelatedField(read_only=True)
    is_usable = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'character_class', 'skill_type', 'cooldown', 'is_active', 'is_npc_skill', 'unlock_at_level', 'bonus_type', 'bonus_value', 'icon', 'created_at']

    def get_is_usable(self, obj):
        character = self.context.get('character')
        if character:
            return obj.is_usable(character)
        return False


class CharacterSkillSerializer(serializers.ModelSerializer):
    character = serializers.PrimaryKeyRelatedField(read_only=True)
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = CharacterSkill
        fields = ['id', 'character', 'skill', 'acquired_at', 'acquired_level']


class EquipmentSerializer(serializers.ModelSerializer):
    character_class = serializers.PrimaryKeyRelatedField(read_only=True)
    is_equippable = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description', 'slot', 'rarity', 'primary_stat_type', 'primary_stat_value', 'secondary_stat_type', 'secondary_stat_value', 'tertiary_stat_type', 'tertiary_stat_value', 'required_level', 'required_class', 'icon', 'created_at', 'is_equippable']

    def get_is_equippable(self, obj):
        character = self.context.get('character')
        if character:
            return (character.level >= obj.required_level and
                    (not obj.required_class or obj.required_class == character.character_class))
        return False


class CharacterEquipmentSerializer(serializers.ModelSerializer):
    character = serializers.PrimaryKeyRelatedField(read_only=True)
    equipment_details = EquipmentSerializer(source='equipment', read_only=True)

    class Meta:
        model = CharacterEquipment
        fields = ['id', 'character', 'equipment', 'equipment_details ', 'is_equipped', 'acquired_at', 'acquired_from']


class EnemySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    damage_range = serializers.SerializerMethodField()

    class Meta:
        model = Enemy
        fields = ['id', 'name', 'description', 'hp', 'min_damage', 'max_damage', 'skills', 'is_boss', 'reward', 'xp_reward', 'icon']

    def get_damage_range(self, obj):
        return f"Damages range from {obj.min_damage} to {obj.max_damage}"
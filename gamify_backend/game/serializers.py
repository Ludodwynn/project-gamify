from rest_framework import serializers
from .models import Enemy, Skill

class EnemySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enemy
        fields = ['id', 'name', 'description', 'hp', 'min_damage', 'max_damage', 'is_boss', 'reward', 'xp_reward', 'icon', 'difficulty']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'skill_type', 'cooldown', 'icon']
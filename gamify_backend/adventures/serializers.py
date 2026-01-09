from rest_framework import serializers
from .models import Adventure, Scene, Reward, SceneChoice, AdventureProgress
from users.serializers import CharacterSerializer
from game.serializers import EnemySerializer, SkillSerializer, EquipmentSerializer

class RewardSerializer(serializers.ModelSerializer):
    """Serializer for the rewards, with conditional details depending on the rewards' type."""
    item_details = serializers.SerializerMethodField()
    skill_details = serializers.SerializerMethodField()

    class Meta:
        model = Reward
        fields = ['id', 'type', 'value', 'item', 'skill', 'description', 'item_details', 'skill_details']

    def get_item_details(self, obj):
        """Return details if the object is of type 'item'"""
        if obj.type == 'item' and obj.item:
            return {
                'id': obj.item.id,
                'name': obj.item.name,
                'description': obj.item.description,
                'type': obj.item.type,
            }
        return None

    def get_skill_details(self, obj):
        """Return details if the object is of type 'skill'"""
        if obj.type == 'skill' and obj.skill:
            return {
                'id': obj.skill.id,
                'name': obj.skill.name,
                'description': obj.skill.description,
                'level_required': obj.skill.level_required
            }
        return None


class AdventureSerializer(serializers.ModelSerializer):
    """Serializer for the adventures, with rewards and slug management."""
    rewards = RewardSerializer(many=True, read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Adventure
        fields = ['id', 'title', 'slug', 'description', 'min_level', 'base_xp_reward', 'difficulty', 'estimated_duration', 'is_published', 'rewards']

    def get_fields(self):
        fields = super().get_fields()
        if not self.context['request'].user.is_staff:
            fields.pop('is_published') 
        return fields
    

class LightSceneSerializer(serializers.ModelSerializer):
    """Light Serializer to avoid infinite loops."""
    class Meta:
        model = Scene
        fields = ['id', 'title', 'scene_order']


class SceneSerializer(serializers.ModelSerializer):
    """Serializer for the scenes, with circular relation handling and combat management."""
    adventure = serializers.PrimaryKeyRelatedField(read_only=True)
    next_scene = LightSceneSerializer(read_only=True)
    previous_scene = serializers.PrimaryKeyRelatedField(read_only=True)
    enemy = EnemySerializer(read_only=True)

    class Meta:
        model = Scene
        fields = ['id', 'adventure', 'slug', 'scene_order', 'title', 'content', 'is_starting_scene', 'is_ending_scene', 'is_fight_scene', 'enemy', 'next_scene']


class SceneChoiceSerializer(serializers.ModelSerializer):
    next_scene = serializers.PrimaryKeyRelatedField(read_only=True)
    is_available = serializers.SerializerMethodField()
    unavailable_reason = serializers.SerializerMethodField()

    class Meta:
        model = SceneChoice
        fields = ['scene', 'text', 'order', 'next_scene', 'required_class', 'required_skill', 'required_equipment', 'is_available', 'created_at']

    def get_is_available(self, obj):
        character = self.context.get('character')
        if character:
            return obj.is_available_for_character(character)
        return False

class AdventureProgressSerializer(serializers.ModelSerializer):
    character = CharacterSerializer(read_only=True)
    adventure = AdventureSerializer(read_only=True)
    current_scene = SceneSerializer(read_only=True)
    duration = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = AdventureProgress
        fields = ['id', 'character', 'adventure', 'current_scene', 'completed', 'xp_earned', 'started_at', 'completed_at', 'updated_at', 'duration', 'progress_percentage']

    def get_duration(self, obj):
        if obj.completed_at and obj.started_at:
            duration_seconds = (obj.completed_at - obj.started_at).total_seconds()
            return duration_seconds / 60
        return None
    
    def get_progress_percentage(self, obj):
        if obj.adventure and obj.adventure.scenes.count() > 0:
            current_scene_order = obj.current_scene.scene_order if obj.current_scene else 0
            total_scenes = obj.adventure.scenes.count()
            return (current_scene_order / total_scenes) * 100
        return 0
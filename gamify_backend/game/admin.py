from django.contrib import admin

from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html

from adventures.models import Scene
from .models import Skill, CharacterSkill, Equipment, CharacterEquipment, Enemy

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'character_class', 'skill_type', 'cooldown', 'unlock_at_level', 'is_active', 'is_npc_skill')
    list_filter = ('character_class', 'skill_type', 'is_active', 'is_npc_skill', 'unlock_at_level')
    search_fields = ('name', 'description', 'bonus_type')


@admin.register(CharacterSkill)
class CharacterSkillAdmin(admin.ModelAdmin):
    list_display = ('character_link', 'skill_link', 'acquired_at', 'acquired_level')
    list_filter = ('skill__character_class', 'acquired_level')
    search_fields = ('character__name', 'skill__name')

    def character_link(self, obj):
        url = reverse('admin:users_character_change', args=[obj.character.id])
        return format_html('<a href="{}">{}</a>', url, obj.character.name)
    character_link.short_description = 'Character'

    def skill_link(self, obj):
        url = reverse('admin:game_skill_change', args=[obj.skill.id])
        return format_html('<a href="{}">{}</a>', url, obj.skill.name)
    character_link.short_description = 'Skill'


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'rarity',  'required_level', 'required_class')
    list_filter = ('slot', 'rarity', 'required_level', 'required_class')
    search_fields = ('name', 'description')


@admin.register(CharacterEquipment)
class CharacterEquipmentAdmin(admin.ModelAdmin):
    list_display = ('character_link', 'equipment_link', 'is_equipped', 'acquired_at', 'acquired_from')
    list_filter = ('is_equipped', 'equipment__slot', 'equipment__rarity', 'equipment__required_class')
    search_fields = ('character__name', 'equipment__name', 'acquired_from')
    actions = ['mark_as_equiped', 'mark_as_unequiped']

    def character_link(self, obj):
        url = reverse('admin:users_character_change', args=[obj.character.id])
        return format_html('<a href="{}">{}</a>', url, obj.character.name)
    character_link.short_description = 'Character'

    def equipment_link(self, obj):
        url = reverse('admin:game_equipment_change', args=[obj.equipment.id])
        return format_html('<a href="{}">{}</a>', url, obj.equipment.name)
    character_link.short_description = 'Equipment'

    @admin.action(description='Mark as equipped')
    def mark_as_equiped(self, request, queryset):
        queryset.update(is_equipped=True)

    @admin.action(description='Mark as unequipped')
    def mark_as_unequiped(self, request, queryset):
        queryset.update(is_equipped=False)


class AdventureFilter(admin.SimpleListFilter):
    title = 'Adventure'
    parameter_name = 'adventure'

    def lookups(self, request, model_admin):
        Scene = apps.get_model('adventures', 'Scene')
        Adventure = apps.get_model('adventures', 'Adventure')

        adventures = set()
        for scene in Scene.objects.filter(enemy__isnull=False):
            adventures.add((scene.adventure.id, scene.adventure.title))
        return sorted(adventures, key=lambda x: x[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(scene__adventure__id=self.value())
        return queryset

@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    list_display = ('name', 'hp', 'damage_range', 'is_boss', 'get_skills', 'get_reward', 'get_scenes_link')
    list_filter = ('is_boss', 'reward__type')
    search_fields = ('name', 'reward__description')

    def damage_range(self, obj):
        """Show the damage range."""
        return f"{obj.min_damage}-{obj.max_damage}"
    damage_range.short_description = 'Dégâts'

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        list_filter = list(list_filter) + [AdventureFilter]
        return list_filter

    def get_skills(self, obj):
        """Return a string with the names of the enemy's skills."""
        return ", ".join([skill.name for skill in obj.skills.all()]) if obj.skills.exists() else "-"
    get_skills.short_description = 'Skills'

    def get_reward(self, obj):
        """Show associated reward."""
        if obj.reward:
            return obj.reward.description
        return "-"
    get_reward.short_description = 'Reward'

    def get_scenes_link(self, obj):
        """Show the link toward the scenes associated with this enemy."""
        scenes = obj.scene_set.all()
        if scenes.exists():
            scene_links = []
            for scene in scenes:
                url = reverse('admin:adventures_scene_change', args=[scene.id])
                scene_links.append(f'<a href="{url}">{scene.title}</a>')
            return format_html("<br>".join(scene_links))
        return "-"
    get_scenes_link.short_description = 'Associated scenes'




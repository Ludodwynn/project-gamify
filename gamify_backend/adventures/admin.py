from datetime import timezone
from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from .models import Reward, Adventure, Scene, SceneChoice, AdventureProgress


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('type', 'value', 'get_item', 'get_skill', 'description')
    list_filter = ('type',)
    search_fields = ('description',)

    def get_item(self, obj):
        return obj.item.name if obj.item else "-"
    get_item.short_description = 'Item'

    def get_skill(self, obj):
        return obj.skill.name if obj.skill else "-"
    get_skill.short_description = 'Skill' 

@admin.register(Adventure)
class AdventureAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'min_level', 'estimated_duration')
    list_filter = ('difficulty', 'estimated_duration', 'is_published')
    search_fields = ('title', 'description')
    filter_horizontal = ('rewards',)
    actions = ['publish_adventures', 'unpublish_adventures']

    @admin.action(description='Publish selectionned adventures')
    def publish_adventures(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} published adventures.")

    @admin.action(description='Unpublish selectionned adventures')
    def unpublish_adventures(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} unpublished adventures.")


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('adventure', 'scene_order', 'title', 'is_starting_scene', 'is_ending_scene', 'is_fight_scene', 'previous_scene_link', 'next_scene_link')
    list_filter = ('adventure', 'is_starting_scene', 'is_ending_scene', 'is_fight_scene')
    search_fields = ('adventure__title', 'title', 'content')
    ordering = ('adventure', 'scene_order')

    def previous_scene_link(self, obj):
        """Display a link to create a new scene linked to the current scene."""
        if obj.previous_scene:
            url = reverse('admin:adventures_scene_change', args=[obj.previous_scene.id])
            return format_html('<a href="{}">{}</a>', url, obj.previous_scene.title)
        else:
            return "-"
    previous_scene_link.short_description = 'Scène précédente'

    def next_scene_link(self, obj):
        url = reverse('admin:adventures_scene_add')
        params = f"?previous_scene={obj.id}"
        return format_html('<a href="{}{}">Create next scene</a>', url, params)
    next_scene_link.short_description = 'Create next scene'

    def get_next_scene_order(self, adventure):
        """Return the number for the next scene for a given adventure."""
        max_order = Scene.objects.filter(adventure=adventure).aggregate(models.Max('scene_order'))['scene_order__max']
        return max_order + 1 if max_order is not None else 1

    def get_form(self, request, obj=None, **kwargs):
        """Customize the forme to include a previous_scene field, an automatically fill the scene_order field when creating a new scene."""
        form = super().get_form(request, obj, **kwargs)
        
        adventure = None
        if 'adventure' in request.GET:
            adventure_id = request.GET.get('adventure')
            try:
                adventure = Adventure.objects.get(id=adventure_id)
            except Adventure.DoesNotExist:
                pass
        elif 'previous_scene' in request.GET and obj is None:
            previous_scene_id = request.GET.get('previous_scene')
            try:
                previous_scene = Scene.objects.get(id=previous_scene_id)
                adventure = previous_scene.adventure
                form.base_fields['previous_scene'].initial = previous_scene
            except Scene.DoesNotExist:
                pass

        if adventure:
            form.base_fields['adventure'].initial = adventure
            form.base_fields['scene_order'].initial = self.get_next_scene_order(adventure)

        return form

    def response_add(self, request, obj, post_url_continue=None):
        """Redirect to the parent scene after adding a new scene."""
        if 'previous_scene' in request.GET:
            previous_scene_id = request.GET.get('previous_scene')
            return HttpResponseRedirect(reverse('admin:adventures_scene_change', args=[previous_scene_id]))
        return super().response_add(request, obj, post_url_continue)

@admin.register(SceneChoice)
class SceneChoiceAdmin(admin.ModelAdmin):
    list_display = ('scene', 'text', 'next_scene', 'required_class', 'required_skill', 'required_equipment')
    list_filter = ('scene', 'required_class', 'required_skill', 'required_equipment')
    search_fields = ('text', 'scene__title')


@admin.register(AdventureProgress)
class AdventureProgressAdmin(admin.ModelAdmin):
    list_display = ('character', 'adventure', 'current_scene', 'completed', 'xp_earned', 'started_at', 'completed_at')
    list_filter = ('character', 'adventure', 'completed')
    search_fields = ('character__name', 'adventure__title')
    actions = ['mark_as_completed']

    @admin.action(description='Marquer comme complété')
    def mark_as_completed(self, request, queryset):
        queryset.update(completed=True, completed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} adventure marked as completed.")



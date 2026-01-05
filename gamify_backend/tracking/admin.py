from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import Activity, ActivityType

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'character_link', 'activity_type', 'duration_formatted', 'calories', 'satisfaction', 'xp_earned', 'created_at')
    list_filter = ('activity_type', 'character__user', 'created_at')
    search_fields = ('character__name', 'activity_type__name', 'notes')

    ordering = ('-created_at',)

    def character_link(self, obj):
        url = reverse('admin:users_character_change', args=[obj.character.id])
        return format_html('<a href="{}">{}</a>', url, obj.character.name)
    character_link.short_description = 'Character'

    def duration_formatted(self, obj):
        hours = obj.duration_minutes // 60
        minutes = obj.duration_minutes % 60
        return f"{hours}h {minutes}min" if hours > 0 else f"{minutes}min"
    duration_formatted.short_description = 'Duration'

    @admin.action(description='Mark selected activites as validated')
    def mark_as_validated(modeladmin, request, queryset):
        queryset.update(is_validated=True)
    actions = [mark_as_validated]


admin.site.register(ActivityType)


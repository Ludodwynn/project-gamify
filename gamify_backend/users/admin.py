from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import User, Race, CharacterClass, Character

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'character_count', 'characters_link', 'slug')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')

    def character_count(self, obj):
        return obj.characters.count()
    character_count.short_description = 'Nombre de personnages'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    readonly_fields = ('date_joined', 'created_at', 'updated_at', 'last_login')

    def characters_link(self, obj):
        url = reverse('admin:users_character_changelist') + f'?user__id__exact={obj.id}'
        # print("URL générée :", url)
        return format_html('<a href="{}">Voir les personnages ({})</a>', url, obj.characters.count())
    
    characters_link.short_description = 'Characters'
    


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'race', 'character_class', 'level', 'is_active', 'slug')
    list_filter = ('race', 'character_class', 'is_active')
    search_fields = ('name', 'user__username')



admin.site.register(User, CustomUserAdmin)
admin.site.register(Race)
admin.site.register(CharacterClass)


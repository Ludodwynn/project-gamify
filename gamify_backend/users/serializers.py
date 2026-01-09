from rest_framework import serializers
from .models import User, Race, CharacterClass, Character
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
        }
    
    def create(self, validated_data):
        """Create a user with a hashed password."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update a user, hash the password if given."""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_email(self, value):
        """Validate that email is unique."""
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A user with this mail already exists.")
        return value
    
    def validate_username(self, value):
        """Validate that username is unique"""
        if User.objects.filter(username=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['id', 'name', 'description', 'created_at']


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = ['id', 'name', 'description', 'primary_attribute', 'created_at']


class CharacterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    race = RaceSerializer(read_only=True)
    character_class = CharacterClassSerializer(read_only=True)

    class Meta:
        model = Character
        fields = ['id', 'user', 'name', 'slug', 'race', 'character_class', 'level', 'hp', 'mp', 'skill_points', 'current_xp', 'total_xp', 'created_at', 'updated_at', 'is_active']
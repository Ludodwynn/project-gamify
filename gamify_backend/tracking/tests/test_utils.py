# tracking/tests/test_utils.py
from django.test.signals import setting_changed
from django.db.models.signals import post_save

def disable_signals():
    post_save.receivers = []

def enable_signals():
    from tracking import signals  # Réactive les signaux

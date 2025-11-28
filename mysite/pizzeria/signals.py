from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Пример логирующего сигнала на создание/удаление (опционально)
@receiver(post_save)
def log_create_update(sender, instance, created, **kwargs):
    # пропускаем встроенные таблицы
    name = sender.__name__
    if name in ('Session','LogEntry','Permission'):
        return
    if created:
        print(f"[SIGNAL] Created {sender.__name__} id={getattr(instance,'id',None)}")
    else:
        print(f"[SIGNAL] Updated {sender.__name__} id={getattr(instance,'id',None)}")

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    name = sender.__name__
    if name in ('Session','LogEntry','Permission'):
        return
    print(f"[SIGNAL] Deleted {sender.__name__} id={getattr(instance,'id',None)}")

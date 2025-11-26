from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType


# ------- 1. Сигнал при создании или удалении записи в админке -------
@receiver(post_save)
def on_create_record(sender, instance, created, **kwargs):
    # Пропускаем системные модели Django
    if sender.__name__ in ['LogEntry', 'Session', 'Permission']:
        return

    if created:
        print(f"[SIGNAL] Создана новая запись: {sender.__name__} (ID={instance.id})")
    else:
        print(f"[SIGNAL] Запись обновлена: {sender.__name__} (ID={instance.id})")


@receiver(post_delete)
def on_delete_record(sender, instance, **kwargs):
    if sender.__name__ in ['LogEntry', 'Session', 'Permission']:
        return

    print(f"[SIGNAL] Удалена запись: {sender.__name__} (ID={instance.id})")



# ------- 2. Сигнал при создании суперпользователя -------
@receiver(post_save, sender=User)
def on_superuser_created(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        print(f"[SIGNAL] Создан суперпользователь: {instance.username}")

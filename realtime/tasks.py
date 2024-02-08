# Create your tasks here

from website.models import User

from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def count_users():
    return User.objects.count()


@shared_task
def rename_user(user_id, name):
    w = User.objects.get(user_id=user_id)
    w.name = name
    w.save()

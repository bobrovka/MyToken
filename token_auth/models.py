from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4


class Token(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    key = models.CharField(max_length=36)


def generate_token():
    hash_str = str(uuid4())
    while Token.objects.filter(key=hash_str):
        hash_str = str(uuid4())
    return hash_str


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance, key=generate_token())
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class FollowAuthor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower', verbose_name='Подписчик')
    authors = models.ManyToManyField(
        User, related_name='following', verbose_name='Избранный автор')

    class Meta:
        verbose_name = "Подписка на автора"
        verbose_name_plural = "Подписки на авторов"

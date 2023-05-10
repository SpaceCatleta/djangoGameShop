# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class GameDetail(models.Model):
    label = models.CharField(max_length=100)
    cover = models.ImageField('Обложка игры', upload_to='game_covers')
    release_date = models.DateField('дата выхода')
    price = models.DecimalField(verbose_name='Цена',  max_digits=10, decimal_places=2, default=0)

    developer = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)


    def __str__(self):
        return f'{self.label}, {self.release_date}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    balance = models.DecimalField(verbose_name='Баланс',  max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user}, {self.balance}'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class UsersGames(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    game = models.ForeignKey(GameDetail, verbose_name='Игра', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}, {self.game}'

    class Meta:
        verbose_name = 'Игра пользователя'
        verbose_name_plural = 'Игры пользователей'


class UserChart(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    game = models.ForeignKey(GameDetail, verbose_name='Игра', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}, {self.game}'

    class Meta:
        verbose_name = 'Игра в корзине пользователя'
        verbose_name_plural = 'Игры в корзине пользователей'
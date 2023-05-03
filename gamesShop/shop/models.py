# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone


class GameDetail(models.Model):
    label = models.CharField(max_length=100)
    cover = models.ImageField('Обложка игры', upload_to='game_covers')
    release_date = models.DateField('дата выхода')

    developer = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    game_version = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)


    def __str__(self):
        return f'{self.label}, {self.release_date}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
from django.contrib import admin
from .models import GameDetail, UserProfile, UsersGames, UserChart


class GameDetailAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Main info', {'fields': ['label', 'cover', 'release_date', 'price']}),
        ('More information', {'fields': ['developer', 'publisher', 'description']}),
    ]
admin.site.register(GameDetail, GameDetailAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


@admin.register(UsersGames)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'game')


@admin.register(UserChart)
class UserChartAdmin(admin.ModelAdmin):
    list_display = ('user', 'game')

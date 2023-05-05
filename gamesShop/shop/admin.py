from django.contrib import admin
from .models import GameDetail


class GameDetailAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Main info', {'fields': ['label', 'cover', 'release_date']}),
        ('More information', {'fields': ['developer', 'publisher', 'description']}),
    ]


admin.site.register(GameDetail, GameDetailAdmin)
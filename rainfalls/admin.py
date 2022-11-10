from django.contrib import admin
from .models import Rainfall


@admin.register(Rainfall)
class RainfallAdmin(admin.ModelAdmin):
    pass

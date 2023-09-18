from django.contrib import admin
from .models import Place, PlaceImage


class PlaceImageAdminInline(admin.TabularInline):
    model = PlaceImage


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = (PlaceImageAdminInline,)


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    ...

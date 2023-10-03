from django.contrib import admin
from .models import Place, PlaceImage


class PlaceImageAdminInline(admin.TabularInline):
    model = PlaceImage
    verbose_name = 'Фотография'
    verbose_name_plural = 'Фотографии'
    model.image.field.verbose_name = 'Фото'
    model.__str__ = lambda _: ''


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = (PlaceImageAdminInline,)


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    ...

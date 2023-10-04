from django.contrib import admin
from .models import Place, PlaceImage
from django.utils.html import format_html


class PlaceImageAdminInline(admin.TabularInline):
    model = PlaceImage
    verbose_name = 'Фотография'
    verbose_name_plural = 'Фотографии'
    model.image.field.verbose_name = 'Фото'
    model.__str__ = lambda _: ''

    readonly_fields = ['preview']

    def preview(self, obj):
        try:
            return format_html(f'<img src="{obj.image.url}" height="50">')
        except Exception as e:
            print(e)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = (PlaceImageAdminInline,)


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    ...

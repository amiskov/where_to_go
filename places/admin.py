from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .models import Place, PlaceImage


class PlaceImageAdminInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    verbose_name = 'Фотография'
    verbose_name_plural = 'Фотографии'
    model.image.field.verbose_name = 'Фото'
    model.__str__ = lambda _: ''
    extra = 0

    readonly_fields = ['preview']

    def preview(self, obj):
        try:
            return format_html(f'<img src="{obj.image.url}" height="50">')
        except Exception as e:
            print(e)


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    search_fields = ['title', 'short_description', 'long_description']
    inlines = (PlaceImageAdminInline,)


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ['place', 'image', 'position']

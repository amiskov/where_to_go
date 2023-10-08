import logging

from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .models import Place, PlaceImage

logger = logging.getLogger(__name__)


class PlaceImageAdminInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    verbose_name = 'Фотография'
    verbose_name_plural = 'Фотографии'
    model.image.field.verbose_name = 'Фото'
    model.__str__ = lambda _: ''
    extra = 0

    readonly_fields = ['preview']

    def preview(self, place_image):
        img = '<img src="{}" style="max-height: 200px; max-width: 200px">'
        return format_html(img, place_image.image.url)


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    search_fields = ['title', 'short_description', 'long_description']
    inlines = (PlaceImageAdminInline,)


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ['place', 'image', 'position']
    autocomplete_fields = ['place']

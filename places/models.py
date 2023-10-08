from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    short_description = models.TextField('Короткое описание', blank=True)
    long_description = HTMLField('Полное описание', blank=True)
    lat = models.DecimalField('Широта (lat)', max_digits=16, decimal_places=14)
    lon = models.DecimalField('Долгота (lon)', max_digits=16,
                              decimal_places=14)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(Place, related_name='images',
                              verbose_name='Место',
                              on_delete=models.CASCADE)
    image = models.ImageField('Картинка',)
    position = models.PositiveIntegerField('Порядковый номер', default=0,
                                           blank=False, null=False,
                                           db_index=True)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии мест'
        ordering = ['position']
        unique_together = ('place', 'image')

    def __str__(self):
        return f'{self.image} из {self.place.title}'

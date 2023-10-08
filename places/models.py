from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    description_short = models.CharField('Короткое описание', max_length=256)
    description_long = HTMLField('Полное описание')
    lat = models.DecimalField('Широта (lat)', max_digits=16, decimal_places=14)
    lon = models.DecimalField('Долгота (lon)', max_digits=16,
                              decimal_places=14)

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Картинка',)
    position = models.IntegerField('Позиция')

    class Meta:
        ordering = ['position']
        unique_together = ('place', 'image')

    def __str__(self):
        return f'{self.image} из {self.place.title}'

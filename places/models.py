from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=128)
    description_short = models.CharField('Короткое описчание', max_length=256)
    description_long = models.TextField('Полное описание')
    lat = models.DecimalField('Широта (lat)', max_digits=16, decimal_places=14)
    lon = models.DecimalField('Долгота (lon)', max_digits=16,
                              decimal_places=14)

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Картинка')
    position = models.IntegerField('Позиция')

    def __str__(self):
        return f'Картинка {self.position} для {self.place.title}'
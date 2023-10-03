from django.forms.models import model_to_dict
from django.views.generic import TemplateView, View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from places.models import Place


class PlaceView(View):
    def get(self, request, pk):
        place_qs = Place.objects.filter(pk=pk).prefetch_related('images')
        place = get_object_or_404(place_qs)
        place_dict = model_to_dict(place)
        place_dict['imgs'] = [img.image.url for img in place.images.all()]
        return JsonResponse(place_dict)


class IndexView(TemplateView):
    def get(self, request):
        places = Place.objects.all()
        features = []
        for place in places:
            print(place.title)
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.lon, place.lat]
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.pk,
                    "detailsUrl": f'places/{place.pk}'
                },
            })
        data = {
            "type": "FeatureCollection",
            "features": features
        }

        context = {
            'data': data
        }
        return render(request, 'index.html', context=context)

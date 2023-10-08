from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, resolve_url
from django.views.generic import TemplateView, View

from places.models import Place


class PlaceView(View):
    def get(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        serialized_place = model_to_dict(place)
        serialized_place['imgs'] = [img.image.url for img in place.images.all()]
        return UTF8JsonResponse(serialized_place)


class IndexView(TemplateView):
    def get(self, request):
        places = Place.objects.all()
        features = []
        for place in places:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.lon, place.lat]
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.pk,
                    "detailsUrl": resolve_url('place', pk=place.pk)
                },
            })
        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }

        context = {
            'feature_collection': feature_collection
        }
        return render(request, 'index.html', context=context)


class UTF8JsonResponse(JsonResponse):
    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {"ensure_ascii": False,
                             **(json_dumps_params or {})}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)

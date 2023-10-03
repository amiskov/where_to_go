from django.urls import path

from .views import IndexView, PlaceView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('places/<int:pk>/', PlaceView.as_view(), name='place'),
]

import logging

import backoff
import requests
from django.conf import settings
from django.core.files.base import ContentFile

from places.models import Place, PlaceImage


def create_place(url: str) -> Place:
    """Creates and saves place alongside with photos."""
    logging.info(f'\nLoading {url}')
    resp = requests.get(url)
    resp.raise_for_status()
    place_content = resp.json()

    place, _ = Place.objects.get_or_create(
        title=place_content['title'],
        defaults={
            'short_description': place_content['description_short'],
            'long_description': place_content['description_long'],
            'lat': place_content['coordinates']['lat'],
            'lon': place_content['coordinates']['lng'],
        }
    )
    create_place_images(place, place_content['imgs'])
    return place


def create_place_images(place: Place, image_urls: list[str]):
    """Create PlaceImages from `image_urls` and save them for `place`."""
    position = 0
    for image_url in image_urls:
        filename = image_url.split('/')[-1]

        if not is_image(filename):
            logging.error(f'{filename} is not an image, skipping.')
            continue

        try:
            image_bytes = download_image(image_url)
            place_image, _ = PlaceImage.objects.get_or_create(place=place,
                                                              position=position,)
            place_image.image.save(filename, ContentFile(image_bytes))
            position += 1
        except requests.HTTPError as e:
            logging.error(f'Failed to load {image_url}: {e}')
    return place


@backoff.on_exception(backoff.expo,
                      (requests.ConnectionError, requests.Timeout))
def download_image(url: str) -> bytes:
    """Download an image by `url` to `dir`.

    `url` must have a file extension at the end (`.png`, `.jpg`, etc).
    """
    response = requests.get(url)
    response.raise_for_status()

    images_path = settings.MEDIA_ROOT
    images_path.mkdir(exist_ok=True)

    filename = url.split('/')[-1]
    image_fullpath = images_path.joinpath(filename)
    if image_fullpath.exists():
        logging.warn(f'{filename} already exists.')
        return image_fullpath.read_bytes()
    return response.content


def is_image(file_name: str) -> bool:
    return file_name.lower().endswith(('.jpg', '.jpeg', '.gif', '.png'))

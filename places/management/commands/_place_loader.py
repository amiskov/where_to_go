import requests
import logging
from django.conf import settings
from places.models import Place, PlaceImage
from django.core.files.base import ContentFile


def create_place(url: str) -> Place:
    """Creates and saves place alongside with photos."""
    logging.info(f'\nLoading {url}')
    resp = requests.get(url)
    resp.raise_for_status()
    place_content = resp.json()

    place, _ = Place.objects.get_or_create(
        title=place_content['title'],
        description_short=place_content['description_short'],
        description_long=place_content['description_long'],
        lat=place_content['coordinates']['lat'],
        lon=place_content['coordinates']['lng'],
    )

    position = 0
    for image_url in place_content['imgs']:
        filename = image_url.split('/')[-1]
        if not is_image(filename):
            logging.error(f'{filename} is not an image, skipping.')
            continue

        img_content = download_image(image_url)

        place_image, _ = PlaceImage.objects.get_or_create(
            place=place, position=position,)

        place_image.image.save(filename, ContentFile(img_content))

        logging.info(f'PlaceImage created: {str(place_image)}')
        position += 1

    return place


def download_image(url: str, params=None) -> bytes:
    """Download an image by `url` to `dir`.

    `url` must have a file extension at the end (`.png`, `.jpg`, etc).
    """
    response = requests.get(url, params=params)
    response.raise_for_status()

    images_path = settings.MEDIA_ROOT
    images_path.mkdir(exist_ok=True)

    filename = url.split('/')[-1]
    image_fullpath = images_path.joinpath(filename)
    if image_fullpath.exists():
        logging.info(f'{filename} already exists.')
        return image_fullpath.read_bytes()
    return response.content


def is_image(file_name: str) -> bool:
    return file_name.lower().endswith(('.jpg', '.jpeg', '.gif', '.png'))

"""Classes assisting with image retrieval via the API."""

import enum
from typing import Dict

import yarl

from .census import Query
from .client import Client
from .request import extract_payload, run_query

IMAGE_ENDPOINT = 'https://census.daybreakgames.com/files/ps2/images/static'


class ImageSize(enum.Enum):
    """Enumerates the API image sizes.

    Note that these may not match the actual image size exactly,
    especially for non-square images.

    The following is a list of the enum values and their corresponding
    size in pixels:

        ImageSize.ExtremelySmall  #   8 pixel height
        ImageSize.VerySmall       #  16 pixel height
        ImageSize.Small           #  32 pixel height
        ImageSize.Medium          #  64 pixel height
        ImageSize.Large           # 128 pixel height
        ImageSize.VeryLarge       # 256 pixel height
        ImageSize.Massive         # no size limit

    """
    # NotYetUsed_1 = 1  # Missing load screen assets
    # NotYetUsed_2 = 2  # Missing load screen assets
    ExtremelySmall = 3
    VerySmall = 4
    Small = 5
    Medium = 6
    Large = 7
    VeryLarge = 8
    Unspecified = 9  # Default value? Lots of random stuff has this type
    Massive = 10


class CensusImage:
    """Represents an image asset in the Census API.

    Note that not all images represented by the API actually exist.

    """

    def __init__(self, image_set_id: int, client: Client) -> None:
        self._client = client
        self._fetched = False
        self.set_id = image_set_id
        self._images: Dict[ImageSize, int] = {}

    async def _fetch(self) -> None:
        """Retrieve the image set members for this image."""
        query = Query(collection='image_set',
                      service_id=self._client.service_id,
                      image_set_id=self.set_id).limit(20)
        payload = await run_query(query, session=self._client.session)
        data = extract_payload(payload, 'image_set')
        self._images = {}
        for image_dict in data:
            assert int(image_dict['image_set_id']) == self.set_id
            image_id = int(image_dict['image_id'])
            type_id = int(image_dict['type_id'])
            self._images[ImageSize(type_id)] = image_id
        self._fetched = True

    async def url(self, size: ImageSize = ImageSize.Large) -> yarl.URL:
        """Generate the URL for a given asset.

        Note that this will query the API if the image set members have
        not yet been retrieved.

        Args:
            size (optional): The preferred size of the image, or the
                closest size to it. Defaults to ImageSize.Large.

        Returns:
            The URL object the image can be retrieved with.

        """
        if not self._fetched:
            await self._fetch()
        assert self._images
        size_id = size.value
        # Move outwards from the target size
        offset = 0
        while True:
            try:
                image_id = self._images[ImageSize(size_id+offset)]
            except KeyError:
                pass
            except ValueError:
                if abs(offset) > 10:
                    break
            else:
                break
            if offset > 0:
                offset -= offset*2
            else:
                offset -= offset*2 - 1
            print(offset)
        assert size_id != 0
        url = yarl.URL(IMAGE_ENDPOINT)
        url /= f'{image_id}.png'
        return url

from ..census import Query
from ..datatypes import InterimDatatype
from .image import Image, ImageSet

# from .item import Item
# from .reward import Reward
# from .objective import ObjectiveSet


class Achievement(InterimDatatype):
    """An achievement in PlanetSide 2.

    An achievement is a blanket term covering both weapon medals and service
    ribbons.

    """

    # Since achievements are quite light-weight and cannot be resolved further,
    # their cache size can be safely increased.
    _cache_size = 100
    _collection = 'achievement'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        # Fields set to equal "None" are references to other data types that
        # have not yet been implemented.
        self.description = data['description'][next(iter(data['description']))]
        self.item = None
        self.image = Image(data['image_id'], path=data['image_path'])
        self.image_set = ImageSet(data['image_set_id'])
        self.name = data['name'][next(iter(data['name']))]
        self.objective_group = None  # Identical to objective_set?
        self.repeatable = data['repeatable']
        self.reward = None

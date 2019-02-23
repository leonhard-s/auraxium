from typing import Dict, List, Optional

from ..datatypes import DataType
from .resource import ResourceType
from ..typing import Param


class Ability(DataType):  # pylint: disable=too-many-instance-attributes
    """A PS2 Ability.

    Abilities are persistent, player-bound objects responsible for persistent
    effects like AoE heal or the Heavy Assault's overshield. They are
    generally bound to a resource that is drained as the ability is used.

    """

    _collection = 'ability'

    def __init__(self, id_: int) -> None:
        self.id_ = id_

        # Set default values
        self._ability_type_id: Optional[int] = None
        self.distance_max: Optional[float] = None
        self.expires_after: Optional[int] = None
        self.first_use_delay: Optional[int] = None
        self.is_toggle: Optional[bool] = None
        self.next_use_delay: Optional[int] = None
        self.radius_max: Optional[float] = None
        self.resource_cast_cost: Optional[int] = None
        self.resource_cost: Optional[float] = None
        self._resource_type_id: Optional[int] = None
        self.reuse_delay: Optional[int] = None
        self.param: List[Param] = [None for i in range(14)]
        self.string: List[Optional[str]] = [None for i in range(4)]

    # Define properties
    @property
    def ability_type(self):
        """Returns the AbilityType of this ability."""
        return AbilityType.get(id_=self._ability_type_id)

    @property
    def resource_type(self) -> ResourceType:
        """Returns the ResourceType this ability uses."""
        return ResourceType.get(id_=self._resource_type_id)

    def populate(self, data: Optional[dict] = None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._ability_type_id = d.get('ability_type_id')
        self.distance_max = d.get('distance_max')
        self.expires_after = (int(float(d.get('expire_msec')) / 1000.0)
                              if d.get('expire_msec') is not None else None)
        self.first_use_delay = (int(float(d.get('first_use_delay_msec')) / 1000.0)
                                if d.get('first_use_delay_msec') is not None else None)
        self.is_toggle = bool(d['flag_toggle']) if d.get('flag_toggle') is not None else None
        self.next_use_delay = (int(float(d.get('next_use_delay_msec')) / 1000.0)
                               if d.get('next_use_delay_msec') is not None else None)
        self.radius_max = float(d['radius_max']) if d.get('radius_max') is not None else None
        self.resource_cast_cost = (int(d['resource_cast_cost'])
                                   if d.get('resource_first_cost') is not None else None)
        self.resource_cost = (float(d.get('resource_cost_per_msec')) / 1000.0
                              if d.get('resource_cost_per_msec') is not None else None)
        self._resource_type_id = d.get('resource_type_id')
        self.reuse_delay = (int(float(d.get('reuse_delay_msec')) / 1000.0)
                            if d.get('reuse_delay_msec') is not None else None)

        self.param = [d['param'+str(i)] if d.get('param'+str(i)) is not None
                      else None for i in range(14)]
        self.string = [d['param'+str(i)] if d.get('param'+str(i)) is not None
                       else None for i in range(14)]

        return self


class AbilityType(DataType):
    """Represents a type of ability.

    Groups similarly functioning abilities together, the "param" and "string"
    fields of an ability type also explain the (unnamed) entries for the
    corresponding abilities.

    """

    _collection = 'ability_type'

    def __init__(self, id_: int) -> None:
        self.id_ = id_

        self.description: str = ''
        self.param: List[Param] = [None for i in range(14)]
        self.string: List[Optional[str]] = [None for i in range(4)]

    def populate(self, data: Optional[Dict] = None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = d.get('description', '')
        self.param = [d['param'+str(i)] if d.get('param'+str(i)) is not None
                      else None for i in range(14)]
        self.string = [d['param'+str(i)] if d.get('param'+str(i)) is not None
                       else None for i in range(14)]

        return self

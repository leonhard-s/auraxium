"""Achievement class definition.

Achievements include weapon medals and service ribbons.
"""

from ..base import ImageMixin, Named
from ..census import Query
from ..collections import AchievementData
from .._rest import extract_payload
from .._proxy import InstanceProxy
from ..types import LocaleData

from ._objective import Objective
from ._reward import Reward

__all__ = [
    'Achievement'
]


class Achievement(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """An achievement a player may pursue.

    Achievements include weapon medals and service ribbons.

    .. attribute:: id
       :type: int

       The unique ID of this achievement. In the API payload, this
       field is called ``achievement_id``.

    .. attribute:: item_id
       :type: int

       The :class:`~auraxium.ps2.Item` associated with this
       achievement. An item ID of ``0`` signifies that this achievement
       is a service ribbon and not tied to any weapon
       (e.g. facility type specific capture ribbons).

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the achievement. This is the name of the
       weapon medal or service ribbon displayed in the game.

    .. attribute:: objective_group_id
       :type: int

       The objective group of to this achievement. All objectives in
       the given group will count towards this achievement.

       .. seealso::

          :meth:`objectives` -- Retrieve all objectives from this
          achievement's objective group.

    .. attribute:: reward_id
       :type: int

       The :class:`auraxium.ps2.Reward` granted when this achievement
       is earned.

       .. seealso::

          :meth:`reward` -- Retrieve the reward tied to this
          achievement.

    .. attribute:: repeatable
       :type: bool

       Whether this achievement is repeatable. Ribbons generally are
       repeatable, weapon medals are not.

       .. note::

          Repeatable achievements are tracked differently than one-off
          ones. See the :class:`auraxium.collections.characters_achievement.CharactersAchievement`
          model for details.

    .. attribute:: description
       :type: auraxium.types.LocaleData

       The localised description of achievement.

    .. attribute:: image_id
       :type: int | None

       The image ID of the default image.

    .. attribute:: image_set_id
       :type: int | None

       The corresponding image set.

    .. attribute:: image_path
       :type: str | None

       The base path to the image with the default :attr:`image_id`.
    """

    collection = 'achievement'
    data: AchievementData
    id_field = 'achievement_id'
    _model = AchievementData

    # Type hints for data class fallback attributes
    id: int
    item_id: int
    name: LocaleData
    objective_group_id: int
    reward_id: int
    repeatable: bool
    description: LocaleData
    image_id: int | None
    image_set_id: int | None
    image_path: str | None

    async def objectives(self) -> list[Objective]:
        """Return any objectives in the given objective group."""
        query = Query(
            Objective.collection, service_id=self._client.service_id,
            objective_group_id=self.objective_group_id)
        query.limit(1000)
        data = await self._client.request(query)
        payload = extract_payload(data, Objective.collection)
        return [Objective(o, client=self._client) for o in payload]

    def reward(self) -> InstanceProxy[Reward]:
        """Return the reward tied to this achievement.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Reward.collection, service_id=self._client.service_id)
        query.add_term(field=Reward.id_field, value=self.data.reward_id)
        return InstanceProxy(Reward, query, client=self._client)

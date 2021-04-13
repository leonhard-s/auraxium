======================
Event System Reference
======================

.. automodule:: auraxium.event

Event Types
===========

.. currentmodule:: auraxium.event

.. autoclass:: Event

   .. automethod:: age() -> float

.. autoclass:: AchievementAdded
   :show-inheritance:

.. autoclass:: BattleRankUp
   :show-inheritance:

.. autoclass:: ContinentLock
   :show-inheritance:

.. autoclass:: ContinentUnlock
   :show-inheritance:

.. autoclass:: Death
   :show-inheritance:

.. autoclass:: FacilityControl
   :show-inheritance:

.. autoclass:: GainExperience
   :show-inheritance:

   .. automethod:: filter_experience(id_: int) -> str

.. autoclass:: ItemAdded
   :show-inheritance:

.. autoclass:: MetagameEvent
   :show-inheritance:

.. autoclass:: PlayerFacilityCapture
   :show-inheritance:

.. autoclass:: PlayerFacilityDefend
   :show-inheritance:

.. autoclass:: PlayerLogin
   :show-inheritance:

.. autoclass:: PlayerLogout
   :show-inheritance:

.. autoclass:: SkillAdded
   :show-inheritance:

.. autoclass:: VehicleDestroy
   :show-inheritance:

Event Client 
============

.. currentmodule:: auraxium.event

.. autoclass:: EventClient
   
   .. automethod:: endpoint_status() -> dict[str, bool]

   .. automethod:: add_trigger(trigger: Trigger) -> None

   .. automethod:: get_trigger(name: str) -> Trigger

   .. automethod:: remove_trigger(trigger: Trigger | str, *, keep_websocket_alive: bool = False) -> None

   .. automethod:: close() -> None

   .. automethod:: connect() -> None

   .. automethod:: disconnect() -> None

   .. automethod:: dispatch(event: Event) -> None

   .. automethod:: trigger(self, event: str | typing.Type[Event], *args: str | typing.Type[Event], name: str | None = None, **kwargs) -> typing.Callable[typing.Callable[[Event], typing.Coroutine[None]], None]
   
   .. automethod:: wait_for(trigger: Trigger, *args: Trigger, timeout: float | None = None) -> Event

   .. automethod:: wait_ready(interval: float = 0.05) -> None

Triggers
========

.. autoclass:: Trigger

   .. automethod:: __init__(event: typing.Type[Event] | str, *args: typing.Type[Event] | str, characters: collections.abc.Iterable[auraxium.ps2.Character | int] | None = None, worlds: collections.abc.Iterable[auraxium.ps2.World | str] | None = None, conditions: list[typing.Callable[[Event], bool]] | None = None, action: Callable[[Event], typing.Coroutine[None] | None] | None = None, name: str | None = None, single_shot: bool = False) -> None

   .. automethod:: callback(func: Callable[[Event], typing.Coroutine[None] | None]) -> None

   .. automethod:: check(event: Event) -> bool

   .. automethod:: generate_subscription(logical_and: bool | None = None) -> str

   .. automethod:: run(event: Event) -> None

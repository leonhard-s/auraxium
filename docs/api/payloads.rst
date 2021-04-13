========================
Census Payload Reference
========================

.. currentmodule:: auraxium.models

Base Classes & Interfaces
=========================

.. module:: auraxium.models.base

.. autoclass:: Payload

.. autoclass:: RESTPayload
   :show-inheritance:

.. autoclass:: FallbackMixin

   .. automethod:: fallback_hook(id_: int) -> auraxium.types.CensusData

.. autoclass:: ImageData

.. autoclass:: Event
   :show-inheritance:
   :noindex:

   .. note::

      While this base class is defined in and accessible from the :mod:`auraxium.models.base` module, its canonical location is the :mod:`auraxium.event` namespace.

   .. automethod:: age() -> float

.. autoclass:: CharacterEvent

.. autoclass:: WorldEvent

.. module:: auraxium.models

REST Payloads
=============

Object-Mirror Payloads
----------------------

The following payloads are used as the underlying data container for the objects defined in :mod:`auraxium.ps2`. To avoid needing to document these values in both places, the attribute annotations are omitted for any payloads with an exact equivalent in the :mod:`auraxium.ps2` namespace.

.. autoclass:: AbilityData

.. autoclass:: AbilityTypeData

.. autoclass:: AchievementData

.. autoclass:: ArmourInfoData

.. autoclass:: CharacterData
   :members: BattleRank, Certs, DailyRibbon, Name, Times

.. autoclass:: CurrencyData

.. autoclass:: DirectiveData

.. autoclass:: DirectiveTierData

.. autoclass:: DirectiveTreeCategoryData

.. autoclass:: DirectiveTreeData

.. autoclass:: EffectData

.. autoclass:: EffectTypeData

.. autoclass:: ExperienceData

.. autoclass:: ExperienceRankData
   :members: EmpireData

.. autoclass:: FacilityTypeData

.. autoclass:: FactionData

.. autoclass:: FireGroupData

.. autoclass:: FireModeData

.. autoclass:: ItemCategoryData

.. autoclass:: ItemData

.. autoclass:: ItemTypeData

.. autoclass:: LoadoutData

.. autoclass:: MapHexData

.. autoclass:: MapRegionData

.. autoclass:: MarketingBundleData

.. autoclass:: MarketingBundleSingleData

.. autoclass:: MetagameEventData

.. autoclass:: ObjectiveData

.. autoclass:: ObjectiveTypeData

.. autoclass:: OutfitData

.. autoclass:: OutfitMemberData

.. autoclass:: ProfileData

.. autoclass:: ProjectileData

.. autoclass:: RegionData

.. autoclass:: ResistInfoData

.. autoclass:: ResistTypeData

.. autoclass:: ResourceTypeData

.. autoclass:: RewardData

.. autoclass:: RewardTypeData

.. autoclass:: SkillData

.. autoclass:: SkillCategoryData

.. autoclass:: SkillLineData

.. autoclass:: SkillSetData

.. autoclass:: TitleData

.. autoclass:: VehicleAttachmentData

.. autoclass:: VehicleData

.. autoclass:: WeaponData

.. autoclass:: WorldData

.. autoclass:: ZoneData

.. autoclass:: ZoneEffectData

.. autoclass:: ZoneEffectTypeData

Relational Payloads
-------------------

These are payloads that are returned as part of intermediate tables with no immediate equivalent in the :mod:`auraxium.ps2` namespace.

.. autoclass:: CharacterAchievement

.. autoclass:: CharacterDirective

.. autoclass:: CharacterDirectiveObjective

.. autoclass:: CharacterDirectiveTier

.. autoclass:: CharacterDirectiveTree

.. autoclass:: OutfitRankData

.. autoclass:: PlayerStateGroup

.. autoclass:: WeaponAmmoSlot

.. autoclass:: WeaponDatasheet

Events
======

.. note::

   While the following objects are defined in and available through the :mod:`auraxium.models` module, their canonical location is within the :mod:`auraxium.event` namespace.

.. class:: AchievementAdded
   :noindex:

   Alias of :class:`auraxium.event.AchievementAdded`.

.. class:: BattleRankUp
   :noindex:

   Alias of :class:`auraxium.event.BattleRankUp`.

.. class:: ContinentLock
   :noindex:

   Alias of :class:`auraxium.event.ContinentLock`.

.. class:: ContinentUnlock
   :noindex:

   Alias of :class:`auraxium.event.ContinentUnlock`.

.. autoclass:: Death
   :noindex:

   Alias of :class:`auraxium.event.Death`.

.. autoclass:: FacilityControl
   :noindex:

   Alias of :class:`auraxium.event.FacilityControl`.

.. autoclass:: GainExperience
   :noindex:

   Alias of :class:`auraxium.event.GainExperience`.

.. autoclass:: ItemAdded
   :noindex:

   Alias of :class:`auraxium.event.ItemAdded`.

.. autoclass:: MetagameEvent
   :noindex:

   Alias of :class:`auraxium.event.MetagameEvent`.

.. autoclass:: PlayerFacilityCapture
   :noindex:

   Alias of :class:`auraxium.event.PlayerFacilityCapture`.

.. autoclass:: PlayerFacilityDefend
   :noindex:

   Alias of :class:`auraxium.event.PlayerFacilityDefend`.

.. autoclass:: PlayerLogin
   :noindex:

   Alias of :class:`auraxium.event.PlayerLogin`.

.. autoclass:: PlayerLogout
   :noindex:

   Alias of :class:`auraxium.event.PlayerLogout`.

.. autoclass:: SkillAdded
   :noindex:

   Alias of :class:`auraxium.event.SkillAdded`.

.. autoclass:: VehicleDestroy
   :noindex:

   Alias of :class:`auraxium.event.VehicleDestroy`.

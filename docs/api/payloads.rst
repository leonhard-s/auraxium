========================
Census Payload Reference
========================

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

   .. note::

      While this base class is defined in and accessible from the :mod:`auraxium.models.base` module, its canonical location is the :mod:`auraxium.event` namespace.

.. autoclass:: CharacterEvent

.. autoclass:: WorldEvent

REST Payloads
=============

Object-Mirror Payloads
----------------------

The following payloads are used as the underlying data container for the objects defined in :mod:`auraxium.ps2`. To avoid needing to document these values in both places, the attribute annotations are omitted for any payloads with an exact equivalent in the :mod:`auraxium.ps2` namespace.

.. module:: auraxium.collections

.. autoclass:: AbilityData

.. autoclass:: AbilityTypeData

.. autoclass:: AchievementData

.. autoclass:: ArmourInfoData

.. autoclass:: CharacterData

.. autoclass:: CurrencyData

.. autoclass:: DirectiveData

.. autoclass:: DirectiveTierData

.. autoclass:: DirectiveTreeCategoryData

.. autoclass:: DirectiveTreeData

.. autoclass:: EffectData

.. autoclass:: EffectTypeData

.. autoclass:: ExperienceData

.. autoclass:: ExperienceAwardTypeData

.. autoclass:: ExperienceRankData
   :members: EmpireData

.. autoclass:: FacilityTypeData

.. autoclass:: FactionData

.. autoclass:: FireGroupData

.. autoclass:: FireModeData

.. autoclass:: FishData

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

Collections
-----------

.. module:: auraxium.collections.ability
.. autoclass:: Ability

.. module:: auraxium.collections.ability_type
.. autoclass:: AbilityType

.. module:: auraxium.collections.achievement
.. autoclass:: Achievement

.. module:: auraxium.collections.armor_info
.. autoclass:: ArmorInfo

.. module:: auraxium.collections.character
.. autoclass:: Character

.. module:: auraxium.collections.currency
.. autoclass:: Currency

.. module:: auraxium.collections.directive
.. autoclass:: Directive

.. module:: auraxium.collections.directive_tier
.. autoclass:: DirectiveTier

.. module:: auraxium.collections.directive_tree_category
.. autoclass:: DirectiveTreeCategory

.. module:: auraxium.collections.directive_tree
.. autoclass:: DirectiveTree

.. module:: auraxium.collections.effect
.. autoclass:: Effect

.. module:: auraxium.collections.effect_type
.. autoclass:: EffectType

.. module:: auraxium.collections.experience
.. autoclass:: Experience

.. module:: auraxium.collections.experience_award_type
.. autoclass:: ExperienceAwardType

.. module:: auraxium.collections.experience_rank
.. autoclass:: ExperienceRank

.. module:: auraxium.collections.facility_type
.. autoclass:: FacilityType

.. module:: auraxium.collections.faction
.. autoclass:: Faction

.. module:: auraxium.collections.fire_group
.. autoclass:: FireGroup

.. module:: auraxium.collections.fire_mode_2
.. autoclass:: FireMode2

.. module:: auraxium.collections.fish
.. autoclass:: Fish

.. module:: auraxium.collections.item_category
.. autoclass:: ItemCategory

.. module:: auraxium.collections.item
.. autoclass:: Item

.. module:: auraxium.collections.item_type
.. autoclass:: ItemType

.. module:: auraxium.collections.loadout
.. autoclass:: Loadout

.. module:: auraxium.collections.map_hex
.. autoclass:: MapHex

.. module:: auraxium.collections.map_region
.. autoclass:: MapRegion

.. module:: auraxium.collections.marketing_bundle
.. autoclass:: MarketingBundle

.. module:: auraxium.collections.marketing_bundle_with_1_item
.. autoclass:: MarketingBundleWith1Item 

.. module:: auraxium.collections.metagame_event
.. autoclass:: MetagameEvent

.. module:: auraxium.collections.objective
.. autoclass:: Objective

.. module:: auraxium.collections.objective_type
.. autoclass:: ObjectiveType

.. module:: auraxium.collections.outfit
.. autoclass:: Outfit

.. module:: auraxium.collections.outfit_member
.. autoclass:: OutfitMember

.. module:: auraxium.collections.profile_2
.. autoclass:: Profile2

.. module:: auraxium.collections.projectile
.. autoclass:: Projectile

.. module:: auraxium.collections.region
.. autoclass:: Region

.. module:: auraxium.collections.resist_info
.. autoclass:: ResistInfo

.. module:: auraxium.collections.resist_type
.. autoclass:: ResistType

.. module:: auraxium.collections.resource_type
.. autoclass:: ResourceType

.. module:: auraxium.collections.reward
.. autoclass:: Reward

.. module:: auraxium.collections.reward_type
.. autoclass:: RewardType

.. module:: auraxium.collections.skill
.. autoclass:: Skill

.. module:: auraxium.collections.skill_category
.. autoclass:: SkillCategory

.. module:: auraxium.collections.skill_line
.. autoclass:: SkillLine

.. module:: auraxium.collections.skill_set
.. autoclass:: SkillSet

.. module:: auraxium.collections.title
.. autoclass:: Title

.. module:: auraxium.collections.vehicle_attachment
.. autoclass:: VehicleAttachment

.. module:: auraxium.collections.vehicle
.. autoclass:: Vehicle

.. module:: auraxium.collections.weapon
.. autoclass:: Weapon

.. module:: auraxium.collections.world
.. autoclass:: World

.. module:: auraxium.collections.zone
.. autoclass:: Zone

.. module:: auraxium.collections.zone_effect
.. autoclass:: ZoneEffect

.. module:: auraxium.collections.zone_effect_type
.. autoclass:: ZoneEffectType

Events
======

.. module:: auraxium.models

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

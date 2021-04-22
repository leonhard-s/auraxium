=============================
PlanetSide 2 Object Reference
=============================

.. module:: auraxium.ps2

Player Characters
=================

.. autoclass:: Character(data: auraxium.types.CensusData, client: auraxium.Client)

   .. automethod:: __init__(data: auraxium.types.CensusData, client: auraxium.Client) -> None

   .. automethod:: achievements(**kwargs) -> list[auraxium.models.CharacterAchievement]

   .. automethod:: currency(**kwargs) -> tuple[int, int]

   .. automethod:: directive(results: int = 1, **kwargs) -> list[auraxium.types.CensusData]

   .. automethod:: directive_objective(results: int = 1, **kwargs) -> list[auraxium.models.CharacterDirectiveObjective]

   .. automethod:: directive_tier(results: int = 1, **kwargs) -> list[auraxium.models.CharacterDirectiveTier]

   .. automethod:: directive_tree(results: int = 1, **kwargs) -> list[auraxium.models.CharacterDirectiveTree]

   .. automethod:: events(**kwargs) -> list[auraxium.types.CensusData]

   .. automethod:: events_grouped(**kwargs) -> list[auraxium.types.CensusData]

   .. automethod:: faction() -> auraxium.InstanceProxy[Faction]

   .. automethod:: friends() -> list[Character]

   .. automethod:: get_by_name(name: str, *, locale: str = 'en', client: auraxium.Client) -> typing.Awaitable[Character | None]

   .. automethod:: get_online(id_: int, *args: int, client: auraxium.Client) -> list[Character]

   .. automethod:: items() -> auraxium.SequenceProxy[Item]

   .. automethod:: is_online() -> bool

   .. automethod:: name_long(locale: str = 'en') -> str

   .. automethod:: online_status() -> int

   .. automethod:: outfit() -> auraxium.InstanceProxy[Outfit]

   .. automethod:: outfit_member() -> auraxium.InstanceProxy[OutfitMember]

   .. automethod:: profile() -> auraxium.InstanceProxy[Profile]

   .. automethod:: skill(results: int = 1, **kwargs) -> list[auraxium.types.CensusData]

   .. automethod:: stat(results: int = 1, **kwargs) -> list[auraxium.types.CensusData]

   .. automethod:: stat_by_faction(results: int = 1, **kwargs) -> list[auraxium.types.CensusData]

   .. automethod:: stat_history(results: int = 1, **kwargs) -> list[auraxium.types.CensusData]

   .. automethod:: weapon_stat(results: int = 1, **kwargs) -> list[auraxium.types.CensusData]

   .. automethod:: weapon_stat_by_faction(results: int = 1, **kwargs) -> list[auraxium.types.CensusData]

   .. automethod:: title() -> auraxium.InstanceProxy[Title]

   .. automethod:: world() -> auraxium.InstanceProxy[World]

.. autoclass:: Faction

   .. automethod:: tag() -> str

.. autoclass:: Title

.. autoclass:: Currency

Outfits
=======

.. autoclass:: Outfit

   .. automethod:: tag() -> str

   .. automethod:: get_by_name(name: str, *, locale: str = 'en', client: auraxium.Client) -> typing.Awaitable[Outfit | None]

   .. automethod:: get_by_tag(tag: str, client: auraxium.Client) -> typing.Awaitable[Outfit | None]

   .. automethod:: leader() -> auraxium.InstanceProxy[Character]

   .. automethod:: members() -> auraxium.SequenceProxy[OutfitMember]

   .. automethod:: ranks() -> List[auraxium.models.OutfitRankData]

.. autoclass:: OutfitMember

   .. automethod:: character() -> auraxium.InstanceProxy[Character]

   .. automethod:: outfit() -> auraxium.InstanceProxy[Outfit]

Game World & Servers
====================

.. autoclass:: Region

   .. automethod:: map_region() -> auraxium.InstanceProxy[MapRegion]

   .. automethod:: zone() -> auraxium.InstanceProxy[Zone]

.. autoclass:: FacilityType

.. autoclass:: World

   .. automethod:: events(**kwargs: Any) -> list[auraxium.types.CensusData]

   .. automethod:: get_by_name(name: str, *, locale: str = 'en', client: auraxium.Client) -> typing.Awaitable[World | None]

   .. automethod:: map(zone: int | Zone, *args: int | Zone) -> list[auraxium.types.CensusData]

   .. automethod:: status() -> tuple[str, datetime.datetime]

.. autoclass:: Zone

   .. automethod:: is_dynamic() -> bool

Classes & Vehicles
==================

.. autoclass:: Loadout

   .. automethod:: armour_info() -> auraxium.SequenceProxy[ArmourInfo]

   .. automethod:: faction() -> auraxium.InstanceProxy[Faction]

   .. automethod:: profile() -> auraxium.InstanceProxy[Profile]

   .. automethod:: resist_info() -> auraxium.SequenceProxy[ResistInfo]

.. autoclass:: Profile

   .. automethod:: armour_info() -> auraxium.SequenceProxy[ArmourInfo]

   .. automethod:: resist_info() -> auraxium.SequenceProxy[ResistInfo]

.. autoclass:: Vehicle

   .. automethod:: factions() -> auraxium.SequenceProxy[Faction]

   .. automethod:: get_by_faction(faction: Faction | int, *, client: auraxium.Client) -> list[Vehicle]

   .. automethod:: skill_sets(faction: Faction | int | None) -> auraxium.SequenceProxy[SkillSet]

.. autoclass:: VehicleAttachment

   .. automethod:: faction() -> auraxium.InstanceProxy[Faction]

   .. automethod:: item() -> auraxium.InstanceProxy[Item]

   .. automethod:: vehicle() -> auraxium.InstanceProxy[Vehicle]

Firing Mechanics
================

.. autoclass:: FireGroup

   .. automethod:: fire_modes() -> auraxium.SequenceProxy[FireMode]

.. autoclass:: FireMode

   .. automethod:: type() -> FireModeType

   .. automethod:: state_groups() -> dict[PlayerState, auraxium.models.PlayerStateGroup]

   .. automethod:: projectile() -> auraxium.InstanceProxy[Projectile]

.. autoclass:: FireModeType

.. autoclass:: Projectile

   .. automethod:: flight_type() -> ProjectileFlightType

.. autoclass:: ProjectileFlightType
   :undoc-members:

.. autoclass:: PlayerState
   :undoc-members:

Metagame & Alerts
=================

.. autoclass:: MetagameEvent

.. autoclass:: MetagameEventState

Items & Weapons
===============

.. autoclass:: Item

   .. automethod:: attachments() -> auraxium.SequenceProxy[Item]

   .. automethod:: category() -> auraxium.InstanceProxy[ItemCategory]

   .. automethod:: faction() -> auraxium.InstanceProxy[Faction]

   .. automethod:: datasheet() -> auraxium.models.WeaponDatasheet

   .. automethod:: profiles() -> auraxium.SequenceProxy[Profile]

   .. automethod:: type() -> auraxium.InstanceProxy[ItemType]

   .. automethod:: weapon() -> auraxium.InstanceProxy[Weapon]

.. autoclass:: ItemCategory

.. autoclass:: ItemType

.. autoclass:: Weapon

   .. automethod:: is_heat_weapon() -> bool

   .. automethod:: ammo_slots() -> list[auraxium.models.WeaponAmmoSlot]

   .. automethod:: attachments() -> auraxium.SequenceProxy[Item]

   .. automethod:: datasheet() -> auraxium.models.WeaponDatasheet

   .. automethod:: fire_groups() -> auraxium.SequenceProxy[FireGroup]

   .. automethod:: get_by_name(name: str, *, locale: str = 'en', client: auraxium.Client) -> typing.Awaitable[Weapon | None]

   .. automethod:: item() -> auraxium.InstanceProxy[Item]

Map Screen
==========

.. autoclass:: MapHex

   .. automethod:: map_region() -> auraxium.InstanceProxy[MapRegion]

.. autoclass:: MapRegion

   .. automethod:: get_by_facility_id(facility_id: int, client: auraxium.Client) -> MapRegion

   .. automethod:: get_connected() -> set[MapRegion]

   .. automethod:: zone() -> auraxium.InstanceProxy[Zone]

Certifications & A.S.P. Skills
==============================

.. autoclass:: Skill

   .. automethod:: grant_item() -> auraxium.InstanceProxy[Item]

   .. automethod:: skill_line() -> auraxium.InstanceProxy[SkillLine]

.. autoclass:: SkillCategory

   .. automethod:: skill_lines() -> auraxium.SequenceProxy[SkillLine]

   .. automethod:: skill_set() -> auraxium.InstanceProxy[SkillSet]

.. autoclass:: SkillLine

   .. automethod:: category() -> auraxium.InstanceProxy[SkillCategory]

   .. automethod:: skills() -> auraxium.SequenceProxy[Skill]

.. autoclass:: SkillSet

   .. automethod:: categories() -> auraxium.SequenceProxy[SkillCategory]

   .. automethod:: required_item() -> auraxium.InstanceProxy[Item]

Progression
===========

.. autoclass:: Achievement

   .. automethod:: objectives() -> list[Objective]

   .. automethod:: reward() -> auraxium.InstanceProxy[Reward]

.. autoclass:: Experience

.. autoclass:: ExperienceRank

   .. automethod:: image(faction: int | Faction) -> str

.. autoclass:: Directive

   .. automethod:: objectives() -> auraxium.SequenceProxy[Objective]

   .. automethod:: tier() -> auraxium.InstanceProxy[DirectiveTier]

   .. automethod:: tree() -> auraxium.InstanceProxy[DirectiveTree]

.. autoclass:: DirectiveTier

   .. automethod:: directives() -> auraxium.SequenceProxy[Directive]

   .. automethod:: rewards() -> list[Reward]

   .. automethod:: tree() -> auraxium.InstanceProxy[DirectiveTree]

.. autoclass:: DirectiveTree

   .. automethod:: category() -> auraxium.InstanceProxy[DirectiveTreeCategory]

   .. automethod:: directives() -> auraxium.SequenceProxy[Directive]

   .. automethod:: tiers() -> auraxium.SequenceProxy[DirectiveTier]

.. autoclass:: DirectiveTreeCategory

   .. automethod:: trees() -> auraxium.SequenceProxy[DirectiveTree]

.. autoclass:: Objective

   .. automethod:: get_by_objective_group(objective_group_id: int, client: auraxium.Client) -> auraxium.SequenceProxy[Objective]

   .. automethod:: type() -> auraxium.InstanceProxy[ObjectiveType]

.. autoclass:: ObjectiveType

.. autoclass:: Reward

   .. automethod:: get_by_reward_group(reward_group_id: int, client: auraxium.Client) -> auraxium.SequenceProxy[Reward]

   .. automethod:: get_by_reward_set(reward_set_id: int, client: auraxium.Client) -> auraxium.SequenceProxy[Reward]

   .. automethod:: type() -> auraxium.InstanceProxy[RewardType]

.. autoclass:: RewardType

Abilities
=========

.. autoclass:: Ability

   .. automethod:: resource_type() -> auraxium.InstanceProxy[ResourceType]

   .. automethod:: type() -> auraxium.InstanceProxy[AbilityType]

.. autoclass:: AbilityType

.. autoclass:: ResourceType

Effects
=======

.. autoclass:: Effect

   .. automethod:: resist_type() -> auraxium.InstanceProxy[ResistType]

   .. automethod:: target_type() -> TargetType | None

   .. automethod:: type() -> auraxium.InstanceProxy[EffectType]

.. autoclass:: EffectType

.. autoclass:: TargetType
   :undoc-members:

.. autoclass:: ZoneEffect

   .. automethod:: ability() -> auraxium.InstanceProxy[Ability]

   .. automethod:: type() -> auraxium.InstanceProxy[ZoneEffectType]

.. autoclass:: ZoneEffectType

Resistance & Armour
===================

.. autoclass:: ArmourFacing
   :undoc-members:

.. autoclass:: ArmourInfo

   .. automethod:: facing() -> ArmourFacing

.. autoclass:: ResistInfo

   .. automethod:: type() -> auraxium.InstanceProxy[ResistType]

.. autoclass:: ResistType

Weapon Unlocks & Depot Bundles
==============================

.. autoclass:: MarketingBundle

   .. automethod:: image() -> str

   .. automethod:: items() -> list[tuple[Item, int]]

.. autoclass:: MarketingBundleSingle

   .. automethod:: item() -> auraxium.InstanceProxy[Item]

Leaderboard
===========

.. automodule:: auraxium.ps2.leaderboard

   .. autoclass:: Period
      :undoc-members:

   .. autoclass:: Stat
      :undoc-members:

   .. autofunction:: by_char(stat: Stat, character: int | auraxium.ps2.Character, period: Period = Period.FOREVER, *, client: auraxium.Client) -> tuple[int, int] | None

   .. autofunction:: by_char_multi(stat: Stat, character: int | auraxium.ps2.Character, *args: int | auraxium.ps2.Character, period: Period = leaderboard.Period.FOREVER, client: auraxium.Client) -> list[tuple[int, int]]

   .. autofunction:: top(stat: Stat, period: Period = Period.FOREVER, matches: int = 10, offset: int = 0, world: int | auraxium.ps2.World | None = None, *, client: auraxium.Client) -> list[tuple[int, auraxium.ps2.Character]]

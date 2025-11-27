REST Client Interface
=====================

.. autoclass:: auraxium.Client

   .. automethod:: count(type_: type[auraxium.base.Ps2Object], **kwargs) -> int

   .. automethod:: find(type_: type[auraxium.base.Ps2Object], results: int = 10, offset: int = 0, promote_exact: bool = False, check_case: bool = True, **kwargs) -> list[auraxium.base.Ps2Object]

   .. automethod:: get(type_: type[auraxium.base.Ps2Object], check_case: bool = True, **kwargs) -> auraxium.base.Ps2Object | None

   .. automethod:: get_by_id(type_: type[auraxium.base.Ps2Object], id_: int) -> auraxium.base.Ps2Object | None

   .. automethod:: get_by_name(type_: type[auraxium.base.Named], name: str, *, locale: str = 'en') -> auraxium.base.Named | None

   .. automethod:: latency() -> float

   .. automethod:: close() -> None

   .. automethod:: request(query: auraxium.census.Query, verb: str = 'get') -> auraxium.types.CensusData

Object Model Bases
==================

.. module:: auraxium.base

.. currentmodule:: auraxium.base

.. autoclass:: Ps2Object

   .. automethod:: query() -> auraxium.census.Query

.. autoclass:: Cached

   .. automethod:: alter_cache(size: int, ttu: float | None = None) -> None

.. autoclass:: Named

Proxy Objects
=============

.. currentmodule:: auraxium

.. autoclass:: InstanceProxy

   .. automethod:: resolve() -> auraxium.base.Ps2Object | None

.. autoclass:: SequenceProxy

   .. automethod:: flatten() -> list[auraxium.base.Ps2Object]

============
Custom Types
============

.. automodule:: auraxium.types

.. currentmodule:: auraxium.types

.. data:: CensusData
   :type: dict[str, str | int | float | CensusData | list[CensusData]]

   Type alias for value types allowed in API requests.

.. autoclass:: LocaleData
   :members:
   :exclude-members: model_config

   .. attribute:: de
      :type: str | None

      German locale

   .. attribute:: en
      :type: str | None

      English locale

   .. attribute:: es
      :type: str | None

      Spanish locale

   .. attribute:: fr
      :type: str | None

      French locale

   .. attribute:: it
      :type: str | None

      Italian locale

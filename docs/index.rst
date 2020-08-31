.. toctree::
   :hidden:

   self

Welcome to Auraxium
===================

Auraxium is an object-oriented, pure-Python wrapper for the `PlanetSide 2 <https://www.planetside2.com/home>`_ API.

It provides a simple object model that can be used by players and outfits without requiring deep knowledge of the API and its idiosyncrasies.

.. note::

   Both the Auraxium project and this documentation are currently a work-in-progress and come with the usual WIP caveats:

   * Some information may be missing
   * Many features are still to be added
   * There may be changes to the public API in the upcoming months

   If you would like to help out get rid of this disclaimer, feel free to get in touch via the repository.

Features
--------

* Clean, Pythonic API.
* Asynchronous endpoints to keep apps responsive during high API load.
* Low-level interface for more optimised, custom queries.
* Support for the real-time event streaming service (ESS).
* User-configurable caching system.
* Fully type annotated.

Links
-----

* `GitHub repository <https://github.com/leonhard-s/auraxium>`_
* `Issue tracker <https://github.com/leonhard-s/auraxium/issues>`_
* `Census API Documentation <https://census.daybreakgames.com/>`_

Documentation Contents
----------------------

.. note::

   Due to the object model currently undergoing regular updates, there is no static documentation yet.
   
   Please refer to introspection of the :mod:`auraxium.ps2` module for the time being.

.. toctree::

   The Auraxium Client <core>
   Event Streaming <ess>
   The Census Module <census>

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`search`

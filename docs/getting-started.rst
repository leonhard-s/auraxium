===============
Getting Started
===============

Prerequisites
=============

Auraxium currently requires `Python`_ version 3.8 or higher. Versions prior to 3.6 are not supported due to type hinting constraints. Versions 3.6 and 3.7 can likely be supported if there is demand, get in touch via the `repository issues`_ if your use case requires compatibility with these particular versions.

Using the latest version of Python is generally recommended.

Installation
============

Auraxium can be installed from PyPI through pip:

.. rubric:: Windows

.. code-block::

    python -m pip install --user --upgrade auraxium

.. rubric:: Unix

.. code-block::

    python3 -m pip install --user --upgrade auraxium

You can also use the following commands to install the latest development build directly from the repository:

.. rubric:: Windows

.. code-block::

    python -m pip install --user -e git+git://github.com/leonhard-s/auraxium.git#egg=auraxium

.. rubric:: Unix

.. code-block::

    python3 -m pip install --user -e git+git://github.com/leonhard-s/auraxium.git#egg=auraxium

.. note::

    When using pre-release versions of Auraxium as a dependency for your own packages, be sure to to pin the exact version used in ``setup.py`` or ``requirements.txt``.

    The API for these versions should not be considered stable and could break your application with the next minor version upgrade.

Overview
========

Auraxium can interface with the Daybreak Game Company's `Census API`_ in one of two ways. The first is the object model, which wraps the API's REST interface and allows accessing specific pieces of data like character names or weapon statistics.

The other is the event stream, used to react to in-game events like continent locks or player deaths via a WebSocket connection.

Object Model
------------

All API interactions are performed through :class:`auraxium.Client` or one of its sub classes. The class representations of in-game objects can be found in the :mod:`auraxium.ps2` module.

To retrieve in-game object instances, use :meth:`~auraxium.Ps2Object.get`, :meth:`~auraxium.Ps2Object.find`, or one of the ``get_by_*()`` helpers.

These methods are available for either of the following patterns:

.. rubric:: Client-Based Access

.. code-block:: python3

    client = auraxium.Client()

    my_char = await client.get_by_name(auraxium.ps2.Character, 'Higby')

.. rubric:: Object-Based Access

.. code-block:: python3

    client = auraxium.Client()

    my_char = await auraxium.ps2.Character.get_by_name('Higby', client=client)

.. note::

    Object-based access is generally preferrable as it exposes additional, class-specific helpers like :meth:`auraxium.ps2.Outfit.get_by_tag()`.

For more information on the available classes and the attributes they expose, refer to the :doc:`object model reference <api/ps2>`.

Event Stream
------------

The :class:`auraxium.EventClient` sub class adds a trigger-action system allowing the user to trigger actions when certain in-game events occur:

.. code-block:: python3

    client = auraxium.EventClient()

    @client.trigger(auraxium.EventType.DEATH)
    async def on_death(event):
        victim_id = int(event.payload['character_id'])
        victim = await client.get_by_id(auraxium.ps2.Character, victim_id)
        print(f'Player {victim.name}' has died)

For more information on the event streaming system, refer to the :doc:`event streaming documentation <event>`.

Service IDs
===========

The PlanetSide 2 API requires all client applications to register and use a service ID for all of its requests. Service IDs are used to identify your application and troubleshoot quality of service issues.

You can apply for your own service ID `here <service ID signup>`_. The process is free and usually only takes an hour or two to complete.

In Auraxium, the service ID is specified via the `service_id` argument of the :class:`auraxium.Client` instance.

For casual use and development, the default ``s:example`` service ID is also avilable, but it is limited to 10 requests per minute per IP address.

.. _Census API: https://census.daybreakgames.com/
.. _Python: https://www.python.org/downloads/
.. _repository issues: https://github.com/leonhard-s/auraxium/issues
.. _service ID signup: https://census.daybreakgames.com/#devSignup

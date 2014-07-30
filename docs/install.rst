.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _install:

=============================================================
Installing MobilePartners (FirefoxOS Scaling Website (FXOSS))
=============================================================

Pre-Requisites
--------------

Below you will find basic setup and deployment instructions for the FXOSS
project. To begin you should have the following applications installed on your
local development system::

- Python >= 2.6 (2.7 recommended)
- `pip >= 1.1 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.7 <http://www.virtualenv.org/>`_
- `virtualenvwrapper >= 3.0 <http://pypi.python.org/pypi/virtualenvwrapper>`_
- PostgreSQL >= 9.1.11
- git >= 1.7


Getting Started
---------------

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    mkvirtualenv fxoss -r $PWD/requirements/dev.txt

Then create a local settings file and set your ``DJANGO_SETTINGS_MODULE`` to use it::

    cp $PWD/project/settings/local.py-dist $PWD/project/settings/local.py

Create the PostgreSQL database and run the initial syncdb/migrate::

    createdb fxoss
    python manage.py syncdb
    python manage.py migrate

You should now be able to run the development server::

    python manage.py runserver


Deployment
----------

TODO


Fixtures
--------

Load the default fixtures for the site. Currently, the only fixtures that exist
define a *Content Authors* **Group**. To run:

    python manage.py loaddata fixture_groups.json

.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _site-translations:


Site Translations
=================

Below is a description of how the site is translated and how those translations
are managed for both existing languages and adding new ones.


Architecture Overview
------------------------

To translated the site into multiple languages, multiple copies of the site are created
and managed using the existing mutli-tenancy features in Mezzanine: http://mezzanine.jupo.org/docs/multi-tenancy.html
Pages are considered to be the same on each site if they have the same slug/URL. That
is the existing URLs (/learn/, /market/, etc) on the front end are the same across sites.
The site/language to used is detected by the browser's ``Accept-Language`` header or the
``django_language`` cookie which can be set using the language selection in the site footer.
The admin also uses localized URLs to detect the current site/language. See the Django
documentation for a more verbose description of this detection process https://docs.djangoproject.com/en/1.6/topics/i18n/translation/#how-django-discovers-language-preference


For Admins/Developers
------------------------

The set of available languages is determined by the ``LANGUAGES`` setting but simply
adding a new language here is not sufficient for creating a new language version. As previously
noted, each language will have its own ``Site`` record from ``django.contrib.sites`` and
corresponding CMS content for that site. When a new language needs to be added, a new
site record and a copy of the current CMS content needs to be made. This is handled via
the ``build_language_sites`` management command::

    python manage.py build_language_sites <language-code>
    # Adding French (fr)
    python manage.py build_language_sites fr
    # Adding all languages defined in the LANGUAGES setting
    python manage.py build_language_sites --all

By default this will copy all of the CMS content (Pages, Forms, Links) from the English
site for any new site which is created. This can be skipped via the ``--skip-content`` option.
However, this is not recommended because there is currently nothing in place to copy content
for an existing site. When testing/developing locally you can easily reset the site content
for a non-default language by deleting the site in the admin which will cascade to delete
all of the CMS content. Re-running the management command will create a fresh copy for
the language.

For non-superusers, Mezzanine has a concept of site permissions. That is users can be staff
for one or more sites. Since languages are handled as separate sites it is possible to restrict
users to only a single language/site admin. However, if translators don't have access to the
English version of the site they won't be able to view the original content for making translation
updates. Care should be taken to ensure that content authors have sufficient site permissions
for their translations. Site permissions can be managed in the User admin.


For Translators
------------------------

When logging into the admin you can select the language you would like to see. Once
in the admin you can change this language at any time using the selector in the upper
right-hand corner. When content is updated on the English version of the site, TODO
items will be created under the "Translations" header. This will give a brief description
of what was updated so that the translated content can be updated. When viewing a
translated page (non-English site version), there will be a link on the upper right-hand
side to open a popup window with the English version to aid the translation.

Non CMS Translations
--------------------------

Non CMS content (text marked for translation in code and templates) is translateable
via :doc:`Rosetta </rosetta_translations>`

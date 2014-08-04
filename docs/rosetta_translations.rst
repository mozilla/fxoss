.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _rosetta-translations:


Rosetta Translations
=====================

Below is a description of how the text marked as translateable in code and templates
is translated and how those translations are managed for both existing languages and adding new ones.


i18n Overview
------------------------

If you have not read through the official `translation documentaion <https://docs.djangoproject.com/en/dev/topics/i18n/translation/>`_,
you should. The Django documentation provides an excellent foundation to understand the translation infrastructure.


For Admins/Developers
------------------------

This adds an admin section (Rosetta) which allows for the translation of the non-database content
(which is tracked by the .po files). Content such as the registration email bodies and subjects should be
editable through this interface.

PO files are generated manually for each new locale. This is done via a management command::

    $ python manage.py makemessages -l zh_CN

It is important to note that the `locale name <https://docs.djangoproject.com/en/dev/topics/i18n/#term-locale-name>`_
format differs from the `language code <https://docs.djangoproject.com/en/dev/topics/i18n/#term-language-code>`_.
Be mindful of this when setting up PO files for new locales and enabling language support for the new language code.

For example, simplifed Chinese support requires adding an entry to the ``LANGUAGES`` setting with the proper
language code::

    ('zh-cn', _('Simplified Chinese'))

While the locale name, as shown above, is **zh_CN**.


For Translators
------------------------

When logging into the admin you can navigate to **Rosetta PO File Translation** and select a
PO File in the desired language to start editing. Upon save, a new compiled .MO file will be written
on the server.

**In order for the translations to be visible, a server restart will be required.**

.. Important::
    If you have made any changes to the Rosetta translations a developer
    must restart the server for the changes to appear. To request this
    please contact a developer in irc #oss or file a bug
    Bugzilla: Websites / mobilepartners.mozilla.org

While it is possible in some circumstances to auto reload the MO file, it is ill advised in
production environments for performance reasons. More configuration options can be read about
`here <https://github.com/mbi/django-rosetta#configuration>`_.


Translating Tips
------------------------

Some of the content in Rosetta will have embedded html.

.. code-block:: html

    <p>
        You can also
        <a href="%(password_reset_url)s?next=%(profile_update_url)s">reset your password</a>
        if you've forgotten it.
    </p>

In the above example you should copy the entire block but only translate the strings, so your
copy should look like the following where the Xs are translated:

.. code-block:: html

    <p>
        XXX XXX XXX
        <a href="%(password_reset_url)s?next=%(profile_update_url)s">XXXXX XXXX XXXXXXXX</a>
        XX XXXXX XXXXXX XX.
    </p>

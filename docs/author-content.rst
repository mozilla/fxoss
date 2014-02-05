Content Authoring
=================

Below you will find basic content authoring instructions for the FirefoxOS
Scaling Website (FXOSS) project.


Authenticating
------------------------

In order to author content in the FXOSS site, you will need to:

  1. Navigate to **mobilepartners.mozilla.org/admin**
  2. Supply the **username** (email) and **password** you
  3. Select the **Admin Interface**
  4. Press **Login**

Dashboard
------------------------

The dashboard provides quick access to various site components. The pieces to
focus on for Content Authoring are the *Pages* and *Media Library* sections under
the *Content* category.

Pages
------------------------

Pages are the primary piece of authored content as the site's navigation and
structure are derived from the created pages.  To add a Page to the root of the
site, click **Add+** in the Pages Row.  This will open a form that allows you to
create a Rich Text Page:

  * **Title [en]**: The title that will appear in the navigation node(s) for the
    Rich Test Page. To note: future versions of the software will allow for
    additional language support. The GUI will provide a meaningful way to
    switch between supported languages
  * **Status**: Select Draft to hide the page from all but admin users. Publishing
    the page will allow all users to view the page.
  * If publication dates are required, set the optional **Published from** and **Expires
    on** fields
  * **Show in menus** allows the author to indiciate which menu(s) the navigation
    element should appear in. The current layout supports only *Top navigation
    bar* and *Left-hand tree* menus.
  * **Login required** protects content from anonymous users.
  * **Content [en]**: This field supports WYSIWYG editing, and easy insertion of related
    media
  * To explicitly declare additional meta data, expand the **meta data** tab
    and populate the optional fields accordingly.
  * Be sure to press **Save** to store the Page in the database.

Creating a Child Page is as simple as:

  1. Navigate to the dashboard
  2. Click **Pages**
  3. Selected the **Add...** dropdown next to the Page you would like to append a
     child too, and select **Rich Text Page**.
  4. Add your content as above, and **Save**.

Media Library
-------------------------

The Media Library stores upload images, pdfs, and other related media that will
be linked to from within a Rich Text Page.  It is accessible either from the
Dashboard, or via the WYSIWYG editor while editing a Page. The Media Library
supports Folders and uploading multiple files at once.

If you have all of your related media ready to upload before creating any Pages:

  1. Navigate to the **Media Library** from the Dashboard
  2. Create Folders (if needed) to structure your media via the **New Folder**
     button
  3. Navigate to the target folder and select **Upload**
  4. Press **Select Files** to browse your local file system for files to upload

Alternately, one may upload related media during Page authoring.

  1. Navigate to (or create a) **Page**
  2. In the **Content** field, type and select some text
  3. Click **Insert/Edit Link** in the toolbar
  4. Click the **browse icon** in the popup next to Lin url
  5. The Media Libary popup will render, and one can create folders/upload per
     the above instructions.
  6. Once files(s) have been uploaded, click the **Select File** button next to
     the file you want to insert.
  7. Make any additional configuration changes in the **Insert/Edit Link** popup
  8. Click **Insert**
  9. Be sure to **Save** changes to the Page

Other Content Types
------------------------------

If you need to generate an External Link as a navigation element, this can be
accomplished by creating a Link object from the Pages admin section

  1. Click **Pages**
  2. Click **Add... Link** at the root of the site or as a child of an existing
     content node.
  3. Ensure the **URL** field is a valid URL
  4. Edit other fields as needed
  5. Press **Save**

It is possible to generate a Form from within the Admin. This is beyond the
normal use case for this site. In short, similar to creating a Page, an author
can generate a form to collect data from end users.

Front End Content Editing
------------------------------

If inline editing is enabled, admin users will be able to Edit the **content**
of an existing Page via the front end.

  1. Authenticate via **/admin** and select **Site** as the interface
  2. Navigate to a Page
  3. Click **Edit**
  4. The WYSIWYG editor will render as a modal; make edits and press **Save**

Download Agreement
-------------------------

The download agreement is a special case of a **Page** record. The content of
the page should be the agreement text. The slug of the agreement should be *download-agreement*.
This can be changed by opening the **Meta data** section at the bottom of the page
editor and setting *download-agreement* in the **URL** field. This page should also be
marked as **Login Required** using the checkbox in the editor.

It is also possible to change the version of the agreement. Changing the version will
force all users to resign the agreement. This is managed under the site settings:

  1. Navigate to the **Site > Settings** from the Dashboard
  2. Change the **Download Agreement Version** under **Miscellaneous**
  3. Press **Save**

Protected Downloads
-------------------------

Protected downloads are media assets which require the user to sign the user agreement prior
to accessing. These are a special case of assets managed under the **Media Library**. These
assets are uploaded into a **protected** folder within the **Media Library**.

  1. Navigate to the **Media Library** from the Dashboard
  2. Create Folder a folder named  **protected** (if needed) via the **New Folder** button
  3. Navigate to the **protected** folder and select **Upload**
  4. Press **Select Files** to browse your local file system for files to upload


hr_hospital2
============

Odoo module for hospital management.

Features
--------
- Manage doctors, patients, diseases, and visits
- Disease classifier with tree structure
- Patient and doctor personal data
- Visit scheduling and history
- Ukrainian translation (uk_UA)
- Basic access rights and menu structure

Installation
------------
1. Copy the module to your Odoo addons directory.
2. Update the app list in Odoo.
3. Install the module `hr_hospital2` via the Odoo interface.

Testing
-------
To run module tests, execute:

.. code-block:: bash

   ./odoo-bin -d <your_db> -i hr_hospital2 --test-enable --stop-after-init --log-level=test

Replace `<your_db>` with your Odoo database name.

Translation
-----------
Ukrainian translation is available in `i18n/uk_UA.po`. To update translations:
- Go to Settings > Translations > Load a Translation
- Choose Ukrainian (uk_UA)

Changelog
---------
See changelog.rst for module history.

Docker Stats Graph
==================

To plot docker stats into graph from multiple dockers.

Get Started
-----------

TBD ...

Testing
-------

To find out more info about the testing configuration, check out the
``tox.ini`` file.
Use the ``dev-requirements.txt`` for libraries only used for tests or dev.

.. code:: bash

   # Run the test suite
   tox
   # Run the linter:
   tox -e lint
   # Run the coverage on the src module
   pytest -e coverage


Misc Notes
----------

-  Make sure and edit the package title in ``setup.py`` to reflect your
   app name
-  If you have issue with tox and ``ModuleNotFoundError``, try set
   ``recreate`` to ``True`` in ``tox.ini``.

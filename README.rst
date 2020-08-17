Backend Engineering Exercise
============================

**Language**: Python3x

**Frameworks**: None

**Other tools / dependencies**:

- requests_ for HTTP requests
- click_ for command-line tasks
- memcached_ for caching
- prettytable_ to print out tabular data

.. _requests: https://github.com/psf/requests
.. _click:  https://github.com/pallets/click
.. _memcached: https://memcached.org
.. _prettytable: https://github.com/jazzband/prettytable


Installing and running with Docker
----------------------------------

Download and install project dependencies

.. code-block:: text

    docker-compose up --build


Run program

.. code-block:: text

    docker-compose run cli python main.py


You can modify the subreddit and/or listing size optionally

.. code-block:: text

    docker-compose run cli python main.py --subreddit='popular' --limit=15


Testing
-------

.. code-block:: text

    docker-compose run cli python -m unittest


Feel free to reach out anytime if you have any questions.

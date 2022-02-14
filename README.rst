Docker Stats Graph
==================


.. |Codecov Badge| image:: https://codecov.io/gh/sylhare/docker-stats-graph/branch/master/graph/badge.svg?token=H7VDPOZJWT
  :target: https://codecov.io/gh/sylhare/docker-stats-graph


To plot docker stats into graph from multiple dockers.

Get Started
-----------

Run the ``scrips/generate_data.sh``, this will produce a data.csv that will be used to create the graphs.


Docker Stats Info
-----------------

Let's dig into each of those columns:

- The **CONTAINER** column lists the container IDs.
- The **CPU %** column reports the host capacity CPU utilization.

  - For example, if you have two containers, each allocated the same CPU shares by Docker, and each using max CPU, the docker stats command for each container would report 50% CPU utilization. Though from the container's perspective, their CPU resources would be fully utilized.

- The **MEM USAGE / LIMIT** and **MEM %** columns display the amount of memory used by the container, along with the container memory limit, and the corresponding container utilization percentage.

  - If there is no explicit memory limit set for the container, the memory usage limit will be the memory limit of the host machine.Note that like the CPU % column, these columns report on host utilization.

- The **NET I/O** column displays the total bytes received and transmitted over the network by the corresponding container.

- The **BLOCK I/O** section displays the total bytes written and read to the container file system.
- The **PIDS** column displays the number of kernel process IDs running inside the corresponding container.

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
   tox -e coverage


Misc Notes
----------


-  If you have issue with tox and ``ModuleNotFoundError``, try set
   ``recreate`` to ``True`` in ``tox.ini``.


Sources
-------

Some of the source I use for the `docker stats` command.

- Documentation from docker_
- Article on analyzing-docker-container-performance-native-tools_
- Article on monitoring-docker_
- Datascience Handbook_

.. _analyzing-docker-container-performance-native-tools: https://crate.io/a/analyzing-docker-container-performance-native-tools/
.. _docker: https://docs.docker.com/engine/reference/commandline/stats/
.. _monitoring-docker: http://www.zakariaamine.com/2019-12-04/monitoring-docker
.. _Handbook: https://jakevdp.github.io/PythonDataScienceHandbook/

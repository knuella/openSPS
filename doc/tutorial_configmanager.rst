
Hintergrundprogramme starten
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MongoDB starten:

.. code:: bash

  sudo systemctl start mongodb

oder

.. code:: bash

  sudo service mongodb start

Ins repository Verzeichniss wechseln:

.. code:: bash

  cd rpi-sps/src


Controller starten (Name nach Klassendiagramm = NachrichtenVerwalter):

.. code:: bash

  python3 controller.py

configuration_manager starten unter dem namen "cm" mit den ip-adressen und
ports, die in der controler conf-datei gespeichert sind. (Name nach
Klassendiagramm = KonfigurationsVerwalter):

.. code:: bash

  python3 configuration_manager_mongodb.py cm tcp://127.0.0.10:6666 tcp://127.0.0.10:6665 tcp://127.0.0.10:5556 tcp://127.0.0.10:5555


Nachrichten verschicken / empfangen aus python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: bash

  python3

.. code:: python

  import sys
  from rpisps.context import 

  #argumente für Context
  sys.argv = ['bla', 'test_context', 'tcp://127.0.0.10:6666', 'tcp://127.0.0.10:6665', 'tcp://127.0.0.10:5556', 'tcp://127.0.0.10:5555']

  #Context instanzieren
  test_context = Context()

  #alle templates abfragen
  test_context.request_value('cm', {'operation':'get', 'collection':'templates', 'target':{})

  # config speichern
  test_context.write_value('cm', {'operation':'save', 'collection':'instances', 'target':{'blakey':'blubval'})

  # config abfragen
  test_context.request_value('cm', {'operation':'get', 'collection':'instances', 'target':{})

  # config löschen
  test_context.write_value('cm', {'operation':'delete', 'collection':'instances', 'target':{'object_id':'1234345tesfvcjkdcfnhexr6387'})



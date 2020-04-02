Youtube Closed Captions
-----------------------

Downloads the closed captions(subtitles) from Youtube videos
============================================================


Requirements
~~~~~~~~~~~~

* Currently requires python >= 3.5

To Use
~~~~~~
  
in  main.py

.. code:: python

   id = 'id_video or playlist'
   
create a file ytcc.credential.py with your credentials:

.. code:: python

  username = 'youtube_email'
  password = 'youtube_password'

Development
===========

Run Tests
~~~~~~~~~

*Note:* Functional tests do download directly from Youtube

.. code:: bash

   ## All tests
   python -m unittest discover

   ## Unit tests
   python -m unittest discover test/unit

   ## Functional tests
   python -m unittest discover test/functional


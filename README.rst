Youtube Closed Captions
-----------------------

Downloads the closed captions(subtitles) from Youtube videos
============================================================

.. image:: https://circleci.com/gh/mkly/youtube-closed-captions.svg?style=svg
  :target: https://circleci.com/gh/mkly/youtube-closed-captions

Requirements
~~~~~~~~~~~~

* Currently requires python >= 3.5

To Use
~~~~~~
  
in  ytcc.main
.. code:: python

   video_id = 'id_video'
   
create file ytcc.credential.py as:
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


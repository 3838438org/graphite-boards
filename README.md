Graphite Boards
===============

What?
-----

A webapp written using Flask, Sqlite, LDAP and Twitter bootstrap to generate flexible, responsive dashboards for large or small displays, using the standard Graphite rendering engine.


Why?
----

At Mind Candy we send millions of datapoints into Graphite from our varying systems and applications. The NetOps team have been using these to display simple web pages on large TV screens in the office for some time. 

However, the boards were just hand-crafted HTML and others, technical and non-technical, wanted to display metrics in their part of the office too. We could've used the dashboard creator in Graphite but it was a little too clunky for what we required, so we created Graphite Boards as a quick solution.


Who?
----

"Graphite Boards" was written by Phil Hendren ([dizzythinks](https://github.com/dizzythinks)) and James Denness ([scarybot](https://github.com/scarybot)) from the NetOps team at Mindcandy.


To do and known limitations
----------------------------

  * The javascript may not be as optimal as it could be.
  * Tests! - Graphite Boards was written quickly to solve a problem so tests were not written :-(
  * Currently anyone can change the layout of a dashboard, even when not authed; as this is an internal tool this is not a major issue for us, but adding a check for an authenticated user does need to be added.


Install
=======

    me@localhost:~$ virtualenv myenv
    me@localhost:~$ cd myenv/
    me@localhost:~/myenv$ source bin/activate
    (myenv)me@localhost:~/myenv$ git clone git@github.com:mindcandy/graphite-boards.git
    (myenv)me@localhost:~/myenv/graphite-boards$ pip install -r requirements.txt
    (myenv)me@localhost:~/myenv/graphite-boards$ cp app/setting.py.example app/settings.py

Edit settings.py, and as a minimum, set the full path to your intended sqllite db file (i.e. the path to the "db" folder in the checkout)


    (myenv)me@localhost:~/myenv/graphite-boards$ ./runserver.py 
     * Running on http://0.0.0.0:5000/
     * Restarting with reloader

Authentication
==============

__AUTH_ENABLED__: True/False - When set to "False" in settings.py then "Graphite Boards" will run in "test mode". This means that only the TEST_USER will be available. The application is fully functional using this user but it does limit you to who can create dashboards.

__LDAP_ENABLED__: True/False - If set to True, you will need to add the other settings for your LDAP server. Note... only Secure LDAP is supported so you will need to have your certificate available. When set to False we fall back to SQLite authentication.

__NOTE__: We create an admin/admin user in sqlite the first time you hit the application. This user can edit any dashboard and if you login in with it it will always auth againast the database even if LDAP is enabled.

Screenshots
===========

My Dashboards
-------------
  * List all dashboards you own.
  * Create new dashboards

![My_Dashboards](http://raw.githubusercontent.com/mindcandy/graphite-boards/raw/master/screenshots/2.png)


Edit dashboards
---------------
  * Here you can add new Graphite URL or edit existing ones.

![Edit_View](http://raw.githubusercontent.com/mindcandy/graphite-boards/raw/master/screenshots/3.png)


View All Dashboards
-------------------
  * All dashboards can be viewed without authentication. Transparency rules.

![No_Auth](http://raw.githubusercontent.com/mindcandy/graphite-boards/raw/master/screenshots/1.png)


A Dashboard
-----------
  * Here we have a dashboard with 7 graphs. Each graph is resizable and draggable and layout are saved via callback to the sqlite backend.

![Dashboard](http://raw.githubusercontent.com/mindcandy/graphite-boards/raw/master/screenshots/4.png)



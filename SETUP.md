## Test Requirements
* Python 3.5
* PostgreSQL 9.6
* Ubuntu 16.04

## Python Config

### Create Virtual Env
Install `virtualenv`

    $ sudo apt-get install python-pip
    $ sudo pip install virtualenv
    $ sudo apt-get install python-dev
    
##### CREATE ENVIRONMENT
    $ virtualenv -p /usr/bin/python3.5 env
    
    # activate the new environment
    $ source env/bin/activate
    
    # install requirements
    $ pip install -r requirements.txt
    
##### DEACTIVATE ENVIRONMENT
To deactivate environment for session, enter:

    $ deactivate

## Install and Setup PostgreSQL
[Instructions](https://github.com/simlu/xmonad/blob/master/programs/postgresql.md)
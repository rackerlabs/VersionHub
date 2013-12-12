VersionHub

# Overview
**VersionHub**'s aim is to provide a centralized location for Rackspace to log its Production level applications, their version histories as well as the dependencies of the applications on one another.

The idea came about from Rackerlabs hack week '13 and inspired by Jim Meow-yer and Duncan McCreggorrrr...

    https://github.rackspace.com/rackertools/dev/wiki/Racker-Tools-Hack-Week:-Dec-2013

## Contributors
* Roger Enriquez (UI - Entrepreneur, API - Backend ninja)
* Kacie Hauser (DB - Postgres Pro, API - Tornado master)

## Technologies
* **Python 3.3** API server running on Tornado and nginx
* **Angular JS 2.2** UI running on nginx
* **Postgres 9.3** back-end

## Installation
    sudo -s

    git clone https://github.com/rackerlabs/VersionHub.git

    apt-get install -y python-software-repository libpq-dev build-essential
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python3.3 python3.3-dev

    wget -O /var/tmp/ez_setup.py https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
    python3.3 /var/tmp/ez_setup.py

    wget -O /var/tmp/get_pip.py https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    python3.3 /var/tmp/get_pip.py

    pip install -r requirements.txt

    cd /root/VersionHub/backend
    /usr/local/share/python3/paver create_virtualenv

    source bin/activate
    pip install -r requirements.txt

    version_hub


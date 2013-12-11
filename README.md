VersionHub

# Installation
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


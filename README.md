VersionHub

# Installation
    sudo -s

    git clone https://github.com/rackerlabs/VersionHub.git

    apt-get install -y python3 python3-dev python-pip libpq-dev build-essential
    virtualenv -p /usr/bin/python3 /var/tmp/python3
    source /usr/bin/python3/bin/activate

    cd /root/VersionHub/backend
    pip install -r requirements.txt

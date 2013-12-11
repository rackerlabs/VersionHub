VersionHub

# Installation
    sudo -s

    git clone https://github.com/rackerlabs/VersionHub.git

    cd VersionHub
    apt-get install -y python3 python-pip
    virtualenv -p /usr/bin/python3 /var/tmp/python3
    source /usr/bin/python3/bin/activate

    cd /root/VersionHub
    pip install -r requirements.txt

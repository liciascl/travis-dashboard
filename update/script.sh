#!/bin/sh
git checkout master
git pull origin master
sudo apt-get update


if [ -f ~/update.txt ]
then
    echo "Ja foi atualizado..."
else
    touch ~/update.txt
    echo "Automatizando o update do sistema..." > ~/update.txt
    date >> ~/update.txt
    sudo sed -i '19i\sudo bash /home/pi/travis-dashboard/update/script.sh\' /etc/rc.local
fi
echo "finish update"

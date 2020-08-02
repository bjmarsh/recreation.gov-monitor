#! /usr/bin/env bash

echo;echo
echo "*************************************************"
date
echo "*************************************************"
cd /home/users/bemarsh
echo "Running bashrc..."
source .bashrc
echo "python location is:"
which python
cd /home/users/bemarsh/scripts/recreation
echo "Running script..."
python get_availability.py 2020 10 2 2>&1
python get_availability.py 2020 10 3 2>&1

if [ $? != 0 ]; then
    tail -n 20 cronlog.txt | mail -s "ERROR: recreation.gov script crashed!!" bmarsh9311@gmail.com
fi

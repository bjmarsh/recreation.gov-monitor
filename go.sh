#! /usr/bin/env bash

echo;echo
echo "*************************************************"
date
echo "*************************************************"
cd /home/bennett
echo "Running bashrc..."
source .bashrc
echo "python location is:"
which python
cd /home/bennett/recreation
echo "Running script..."
python3 get_availability.py 2020 10 2 2>&1
python3 get_availability.py 2020 10 3 2>&1

if [ $? != 0 ]; then
    tail -n 20 cronlog.txt | python3 ses.py "ERROR: recreation.gov script crashed!!"
fi

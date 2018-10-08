#!/bin/bash
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane; sim_vehicle.py -v ArduPlane -I 1" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_2; sim_vehicle.py -v ArduPlane -I 2" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_3; sim_vehicle.py -v ArduPlane -I 3"
sleep 10
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5773" --id 253 " &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5783" --id 254" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5793" --id 255" &

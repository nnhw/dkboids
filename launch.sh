#!/bin/bash
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane; sim_vehicle.py -v ArduPlane -I 1" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_2; sleep 5; sim_vehicle.py -v ArduPlane -I 2" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_3; sleep 10; sim_vehicle.py -v ArduPlane -I 3" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_4; sleep 15; sim_vehicle.py -v ArduPlane -I 4" &
sleep 20
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5773" --id 252 " &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5783" --id 253" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5793" --id 254" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5803" --id 255" &
#!/bin/bash
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane; sim_vehicle.py -v ArduPlane -I 1" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_2; sleep 5; sim_vehicle.py -v ArduPlane -I 2" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_3; sleep 10; sim_vehicle.py -v ArduPlane -I 3" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_4; sleep 15; sim_vehicle.py -v ArduPlane -I 4" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_5; sleep 20; sim_vehicle.py -v ArduPlane -I 5" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_6; sleep 25; sim_vehicle.py -v ArduPlane -I 6" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_7; sleep 30; sim_vehicle.py -v ArduPlane -I 7" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_8; sleep 35; sim_vehicle.py -v ArduPlane -I 8" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_9; sleep 40; sim_vehicle.py -v ArduPlane -I 9" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_10; sleep 45; sim_vehicle.py -v ArduPlane -I 10" &
sleep 60
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5773" --id 246 " &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5783" --id 247" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5793" --id 248 " &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5803" --id 249" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5813" --id 250" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5823" --id 251" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5833" --id 252 " &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5843" --id 253" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5853" --id 254" &
konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:5863" --id 255" &
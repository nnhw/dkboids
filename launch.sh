#!/bin/bash
NUM=$1
for a in `seq 1 $NUM`; do
    SL=$((a*5))
    konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/ardupilot/ArduPlane_$a; sleep $SL ;sim_vehicle.py -v ArduPlane -I $a" &
done
sleep 60
for a in `seq 1 $NUM`; do
    ID=$((255-$NUM+$a))
    PORT=$((5763+$a*10))
    konsole --hold --new-tab -e $SHELL -c "cd ~/Work/software/dkboids; python interface.py --master "tcp:127.0.0.1:$PORT" --id $ID " &
done

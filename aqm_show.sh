#!/bin/bash
firefox http://localhost/aqmmaster/ &
sleep 5
xdotool search --sync --onlyvisible --pid $! windowactivate key F11
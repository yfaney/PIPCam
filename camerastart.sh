#!/bin/sh
if [ "$#" -ne 6 ] ; then
        echo "usage: camerastart.sh <width> <height> <bitrate> <fps> <ip> <port>"
else
	raspivid -n -w $1 -h $2 -b $3 -fps $4 -rot 270 -vf -hf -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=$5 port=$6
	#-rot 90
fi


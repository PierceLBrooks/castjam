#!/bin/sh
for mp4 in *.mp4; do
ffmpeg -i $mp4 -vframes 1 -f image2 ${mp4%%.mp4}.png
mv ${mp4%%.mp4}.mp4 ${mp4%%.mp4}.original.mp4
done

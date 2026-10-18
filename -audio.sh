#!/bin/sh
for mp4 in *.original.mp4
do
ffmpeg -i "$mp4" -an -c:v copy "${mp4%%.original.mp4}.mp4"
rm "$mp4"
done


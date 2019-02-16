#!/bin/bash
ffmpeg -i $1 -r 1 -s 300x200 -f image2 $1-%03d.jpeg

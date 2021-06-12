#!/bin/bash
time=$(date "+%Y_%m_%d_%H_%M_%S")
ffmpeg -framerate 12 -i out/image_color%05d.jpg -codec copy -b:v 1000k output_color_$time.mp4 
ffmpeg -framerate 12 -i out/image_depth%05d.jpg -codec copy -b:v 1000k output_depth_$time.mp4 
ffmpeg -i output_color_$time.mp4 -i output_depth_$time.mp4  -filter_complex hstack output_rgbd_$time.mp4 

echo $time
outdir=out_$time
echo $outdir
cp -r out $outdir
rm -rf out/*
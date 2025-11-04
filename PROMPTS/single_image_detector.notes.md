after manifesting the spec ....

## run on remote:
docker run --rm -it -e DISPLAY=:1 -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v /media/ros/rig/FRAMES/cam0/1762219673640745083.png:/data/image.png kalibr:single-image-detector


/ros_entrypoint.sh
source devel/setup.bash
rosrun kalibr single_image_detector /data/image.png
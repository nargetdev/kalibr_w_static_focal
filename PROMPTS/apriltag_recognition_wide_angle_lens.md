My previous thesis that the AprilTags were failing to recognize because of specular highlights was wrong. Even after push processing the images to full black and Floor white many of the April tags are not recognizing I believe this is because of the geometry and field of distortion. What other inputs might be try to the kalibr calibration to remedy.

Lets try a different camera/distortion model

previous: pinhole-radtan
instead lets try: extended unified camera model (eucm)
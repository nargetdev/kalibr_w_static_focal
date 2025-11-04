
we want to embed something like single_image_detector.cpp and then builld it with CMake somehow in the existing `colcon build ...` pipeline.

```single_image_detector.cpp
#include "apriltags/TagDetector.h"
#include "apriltags/Tag36h11.h"  // For tagCodes36h11; change for other families (e.g., Tag16h5.h)
#include <opencv2/opencv.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " <image_path>" << std::endl;
        return 1;
    }

    // Load the image (color or grayscale)
    cv::Mat image = cv::imread(argv[1]);
    if (image.empty()) {
        std::cout << "Error: Could not load image from " << argv[1] << std::endl;
        return 1;
    }

    // Convert to grayscale (required for detection)
    cv::Mat gray;
    cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);

    // Create the detector (using 36h11 family; adjust TagCodes if your grid uses a different family)
    AprilTags::TagDetector detector(AprilTags::tagCodes36h11);

    // Run detection
    std::vector<AprilTags::TagDetection> detections = detector.extractTags(gray);

    // Print results
    std::cout << detections.size() << " tags detected:" << std::endl;
    for (const auto& det : detections) {
        std::cout << "  Id: " << det.id
                  << " (Hamming distance: " << det.hammingDistance
                  << ", good: " << (det.good ? "yes" : "no")
                  << ") at center (" << det.cxy.first << ", " << det.cxy.second << ")" << std::endl;
        // Print corner positions for debugging
        std::cout << "    Corners: ";
        for (int i = 0; i < 4; ++i) {
            std::cout << "(" << det.p[i].first << ", " << det.p[i].second << ") ";
        }
        std::cout << std::endl;
    }

    // Visualize detections on the original image
    for (const auto& det : detections) {
        det.draw(image);  // Draws the tag outline and ID
    }
    cv::imshow("AprilTag Detections", image);
    cv::waitKey(0);  // Press any key to close the window

    return 0;
}
```



;;; existing image
note the existing base image `Dockerfile_ros1_20_04` take a look at how that one is set up.  Extend it with a new `Dockerfile_single_image_detector` which starts FROM `kalibr:ros1-20.04`


.. which was was built via

    docker build -f Dockerfile_ros1_20_04 -t kalibr:ros1-20.04 .


create `Dockerfile_single_image_detector` and `build_simple_image_detector.sh`



;;; runtime
our existing container from `kalibr:ros1-20.04` is run as:

    docker run --rm -it   -e DISPLAY=:1   -e QT_X11_NO_MITSHM=1   -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v /home/ros/UTM_SHARE/PhotogrammetryWAAM/FRAMES:/data kalibr:ros1-20.04

on the remote.

once inside the container the environment is bootstrapped as 


    root@4b516235c099:/catkin_ws# /ros_entrypoint.sh
    (failed reverse-i-search)`sour': /ros_entrypoint.^C
    root@4b516235c099:/catkin_ws# source devel/setup.bash
    root@4b516235c099:/catkin_ws# rosrun kalibr kalibr_calibrate_cameras \
    >         --target april_6x6.yaml \
    >         --models pinhole-radtan pinhole-radtan \
    >         --topics /cam0/image_raw /cam1/image_raw \
    >         --bag data.orig.bag
    importing libraries

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
    cv::imwrite("/out/result.png", image);
    // cv::imshow("AprilTag Detections", image);
    // cv::waitKey(0);  // Press any key to close the window

    return 0;
}

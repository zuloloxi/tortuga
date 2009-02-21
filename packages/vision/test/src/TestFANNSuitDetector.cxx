/*
 * Copyright (C) 2009 Robotics at Maryland
 * Copyright (C) 2009 David Love
 * All rights reserved.
 *
 * Author: David Love <loved@umd.edu>
 * File:  packages/vision/test/src/TestFANNSuitDetector.cpp
 */

// STD Includes
#include <cmath>
#include <set>
#include <iostream>

// Library Includes
#include <UnitTest++/UnitTest++.h>

#include <boost/bind.hpp>
#include <boost/filesystem.hpp>
#include <boost/foreach.hpp>

// Project Includes
#include "core/include/ConfigNode.h"
#include "vision/include/Image.h"
#include "vision/include/OpenCVImage.h"
#include "vision/include/FANNSuitDetector.hpp"

using namespace ram;

static boost::filesystem::path getImagesDir()
{
    boost::filesystem::path root(getenv("RAM_SVN_DIR"));
    return root / "packages" / "vision" / "test" / "data" / "images" /
        "testfann";
}

static std::string getSuitNetworkFile()
{
    boost::filesystem::path root(getenv("RAM_SVN_DIR"));
    return (root / "packages" / "vision" / "test" / "data" /
            "suits.irn").file_string();
}

struct FANNSuitDetectorFixture
{
};

SUITE(FANNSuitDetector) {

TEST_FIXTURE(FANNSuitDetectorFixture, FANNSuitDetectorTest)
{
    core::ConfigNode config = core::ConfigNode::fromString (
        "{ 'SavedImageIdentifierNetwork' : '" + getSuitNetworkFile() + "' }");
    vision::FANNSuitDetector detector = vision::FANNSuitDetector (config);
    vision::Image* img;
    boost::filesystem::directory_iterator end;
    boost::filesystem::path dir = getImagesDir();
    int results[4] = { vision::Suit::CLUB, vision::Suit::DIAMOND,
                       vision::Suit::HEART, vision::Suit::SPADE };
    unsigned int i = 0;

    // Ensure the images directory exists
    CHECK (boost::filesystem::exists (dir));    
    for (boost::filesystem::directory_iterator itr (dir); itr != end; ++itr) {
        if (boost::filesystem::extension (itr->path()) == "jpg") {
            // Open image and ensure it was loaded properly
            img = vision::Image::loadFromFile(itr->path().file_string());
            CHECK(img);

            // Process the image, then make sure we get the right suit
            detector.processImage(img);
            CHECK_EQUAL(detector.getSuit(), results[i++]);
        }
    }
}
    
} // SUITE(FANNSuitDetector)

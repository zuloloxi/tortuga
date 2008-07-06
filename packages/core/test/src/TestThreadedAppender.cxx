/*
 * Copyright (C) 2007 Robotics at Maryland
 * Copyright (C) 2007 Joseph Lisee <jlisee@umd.edu>
 * All rights reserved.
 *
 * Author: Joseph Lisee <jlisee@umd.edu>
 * File:  packages/core/test/src/TestThreadedAppender.cxx
 */

// STD Includes
#include <vector>

// Library Includes
#include <UnitTest++/UnitTest++.h>
#include <log4cpp/Category.hh>
#include <log4cpp/LayoutAppender.hh>

// Project Includes
#include "core/include/ThreadedAppender.h"

/** Buffers all recieved log events, used for testing below */
class BufferedAppender : public log4cpp::LayoutAppender
{
public:
    BufferedAppender(std::string name) : LayoutAppender(name) {}

    virtual void close() { logEvents.clear(); }
          
    std::vector<log4cpp::LoggingEvent> logEvents;
    
protected:
    virtual void _append(const log4cpp::LoggingEvent& event)
    {
        logEvents.push_back(event);
    }
};

using namespace ram;

struct ThreadedAppenderFixture
{
    ThreadedAppenderFixture() :
        appender(new BufferedAppender("RealAppender")),
        threadedAppender(new core::ThreadedAppender(appender)),
        category(0)
    {
        log4cpp::Category::getInstance("Testing");
        category = log4cpp::Category::exists("Testing");
        category->setAppender(threadedAppender);
    }

    ~ThreadedAppenderFixture()
    {
        log4cpp::Category::shutdown();
    }

    BufferedAppender* appender;
    core::ThreadedAppender* threadedAppender;
    log4cpp::Category* category;
};

TEST_FIXTURE(ThreadedAppenderFixture, update)
{
    // Turn off background thread
    threadedAppender->unbackground(true);
    
    CHECK_EQUAL(0u, appender->logEvents.size());

    // Make sure we just call update and nothing happens
    threadedAppender->update(0.0);
    
    // Now log an event, and make sure it only gets through after you call
    // udpate
    category->error("Test");
    CHECK_EQUAL(0u, appender->logEvents.size());

    threadedAppender->update(0.0);
    CHECK_EQUAL(1u, appender->logEvents.size());
    CHECK_EQUAL("Test", appender->logEvents[0].message);
}

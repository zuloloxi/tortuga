/*
 * Copyright (C) 2010 Robotics at Maryland
 * Copyright (C) 2010 Jonathan Wonders <jwonders@umd.edu>
 * All rights reserved.
 *
 * Author: Jonathan Wonders <jwonders@umd.edu>
 * File:  packages/estimation/src/modules/BasicDVLEstimationModule.cpp
 */

// STD Includes
#include <iostream>

// Library Includes
#include <log4cpp/Category.hh>

// Project Includes
#include "vehicle/include/Events.h"
#include "estimation/include/modules/BasicDVLEstimationModule.h"
#include "math/include/Helpers.h"
#include "math/include/Quaternion.h"
#include "math/include/Matrix2.h"

static log4cpp::Category& LOGGER(log4cpp::Category::getInstance("StEstIMU"));

namespace ram {
namespace estimation {

BasicDVLEstimationModule::BasicDVLEstimationModule(core::ConfigNode config,
                                                   core::EventHubPtr eventHub) :
    EstimationModule(eventHub, "BasicDVLEstimationModule")
{
    /* initialization from config values should be done here */
    LOGGER.info("%Vel_b[2] Vel_n[2] Pos_n[2] Timestamp");
}

void BasicDVLEstimationModule::update(core::EventPtr event, 
                                      EstimatedStatePtr estimatedState)
{

    vehicle::RawDVLDataEventPtr ievent =
        boost::dynamic_pointer_cast<vehicle::RawDVLDataEvent>(event);

    /* Return if the cast failed and let people know about it. */
    if(!ievent){
        std::cout << "BasicDVLEstimationModule: update: Invalid Event Type" 
                  << std::endl;
        return;
    }

    /* This is where the estimation should be done
       The result should be stored in estimatedState */

    RawDVLData state = ievent->rawDVLData;
    double timestep = ievent->timestep;
    math::Vector2 vel_b = ievent->velocity_b;

    double yaw = estimatedState->getEstimatedOrientation().getYaw().valueRadians();

    /* calculate current velocity in inertial frame */
    math::Vector2 vel_n = math::nRb(yaw)*vel_b;

    /* grab the old position estimate */
    math::Vector2 oldPos = estimatedState->getEstimatedPosition();
    math::Vector2 oldVel = estimatedState->getEstimatedVelocity();
    
    /* trapezoidal integration for new position */
    math::Vector2 pos_n = oldPos + timestep * (vel_n + oldVel) / 2;

    /* store the new estimates */
    estimatedState->setEstimatedVelocity(vel_n);
    estimatedState->setEstimatedPosition(pos_n);

    /* log the estimates */
    LOGGER.infoStream() << vel_b[0] << " "
                        << vel_b[1] << " "
                        << vel_n[0] << " "
                        << vel_n[1] << " "
                        << pos_n[0] << " "
                        << pos_n[1] << " ";
}

} // namespace estimation
} // namespace ram

# Copyright (C) 2008 Maryland Robotics Club
# Copyright (C) 2008 Joseph Lisee <jlisee@umd.edu>
# All rights reserved.
#
# Author: Joseph Lisee <jlisee@umd.edu>
# File:   packages/python/ram/test/motion/pipe.py

"""
Tests for the ram.motion.pipe module
"""

# STD Imports
import unittest

# Project Imports
import ext.math as math

import ram.motion as motion
import ram.motion.pipe
import ram.test.motion.support as support

class TestHover(support.MotionTest):
    def testAngle(self):
        # Dead center, with yawGain = 1
        pipe = motion.pipe.Pipe(x = 0, y = 0, relativeAngle = 15)
        m = motion.pipe.Hover(pipe = pipe, maxSpeed = 1,
                              maxSidewaysSpeed = 1)
        
        self.motionManager.setMotion(m)
        self.assertAlmostEqual(15, self.controller.yawChange, 3)
        
        # Make sure bad yaw gains are protected
        self.assertRaises(TypeError, motion.pipe.Hover, x = 0, y = 0, 
                          relativeAngle = 0, yawGain = 2)
        
        # Test a yaw gain
        pipe = motion.pipe.Pipe(x = 0, y = 0, relativeAngle = 30)
        m = motion.pipe.Hover(pipe = pipe, maxSpeed = 1,
                              maxSidewaysSpeed = 1, yawGain = 0.5)
        
        self.motionManager.setMotion(m)
        self.assertAlmostEqual(15, self.controller.yawChange, 3)
        
    def testUpperLeftHover(self):
        # All gains set to 1 (default)
        pipe = motion.pipe.Pipe(x = -0.5, y = 0.5, relativeAngle = 0)
        m = motion.pipe.Hover(pipe = pipe, maxSpeed = 1,
                              maxSidewaysSpeed = 1)
        
        self.motionManager.setMotion(m)
        self.assertAlmostEqual(0, self.controller.yawChange, 3)
        self.assertAlmostEqual(0.5, self.controller.speed, 3)
        self.assertAlmostEqual(-0.5, self.controller.sidewaysSpeed, 3)
        
        # Different gains
        pipe = motion.pipe.Pipe(x = -0.5, y = 0.5, relativeAngle = 0)
        m = motion.pipe.Hover(pipe = pipe, maxSpeed = 0.5,
                              maxSidewaysSpeed = 2)
        
        self.motionManager.setMotion(m)
        self.assertAlmostEqual(0, self.controller.yawChange, 3)
        self.assertAlmostEqual(0.25, self.controller.speed, 3)
        self.assertAlmostEqual(-1, self.controller.sidewaysSpeed, 3)
    
    def testLowerRightHover(self):
        # All gains set to 1 (default)
        pipe = motion.pipe.Pipe(x = 0.25, y = -1, relativeAngle = 0)
        m = motion.pipe.Hover(pipe = pipe, maxSpeed = 1,
                              maxSidewaysSpeed = 1)
        
        self.motionManager.setMotion(m)
        self.assertAlmostEqual(0, self.controller.yawChange, 3)
        self.assertAlmostEqual(-1, self.controller.speed, 3)
        self.assertAlmostEqual(0.25, self.controller.sidewaysSpeed, 3)
        
        # Different gains
        pipe = motion.pipe.Pipe(x = 0.25, y = -1, relativeAngle = 0)
        m = motion.pipe.Hover(pipe = pipe, maxSpeed = 3,
                              maxSidewaysSpeed = 0.75)
        
        self.motionManager.setMotion(m)
        self.assertAlmostEqual(0, self.controller.yawChange, 3)
        self.assertAlmostEqual(-3, self.controller.speed, 3)
        self.assertAlmostEqual(0.1875, self.controller.sidewaysSpeed, 3)
    
    def testStop(self):
        # Move the vehicle
        pipe = motion.pipe.Pipe(x = -0.5, y = 0.5, relativeAngle = 0)
        m = motion.pipe.Hover(pipe = pipe, maxSpeed = 1,
                              maxSidewaysSpeed = 1)
        
        self.motionManager.setMotion(m)
        self.assertAlmostEqual(0, self.controller.yawChange, 3)
        self.assertAlmostEqual(0.5, self.controller.speed, 3)
        self.assertAlmostEqual(-0.5, self.controller.sidewaysSpeed, 3)
        
        # Make sure it stops
        self.motionManager.stopCurrentMotion()
        self.assertAlmostEqual(0, self.controller.yawChange, 3)
        self.assertAlmostEqual(0, self.controller.speed, 3)
        self.assertAlmostEqual(0, self.controller.sidewaysSpeed, 3)
    
        
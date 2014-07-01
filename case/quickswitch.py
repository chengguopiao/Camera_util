#!/usr/bin/python
# coding:utf-8

from uiautomatorplug.android import device as d
import commands
import re
import subprocess
import os
import string
import time
import sys
import util 
import unittest

a  = util.Adb()
sm = util.SetCaptureMode()
tb = util.TouchButton()
so = util.SetOption()
#Written by Piao chengguo


#################################

PACKAGE_NAME = 'com.intel.camera22'
ACTIVITY_NAME = PACKAGE_NAME + '/.Camera'

class CameraTest(unittest.TestCase):
    def setUp(self):
        super(CameraTest,self).setUp()
        # rm DCIM folder and refresh from adb shell
        a.cmd('rm','/sdcard/DCIM/100ANDRO')
        a.cmd('refresh','/sdcard/DCIM/100ANDRO')
        #Because default camera after launching is single mode, so we set this step in setUp().
        #Step 1. Launch single capture activity
        a.cmd('launch','com.intel.camera22/.Camera')
        time.sleep(2)
        if  d(text = 'OK').wait.exists(timeout = 3000):
            d(text = 'OK').click.wait()
        sm.switchCaptureMode('single')


    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        self._pressBack(4)
        a.cmd('pm','com.intel.camera22')


# Quick Switch 6

# Test case 1
    def testQuickSwitchtoSinglemode(self):
        """
        Summary:testQuickSwitchtoSinglemode: Quick Switch to Single mode
        Steps:  1.Launch single capture activity
                2.press change mode and then press Video icon to enter video
                3.press change mode icon then choose camera group 
        """    
        # steps 2
        sm.switchCaptureMode('video')      # change video mode
        tb.confirmCameraMode('video')  
        time.sleep(1)
        # steps 3
        sm.switchCaptureMode('single')  # change camera mode
        tb.confirmCameraMode('single')  # check camera mode

# Test case 2
    def testQuickSwitchtoHDRmode(self):
        """
        Summary:testQuickSwitchtoHDRmode: Quick Switch to HDR mode
        Steps:  1.Launch HDR capture activity
                2.press change mode and then press Video icon to enter video
                3.press change mode icon then choose camera group  
        """
        # step 1  
        sm.switchCaptureMode('hdr')    # change hdr mode
        time.sleep(1)
        # step 2
        sm.switchCaptureMode('video')   # change video mode
        tb.confirmCameraMode('video')  
        time.sleep(1)
        # step 3
        sm.switchCaptureMode('single')     # change camera mode
        # check camera mode
        tb.confirmCameraMode('single')

# Test case 3
    def testQuickSwitchtoSmileCammode(self):
        """
        Summary:testQuickSwitchtoSmileCammode: Quick Switch to SmileCam mode
        Steps:  1.Launch SmileCam capture activity
                2.press change mode and then press Video icon to enter video
                3.press change mode icon then choose camera group  
        """  
        # step 1  
        sm.switchCaptureMode('smile')    # change smile mode
        time.sleep(1)
        # step 2
        sm.switchCaptureMode('video')   # change video mode
        time.sleep(1)
        tb.confirmCameraMode('video')
        # step 3
        sm.switchCaptureMode('smile')     # change camera mod

# Test case 4
    def testQuickSwitchtoBurstmode(self):
        """
        Summary:testQuickSwitchtoBurstmode: Quick Switch to Burst mode
        Steps:  1.Launch Burst capture activity
                2.press change mode and then press panorama icon to enter panorama
                3.press change mode icon then choose Multi group  
        """  
        # step 1  
        sm.switchCaptureMode('burstfast')    # change burst mode
        time.sleep(1)
        tb.confirmCameraMode('single')  
        # step 2
        sm.switchCaptureMode('panorama')   # change panorama mode
        time.sleep(1)
        tb.confirmCameraMode('panorama') 
        # step 3
        sm.switchCaptureMode('burstfast')     # change burst mode
        # check camera mode
        tb.confirmCameraMode('single')        

# Test case 5    
    def testQuickSwitchtoPerfectShotmode(self):
        """
        Summary:testQuickSwitchtoPerfectShotmode: Quick Switch to Perfect Shot mode 
        Steps:  1.Launch Perfect capture activity
                2.press change mode and then press panorama icon to enter panorama
                3.press change mode icon then choose Multi group  
        """ 
        # step 1
        sm.switchCaptureMode('perfectshot')    # change perfectshot mode
        time.sleep(1)
        tb.confirmCameraMode('perfectshot')  
        # step 2
        sm.switchCaptureMode('panorama')   # change panorama mode
        time.sleep(1)
        tb.confirmCameraMode('panorama') 
        # step 3
        sm.switchCaptureMode('perfectshot')    # change perfectshot mode
        time.sleep(1)
        tb.confirmCameraMode('perfectshot') 

# Test case 6
    def testQuickSwitchtoGallery(self):
        """
        Summary:testQuickSwitchtoGallery: Quick Switch to gallery 
        Steps:  1. Launch camera 
                2. Touch shutter button to capture a picture
                3. Touch the thubnail icon to view it in gallery 
        """ 
        # step 2
        time.sleep(1)
        tb.captureAndCheckPicCount('single',2)  # capture picture
        time.sleep(1)                                    
        d(resourceId = 'com.intel.camera22:id/thumbnail').click.wait()   # enter gallery
        time.sleep(2)
        # step 2
        d.click(1200,800)
        time.sleep(1)
        assert d(resourceId = 'android:id/home').wait.exists(timeout = 3000)




######################################



    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        time.sleep(1)
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes):
        for i in range(1,touchtimes+1):
            d.press('back')

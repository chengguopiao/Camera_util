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

# PATH
PATH ='/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml '
PATH1='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml '
# key
EXPOSURE_KEY ='| grep pref_camera_exposure_key'
IOS_KEY='| grep pref_camera_iso_key'
LOCATION_KEY ='| grep pref_camera_geo_location_key'


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
        sm.switchCaptureMode('panorama')   # change panorama mode
        time.sleep(1)
        tb.confirmCameraMode('panorama')

    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        self._pressBack(4)
        a.cmd('pm','com.intel.camera22')

### Panorama capture 12 ###
# Test case 1
    def testPanoramaCaptureWithExposureAuto(self):
    	'''
        Summary:testPanoramaCapturepictureWithGeoLocationOn: capture Panorama picture in geolocation on mode
        Steps: 
    	1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure auto
        3.Touch shutter button
        4.Touch shutter button to capture picture
        '''
        # step 2
        so.setCameraOption('Exposure','0')
        # step 4~5
        tb.confirmSettingMode('Exposure','0')
        tb.captureAndCheckPicCount('smile',2)

# Test case 2
    def testPanoramaCaptureWithExposurePlusOne(self):   
        '''
        Summary:testPanoramaCaptureWithExposurePlusOne:capture Panorama picture with Exposure +1
        Steps  :
        1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure 1
        3.Touch shutter button 
        4.Touch shutter button to capture picture
        '''

        # step 2
        so.setCameraOption('Exposure','3')
        # step 4~5
        tb.confirmSettingMode('Exposure','3')
        tb.captureAndCheckPicCount('smile',2)

# Test case 3
    def testPanoramaCaptureWithExposurePlusTwo(self):
        '''
        Summary:testPanoramaCapturePictureWithExposurePlusOne: capture Panorama picture with Exposure +2
        Steps: 
        1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure 2
        3.Touch shutter button 
        4.Touch shutter button to capture picture
        '''

        # step 2
        so.setCameraOption('Exposure','6')
        # step 4~5
        tb.confirmSettingMode('Exposure','6')
        tb.captureAndCheckPicCount('smile',2)

# Test case 4
    def testPanoramaCaptureWithExposureRedOne(self):
        '''
        Summary:testPanoramaCaptureWithExposureRedOne: capture Panorama picture with Exposure -1
        Steps:
        1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure -1
        3.Touch shutter button 
        4.Touch shutter button to capture picture
        '''   

        # step 2
        so.setCameraOption('Exposure','-3')
        # step 4~5
        tb.confirmSettingMode('Exposure','-3')
        tb.captureAndCheckPicCount('smile',2)

# Test case 5    
    def testPanoramaCaptureWithExposureRedTwo(self):
        '''
        Summary:testPanoramaCaptureWithExposureRedTwo: capture Panorama picture with Exposure -2
        Steps:
        1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure -1
        3.Touch shutter button 
        4.Touch shutter button to capture picture
        '''   

        # step 2
        so.setCameraOption('Exposure','-6')
        # step 4~5
        tb.confirmSettingMode('Exposure','-6')
        tb.captureAndCheckPicCount('smile',2)

# Test case 6
    def testPanoramaCapturepictureWithGeoLocationOn(self):
        """
        Summary:testPanoramaCapturepictureWithGeoLocationOn: capture Panorama picture in geolocation on mode
        Steps:  1.Launch Panorama activity
                2.Check geo-tag ,set to ON
                3.Touch shutter button to capture picture
        """ 
        # step 1

        # step 2
        so.setCameraOption('Geo Location','on')
        # step 4~5
        tb.confirmSettingMode('Geo Location','on')
        tb.captureAndCheckPicCount('smile',2)

# Test case 7
    def testPanoramaCapturepictureWithGeoLocationOff(self):
        """
        Summary:testPanoramaCapturepictureWithGeoLocationOff: capture Panorama picture in geolocation off mode
        Steps:  1.Launch Panorama activity
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture picture
                4.Exit activity
        """ 


        # step 2
        so.setCameraOption('Geo Location','off')
        # step 4~5
        tb.confirmSettingMode('Geo Location','off')
        tb.captureAndCheckPicCount('smile',2)

# Test case 8
    def testPanoramaCapturepictureWithISOSettingAuto(self):
        """
        Summary:testPanoramaCapturepictureWithISOSettingAuto: Capture image with ISO Setting Auto
        Steps:  1.Launch Panorama activity
                2.Touch Geo-tag setting  icon,Set Geo-tag OFF
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity 
        """

        # step 2
        so.setCameraOption('ISO','iso-auto')
        # step 4~5
        tb.confirmSettingMode('ISO','iso-auto')
        tb.captureAndCheckPicCount('smile',2)

# Test case 9    
    def testPanoramaCapturepictureWithISOSetting100(self):
        """
        Summary:testPanoramaCapturepictureWithISOSetting100: Capture image with ISO Setting 100
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 100
        3.Touch shutter button
        4.Touch shutter button to capture picture
        """

        # step 2
        so.setCameraOption('ISO','iso-100')
        # step 4~5
        tb.confirmSettingMode('ISO','iso-100')
        tb.captureAndCheckPicCount('smile',2)

# Test case 10
    def testPanoramaCapturepictureWithISOSetting200(self):
        """
        Summary:testPanoramaCapturepictureWithISOSetting200: Capture image with ISO Setting 200
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 200
        3.Touch shutter button
        4.Touch shutter button to capture picture  
        """

        # step 2
        so.setCameraOption('ISO','iso-200')
        # step 4~5
        tb.confirmSettingMode('ISO','iso-200')
        tb.captureAndCheckPicCount('smile',2)

# Test case 11
    def testPanoramaCapturepictureWithISOSetting400(self):
        """
        Summary:testPanoramaCapturepictureWithISOSetting400: Capture image with ISO Setting 400
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 400
        3.Touch shutter button
        4.Touch shutter button to capture picture
        5.Exit  activity 
        """

        # step 2
        so.setCameraOption('ISO','iso-400')
        # step 4~5
        tb.confirmSettingMode('ISO','iso-400')
        tb.captureAndCheckPicCount('smile',2)

# Test case 12
    def testPanoramaCapturepictureWithISOSetting800(self):
        """
        Summary:testPanoramaCapturepictureWithISOSetting800: Capture image with ISO Setting 800
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 800
        3.Touch shutter button
        4.Touch shutter button to capture picture
        """

        # step 2
        so.setCameraOption('ISO','iso-800')
        # step 4~5
        tb.confirmSettingMode('ISO','iso-800')
        tb.captureAndCheckPicCount('smile',2)  





#######################################

    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        time.sleep(1)
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes):
        for i in range(1,touchtimes+1):
            d.press('back')

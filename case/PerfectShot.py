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
SCENE_KEY ='| grep pref_camera_scenemode_key'


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
        else:
            assert d(resourceId = 'com.intel.camera22:id/shutter_button'),'Launch camera failed!!'
        sm.switchCaptureMode('perfectshot')   # change panorama mode
        time.sleep(1)
        tb.confirmCameraMode('perfectshot')

    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        self._pressBack(4)
        a.cmd('pm','com.intel.camera22')



# PerfectShot capture 14
# Test case 1
    def testPerfectShotCaptureWithExposureAuto(self):
        """
        Summary:testCaptureWithExposureZero: Take burst piture with exposure 0
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to 0
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Exposure','0')
        # step 4~5
        tb.confirmSettingMode('Exposure','0')
        tb.captureAndCheckPicCount('single',2)

# Test case 2        
    def testPerfectShotCaptureWithExposurePlusOne(self):
        """
        Summary:testCaptureWithExposurePlusOne: Take burst piture with exposure +1
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to +1
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Exposure','3')
        # step 4~5
        tb.confirmSettingMode('Exposure','3')
        tb.captureAndCheckPicCount('single',2)

# Test case 3    
    def testPerfectShotCaptureWithExposurePlusTwo(self):
        """
        Summary:testCapturePictureWithExposurePlusOne: Take burst piture with exposure +2
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to +2
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Exposure','6')
        # step 4~5
        tb.confirmSettingMode('Exposure','6')
        tb.captureAndCheckPicCount('single',2)
# Test case 4
    def testPerfectShotCaptureWithExposureRedOne(self):
        """
        Summary:testCaptureWithExposureRedOne: Take burst piture with exposure -1
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to -1
                3.Touch shutter button to capture picture
        """  
        

        # step 2
        # step 2
        so.setCameraOption('Exposure','-3')
        # step 4~5
        tb.confirmSettingMode('Exposure','-3')
        tb.captureAndCheckPicCount('single',2)

# Test case 5
    def testPerfectShotCaptureWithExposureRedTwo(self):
        """
        Summary:testCaptureWithExposureRedTwo: Take burst piture with exposure -2
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to -2
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Exposure','-6')
        # step 4~5
        tb.confirmSettingMode('Exposure','-6')
        tb.captureAndCheckPicCount('single',2)

# Test case 6
    def testPerfectShotCapturePictureWithScenesAuto(self):
        """
        Summary:testCapturePictureWithScenesAuto: Take picture with set scenes to auto
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to auto
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Scenes','auto')
        # step 4~5
        tb.confirmSettingMode('Scenes','auto')
        tb.captureAndCheckPicCount('single',2)

# Test case 7
    def testPerfectShotCapturePictureWithScenesSport(self):
        """
        Summary:testCapturePictureWithScenesSport: Take picture with set scenes to Sports
        Steps:  1Launch perfect shot activity
                2.Check scence mode ,set mode to Sports
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Scenes','sports')
        # step 4~5
        tb.confirmSettingMode('Scenes','sports')
        tb.captureAndCheckPicCount('single',2)

# Test case 8
    def testPerfectShotCapturePictureWithScenesNightPortrait(self):
        """
        Summary:testCapturePictureWithScenes NightPortrait: Capture image with Scene modeNightPortrait
        Steps:  1.Launch perfect shot activity
                2.Set Scene mode Night-portrait
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Scenes','night-portrait')
        # step 4~5
        tb.confirmSettingMode('Scenes','night-portrait')
        tb.captureAndCheckPicCount('single',10)       

# Test case 9
    def testPerfectShotCapturePictureWithScenesLandscape(self):
        """
        Summary:testCapturePictureWithScenesLandscape: Take picture with set scenes to landscape
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to landscape
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Scenes','landscape')
        # step 4~5
        tb.confirmSettingMode('Scenes','landscape')
        tb.captureAndCheckPicCount('single',2)     

# Test case 10
    def testPerfectShotCapturePictureWithScenesPortrait(self):
        """
        Summary:testCapturePictureWithScenesSport: Take picture with set scenes to portrait
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to portrait
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Scenes','portrait')
        # step 4~5
        tb.confirmSettingMode('Scenes','portrait')
        tb.captureAndCheckPicCount('single',2)       

# Test case 11
    def testPerfectShotCapturePictureWithScenesNight(self):
        """
        Summary:testCapturePictureWithScenesNight: Take picture with set scenes to night
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to night
                3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Scenes','night')
        # step 4~5
        time.sleep(3)
        tb.confirmSettingMode('Scenes','night')
        tb.captureAndCheckPicCount('single',10)  

# Test case 12
    def testPerfectShotCapturePictureWithScenesBarcode(self):
        """
        Summary:testCapturePictureWithScenesBarcode: Capture image with Scene mode Barcode
        Steps:  1.Launch perfect shot activity
        2.Set Scene mode Barcode
        3.Touch shutter button to capture picture
        """
        

        # step 2
        so.setCameraOption('Scenes','barcode')
        # step 4~5
        tb.confirmSettingMode('Scenes','barcode')
        tb.captureAndCheckPicCount('single',2) 

# Test case 13
    def testPerfectShotCapturepictureWithGeoLocationOn(self):
        """
        Summary:testCapturepictureWithGeoLocationOn: capture PerfectShot picture in geolocation on mode
        Steps:  1.Launch perfect shot activity
                2.Check geo-tag ,set to ON
                3.Touch shutter button to capture picture
        """ 
        

        # step 2
        so.setCameraOption('Geo Location','on')
        # step 4~5
        tb.confirmSettingMode('Geo Location','on')
        tb.captureAndCheckPicCount('single',2)  

# Test case 14
    def testPerfectShotCapturepictureWithGeoLocationOff(self):
        """
        Summary:testCapturepictureWithGeoLocationOff: capture PerfectShot picture in geolocation off mode
        Steps:  1.Launch perfect shot activity
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture  picture
        """ 
        
        # step 2
        so.setCameraOption('Geo Location','off')
        # step 4~5
        tb.confirmSettingMode('Geo Location','off')
        tb.captureAndCheckPicCount('single',2)  

####################################################################################################################

    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        time.sleep(1)
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes):
        for i in range(1,touchtimes+1):
            d.press('back')

#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import commands
import re
import subprocess
import os
import string
import time
import sys

##################################################################################################################
a  = util.Adb()
sm = util.SetMode()
tb = util.TouchButton()

#################################################################################################################
CPTUREBUTTON_RESOURCEID ='com.intel.camera22:id/btn_mode'
FRONTBACKBUTTON_DESCR = 'com.intel.camera22:id/shortcut_mode_2'
CPTUREPOINT='adb shell input swipe 2200 1095 2200 895 '
DRAWUP_CAPTUREBUTTON='adb shell input swipe 2200 1095 2200 895 '


CAMERA_ID = 'adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'
#################################################################################################################



class TouchButton():

    def takePicture(self,status):
        # capture single image
        def _singlecapture():
            d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait()
            time.sleep(2)
        # capture smile image
        def _smilecapture():
            d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait()
            time.sleep(2)
            d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait()
        # capture single image by press 2s
        def _longclickcapture():
            commands.getoutput(DRAWUP_CAPTUREBUTTON + '2000')
            time.sleep(2) 
        #Dictionary
        takemode={'single':_singlecapture,'smile':_smilecapture,'longclick':_longclickcapture}    
        takemode[status]()
     
    def takePictureCustomTime(self,status): 
        # capture image by press Custom Time
        commands.getoutput(DRAWUP_CAPTUREBUTTON+ (status+'000'))



    def takeVideo(self,status):
        # Start record video
        d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait() 
        # Set recording time
        time.sleep(status - 2)
        #Stop record video
        d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait() 
        return True

    def switchBackOrFrontCamera(self,status,):
        d(resourceId = FRONTBACKBUTTON_DESCR).click.wait()
        #Dictionary
        camerastatus = {'back': '0','front':'1'}  
        # Get the current camera status
        currentstatus = commands.getoutput(CAMERA_ID)
        # Confirm the current status of the user is required
        if currentstatus.find(camerastatus.get(status)) == -1:
            time.sleep(1)
            # set the camera status
            d(resourceId = FRONTBACKBUTTON_DESCR).click.wait()
            time.sleep(3)
            # Get the current camera status
            currentstatus = commands.getoutput(CAMERA_ID)
            # check the result
            if currentstatus.find(camerastatus.get(status)) != -1:
                print ('set camera is '+status)
                return True
            else:
                print ('set camera is '+status+' fail')
                return False
        else:
            print('Current camera is ' + status)

    def _captureAndCheckPicCount(self,capturemode,format,delaytime):
        beforeNo = commands.getoutput('adb shell ls /sdcard/DCIM/100ANDRO/* | grep '+ format +' | wc -l') #Get count before capturing
        TB.takePicture(capturemode)
        time.sleep(delaytime) #Sleep a few seconds for file saving
        afterNo = commands.getoutput('adb shell ls /sdcard/DCIM/100ANDRO/* | grep '+ format +' | wc -l') #Get count after taking picture
        if beforeNo == afterNo: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture/video failed!')

    def _confirmSettingMode(self,sub_mode,option):
        if sub_mode == 'location':
            result = commands.getoutput('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep '+ sub_mode)
            if result.find(option) == -1:
                self.fail('set camera setting ' + sub_mode + ' to ' + option + ' failed')
        else:
            result = commands.getoutput('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep ' + sub_mode)
            if result.find(option) == -1:
                self.fail('set camera setting ' + sub_mode + ' to ' + option + ' failed')            
    
    def _confirmCameraMode(self,mode):
        result = commands.getoutput('cat','/data/data/com.intel.camera22/shared_prefs/mode_selected.xml| grep \'value="%s"\''%mode)
        if result.find(mode) == -1:
            self.fail('set camera '+mode +' mode fail')               

       

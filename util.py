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

##################################################################################################################
#ADB() Class variable
ADB            = 'adb'
ADB_SHELL      = ADB + ' shell'
ADB_DEVICES    = ADB + ' devices'
ANDROID_SERIAL ='ANDROID_SERIAL'
##################################################################################################################
#SetCaptureMode() Class variable
MODE_LIST = ['single','depth','panorama','burst','perfectshot','video']
POP_MODE  = {'smile':"Smile\nOFF",
             'hdr':"HDR\nOFF",
             'burstfast':'FAST',
             'burstslow':'SLOW'
             }
##################################################################################################################
#SetOption() Class variable
Exposure          = ['-6','-3','0','3','6'] #_0_0
ISO               = ['iso-auto','iso-100','iso-200','iso-400','iso-800'] #_0_0
White_Balance     = ['auto','incandescent','fluorescent','cloudy-daylight','daylight'] #_0_0
Switch_Camera     = ['1','0'] #_0
Face_Detection    = ['off','on'] #_0
Scenes            = ['auto','landscape','portrait','night','sports','night-portrait'] #_0_0
Self_Timer        = ['0','3','5','10'] #_0_0
Geo_Location      = ['off','on'] #_0
Picture_Size      = ['WideScreen','StandardScreen'] #_0_0
Hints             = ['off','on'] #_0_0
Settings_Layout   = ['Mini','Large'] #_0
Shortcut_Button_1 = ['exposure','iso','whitebalance','flashmode','id','fdfr','scenemode','delay','geo'] #_0
Shortcut_Button_2 = ['exposure','iso','whitebalance','flashmode','id','fdfr','scenemode','delay','geo'] #_0
Shortcut_Button_3 = ['exposure','iso','whitebalance','flashmode','id','fdfr','scenemode','delay','geo'] #_0

SETTINGS_0        = ['Switch_Camera', 'Face_Detection', 'Geo_Location', 'Settings_Layout', 'Shortcut_Button_1', 'Shortcut_Button_2', 'Shortcut_Button_3']
SETTINGS_0_0      = ['Exposure', 'ISO', 'White_Balance', 'Scenes', 'Self_Timer', 'Picture_Size', 'Hints']

DICT_OPTION_KEY   = {'Exposure'         : 'pref_camera_exposure_key',
                     'ISO'              : 'pref_camera_iso_key',
                     'White_Balance'    : 'pref_camera_whitebalance_key',
                     'Switch_Camera'    : 'pref_camera_id_key',
                     'Face_Detection'   : 'pref_fdfr_key',
                     'Scenes'           : 'pref_camera_scenemode_key',
                     'Self_Timer'       : 'pref_camera_delay_shooting_key',
                     'Geo_Location'     : 'pref_camera_geo_location_key',
                     'Picture_Size'     : 'pref_camera_picture_size_key',
                     'Hints'            : 'pref_camera_hints_key',
                     'Settings_Layout'  : 'pref_settings_layout_key',
                     'Shortcut_Button_1': 'pref_shortcut_button1_key',
                     'Shortcut_Button_2': 'pref_shortcut_button2_key',
                     'Shortcut_Button_3': 'pref_shortcut_button3_key'}

DICT_OPTION_NAME  = {'Exposure'         : Exposure,
                     'ISO'              : ISO,
                     'White_Balance'    : White_Balance,
                     'Switch_Camera'    : Switch_Camera,
                     'Face_Detection'   : Face_Detection,
                     'Scenes'           : Scenes,
                     'Self_Timer'       : Self_Timer,
                     'Geo_Location'     : Geo_Location,
                     'Picture_Size'     : Picture_Size,
                     'Hints'            : Hints,
                     'Settings_Layout'  : Settings_Layout,
                     'Shortcut_Button_1': Shortcut_Button_1,
                     'Shortcut_Button_2': Shortcut_Button_2,
                     'Shortcut_Button_3': Shortcut_Button_3}
                     
DEFAULT_OPTION    = {'Exposure'         : Exposure[2],
                     'ISO'              : ISO[0],
                     'White_Balance'    : White_Balance[0],
                     'Switch_Camera'    : Switch_Camera[1],
                     'Face_Detection'   : Face_Detection[1],
                     'Scenes'           : Scenes[0],
                     'Self_Timer'       : Self_Timer[0],
                     'Geo_Location'     : Geo_Location[1],
                     'Picture_Size'     : Picture_Size[0],
                     'Hints'            : Hints[0],
                     'Settings_Layout'  : Settings_Layout[0],
                     'Shortcut_Button_1': Shortcut_Button_1[3],
                     'Shortcut_Button_2': Shortcut_Button_2[4],
                     'Shortcut_Button_3': Shortcut_Button_3[5]}
                     
##################################################################################################################
#TouchButton() Class variable
CONFIRM_MODE_LIST       = ['video','single','depth','panorama','burst','perfectshot']
CPTUREBUTTON_RESOURCEID = 'com.intel.camera22:id/btn_mode'
FRONTBACKBUTTON_DESCR   = 'com.intel.camera22:id/shortcut_mode_2'
CPTUREPOINT             = 'adb shell input swipe 2200 1095 2200 895 '
DRAWUP_CAPTUREBUTTON    = 'adb shell input swipe 2200 1095 2200 895 '
CAMERA_ID               = 'adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'

##################################################################################################################

class Adb():

    '''
    This method support user execute adb commands,support push,pull,cat,refresh,ls,launch,rm

    usage:  adb=Adb()
    ------------------------------------------------------------------------------------------------------------
    | adb.cmd('cat','xxxx/xxx.xml')                 |  adb shell cat xxxx/xxx.xml,return cat result             | 
    ------------------------------------------------------------------------------------------------------------
    | adb.cmd('refresh','/sdcard/')                 |  refresh media file under path /sdcard/,return ture/false |
    ------------------------------------------------------------------------------------------------------------
    | adb.cmd('ls','/sdcard/')                      |  get the file number under path /sdcard/,return number    |                         
    ------------------------------------------------------------------------------------------------------------    
    | adb.cmd('rm','xxxx/xxxx.jpg')                 |  delete xxxx/xxx.jpg,return true/false                    |
    ------------------------------------------------------------------------------------------------------------ 
    | adb.cmd('launch','com.intel.camera22/.Camera')|  launch social camera app,return adb commands             |
    ------------------------------------------------------------------------------------------------------------
    '''
    def cmd(self,action,path,t_path=None):
        #export android serial
        if not os.environ.has_key(ANDROID_SERIAL):
            self._exportANDROID_SERIAL()
        #adb commands
        action1={
        'refresh':self._refreshMedia,
        'ls':self._getFileNumber,
        'cat':self._catFile,
        'launch':self._launchActivity,
        'rm':self._deleteFile,
        'pm':self._resetApp
        }
        action2=['pull','push']
        if action in action1:
            return action1.get(action)(path)
        elif action in action2:
            return self._pushpullFile(action,path,t_path)
        else:
            raise Exception('commands is unsupported,only support [push,pull,cat,refresh,ls,launch,rm] now')

    def _resetApp(self,path):
        p = self._shellcmd('pm clear ' + path)
        return p        

    def _refreshMedia(self,path):
        p = self._shellcmd('am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://' + path)
        out = p.stdout.read().strip()
        if 'result=0' in out:
            return True
        else:
            return False

    def _getFileNumber(self,path):
        p = self._shellcmd('ls ' + path + ' | wc -l')
        out = p.stdout.read().strip()
        return string.atoi(out)


    def _launchActivity(self,component):
        p = self._shellcmd('am start -n ' + component)
        return p

    def _catFile(self,path):
        p = self._shellcmd('cat ' + path)
        out = p.stdout.read().strip()
        return out

    def _deleteFile(self,path):
        p = self._shellcmd('rm -r  ' + path)
        p.wait()
        number = self._getFileNumber(path)
        if number == 0 :
            return True
        else:
            return False

    def _pushpullFile(self,action,path,t_path):
        beforeNO = self._getFileNumber(t_path)
        p = self._t_cmd(action + ' ' + path + ' ' + t_path)
        p.wait()
        afterNO = self._getFileNumber(t_path)
        if afterNO > beforeNO:
            return True
        else:
            return False

    def _exportANDROID_SERIAL(self):
        #get device number
        device_number = self._getDeviceNumber()
        #export ANDROID_SERIAL=xxxxxxxx
        os.environ[ANDROID_SERIAL] = device_number

    def _getDeviceNumber(self):
        #get device number, only support 1 device now
        #show all devices
        cmd = ADB_DEVICES
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
        out=p.stdout.read().strip()
        #out is 'List of devices attached /nRHBxxxxxxxx/t device'
        words_before = 'List of devices attached'
        word_after = 'device'
        #get device number through separate str(out)
        device_number = out[len(words_before):-len(word_after)].strip()
        if len(device_number) >= 17:
            raise Exception('more than 1 device connect,only suppport 1 device now')
        else:
            return device_number

    def _shellcmd(self,func):
        cmd = ADB_SHELL + ' ' + func
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    def _t_cmd(self,func):
        cmd = ADB + ' ' + func
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

class SetCaptureMode():

    def _swipeCaptureList(self,mode): 
        mode_index = MODE_LIST.index(mode)
        for i in range(mode_index):
            # mode image coordinate: right_x_coordinate = 2252 left_x_coordinate = 2252. swipe from right to left.
            d.swipe(2252,1044,2120,1044)

    def _clickCaptureMode(self):
        # mode image center coordinate (2195,975)
        d.click(2195,975)

    def switchCaptureMode(self,mode):
        '''
        Usage: This method is used to switch social camera 2.3 capture mode.
        e.g. SetCaptureMode.switchCaptureMode('single')
        '''
        d(description = 'Show switch camera mode list').click.wait()
        if mode == 'smile' or mode == 'hdr':
            d(text = POP_MODE[mode]).click.wait()
        elif mode == 'burstfast' or mode == 'burstslow':
            self._swipeCaptureList('burst')
            d(text = POP_MODE[mode]).click.wait()
        else:
            self._swipeCaptureList(mode)
            self._clickCaptureMode()

class SetOption():

    def _getOptionOrdinate(self,optiontext):
        optiontitlebounds = d(text = optiontext).info.get('bounds')
        optiony = (optiontitlebounds['top'] + optiontitlebounds['bottom'])/2
        return optiony

    def _getOptionWidthAndHeight(self):
        optionbounds = d(resourceId = 'com.intel.camera22:id/rl').info.get('bounds')
        optionwidth  = (optionbounds['right'] - optionbounds['left'])
        optionheight = (optionbounds['bottom'] - optionbounds['top'])
        return optionwidth, optionheight

    def _getSettingBounds(self):
        rightoptionbounds = d(resourceId = 'com.intel.camera22:id/camera_setting_layout').info.get('bounds')
        rightx  = rightoptionbounds['right']
        topy    = rightoptionbounds['top']
        bottomy = rightoptionbounds['bottom']
        centerx = (rightoptionbounds['right'] - rightoptionbounds['left'])/2
        return rightx, topy, bottomy, centerx

    def _getFirstItem(self):
        optionbounds = d(resourceId = 'com.intel.camera22:id/rl').info.get('bounds')
        xfirstitem   = (optionbounds['left'] + optionbounds['right'])/2
        return xfirstitem

    def _slideSettingListUp(self):
        x   = self._getSettingBounds()[3]
        y_1 = self._getSettingBounds()[2] - self._getOptionWidthAndHeight()[1]
        y_2 = self._getSettingBounds()[1] - self._getOptionWidthAndHeight()[1]
        d.swipe(x, y_1, x, y_2)

    def _slideOptionLeftToRight(self,optiontext,diffindex):
        # --->>>
        x_1 = self._getSettingBounds()[0] - self._getOptionWidthAndHeight()[0]
        x_2 = self._getSettingBounds()[0]
        y   = self._getOptionOrdinate(optiontext)
        x_i = self._getOptionWidthAndHeight()[0] * (diffindex - 1)
        d.swipe(x_1, y, x_2 + x_i, y)

    def _slideOptionRightToLeft(self,optiontext,diffindex):
        # <<<---
        x_1 = self._getSettingBounds()[0] - self._getOptionWidthAndHeight()[0]
        x_2 = self._getSettingBounds()[0] - self._getOptionWidthAndHeight()[0] - self._getOptionWidthAndHeight()[0]
        y   = self._getOptionOrdinate(optiontext)
        x_i = self._getOptionWidthAndHeight()[0] * (diffindex - 1)
        d.swipe(x_1, y, x_2 - x_i, y)

    def setCameraOption(self,optiontext,option):
        '''
           ***Usage***
            To set Scenes as 'sports':
                self.setCameraOption('Scenes','sports')

                You may need use the arguements that have been defined at the top of this file
        '''
        d(resourceId = 'com.intel.camera22:id/camera_settings').click.wait()
        trytimes = 1
        while d(text = optiontext).wait.gone(timeout = 2000) and trytimes < 5:
            self._slideSettingListUp()
            trytimes = trytimes + 1
        newoptiontext = optiontext.replace(' ', '_')
        cated_0_0 = int(commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | wc -l'))
        #If it is the first time launching camera, there are only 4 lines in _0_0.xml. Need more logic.
        if cated_0_0 > 4:
            #Get the current option
            if newoptiontext not in SETTINGS_0:
                stringcated = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep %s' %DICT_OPTION_KEY[newoptiontext])
                currentoption = (((stringcated.split('>'))[1]).split('<'))[0]
            else:
                stringcated = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep %s' %DICT_OPTION_KEY[newoptiontext])
                currentoption = (((stringcated.split('>'))[1]).split('<'))[0]
            #Get the current option's index and compare it with the target option
            currentindex = DICT_OPTION_NAME[newoptiontext].index(currentoption)
            targetindex  = DICT_OPTION_NAME[newoptiontext].index(option)
            diffindex = abs(currentindex - targetindex)
            #Settinglayout do change UI very much, so need one more logic
            settinglayout = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_settings_layout_key')
            if settinglayout.find('Large')!= -1:
                if currentindex != targetindex:
                    d.click(self._getFirstItem() + self._getOptionWidthAndHeight()[1] * targetindex, self._getOptionOrdinate(optiontext))
                else:
                    d(resourceId = 'com.intel.camera22:id/mini_layout_view').click.wait()
            else:
                #If current option is just the target option, do nothing('pass').
                if currentindex > targetindex:
                    self._slideOptionLeftToRight(optiontext, diffindex)
                elif currentindex < targetindex:
                    self._slideOptionRightToLeft(optiontext, diffindex)
                else:
                    #Neither higher nor lower than the target option, that means the current option is just the target one.
                    d(resourceId = 'com.intel.camera22:id/mini_layout_view').click.wait()
        else:
            currentoption = DEFAULT_OPTION[newoptiontext]
            currentindex = DICT_OPTION_NAME[newoptiontext].index(currentoption)
            targetindex  = DICT_OPTION_NAME[newoptiontext].index(option)
            diffindex = abs(currentindex - targetindex)
            if currentindex > targetindex:
                self._slideOptionLeftToRight(optiontext, diffindex)
            elif currentindex < targetindex:
                self._slideOptionRightToLeft(optiontext, diffindex)
            else:
                #Neither higher nor lower than the target option, that means the current option is just the target one.
                d(resourceId = 'com.intel.camera22:id/mini_layout_view').click.wait()
        oldoption    = DICT_OPTION_NAME[newoptiontext].index(DEFAULT_OPTION[newoptiontext])
        targetoption = DICT_OPTION_NAME[newoptiontext].index(option)
        if oldoption != targetoption:
            if newoptiontext not in SETTINGS_0:
                resultoption = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep %s' %DICT_OPTION_KEY[newoptiontext])
                if resultoption.find(option) == -1:
                    raise Exception('Set camera setting <' + optiontext + '> to <' + option + '> failed')
            else:
                resultoption = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep %s' %DICT_OPTION_KEY[newoptiontext])
                if resultoption.find(option) == -1:
                    raise Exception('Set camera setting <' + optiontext + '> to <' + option + '> failed')
        else:
            #If the current option is the default one, there is no need for confirmation
            pass

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

    def switchBackOrFrontCamera(self,status):
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
    
    def confirmSettingMode(self,sub_mode,option):
        mode = sub_mode.replace(' ', '_')
        if option == DEFAULT_OPTION[mode]:
            print ('current is '+ sub_mode + option +' mode' )
        else:            
            if mode not in SETTINGS_0:
                result = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep ' + DICT_OPTION_KEY[mode])
                if result.find(option) == -1:
                    raise Exception('set camera setting ' + mode + ' to ' + option + ' failed') 
            else:
                result = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep '+ DICT_OPTION_KEY[mode])
                if result.find(option) == -1:
                    raise Exception('set camera setting ' + mode + ' to ' + option + ' failed')             
    
    def confirmCameraMode(self,mode):
        mode_index = CONFIRM_MODE_LIST.index(mode) -1
        mode_new   = str(mode_index)
        result = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/mode_selected.xml| grep \'value="%s"\''%mode_new)
        if result.find(mode_new) == -1:
            raise Exception('set camera '+mode +' mode fail')


    def captureAndCheckPicCount(self,capturemode,delaytime=0):
        d = { 'single':'jpg', 'video':'mp4', 'smile':'jpg', 'longclick':'jpg'} 
        beforeNo = commands.getoutput('adb shell ls /sdcard/DCIM/100ANDRO/* | grep '+ d[capturemode] +' | wc -l') #Get count before capturing
        if capturemode == 'video':
            self.takeVideo(delaytime)
        else:
            self.takePicture(capturemode)
        time.sleep(delaytime) #Sleep a few seconds for file saving
        afterNo = commands.getoutput('adb shell ls /sdcard/DCIM/100ANDRO/* | grep '+ d[capturemode] +' | wc -l') #Get count after taking picture
        result = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/mode_selected.xml| grep \'value="3"\'')
        if result.find('value="3"') != -1:
            if string.atoi(beforeNo) != string.atoi(afterNo) - 10:
               raise Exception('Taking picture/video failed!')
        else:
            if string.atoi(beforeNo) == string.atoi(afterNo) :#If the count does not raise up after capturing, case failed
                raise Exception('Taking picture/video failed!')

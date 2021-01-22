# -*- coding: utf-8 -*-

__author__ = 'Creeper19472'

'''
// Camera.py

This py file uses api.py to control your camera. DEMO.
This program will disable the encryption of your camera
at the beginning and re-enable it after the program ends.

This program actually only uses part of the functions of
api.py, and you can find other usages in api.py.

To use this program, please go to open.ys7.com to apply
for a developer account and obtain appKey and appSecret.

In addition, you also need to obtain the serial number
of the device you want to control. You can use the
experience camera provided by the developer platform, or
use the private camera in your account.

Please fill in this information in config.ini.

At the same time you also need to pay attention: not all
devices support some functions in this program. This may
cause some errors. The device model we used when developing
this program was C6C.

Note: DON'T USE THIS PROGRAM TOO OFTEN.

'''

import sys, time, configparser
from apscheduler.schedulers.background import BackgroundScheduler
from api import CameraAPI


class SchedulerAction():
    def enableCamera():
        result = CameraAPI.SwitchScene(accessToken, device, 0)

    def disableCamera():
        result = CameraAPI.SwitchScene(accessToken, device, 1)


config = configparser.ConfigParser()
config.read("./config.ini")

device = config['General']['deviceSerial']
devcode = config['General']['validateCode']
appKey = config['General']['appKey']
appSecret = config['General']['appSecret']

result = CameraAPI.GetToken(appKey, appSecret)
if result == False:
    print('Failed to get accessToken. Do you wish to enter it manually?')
    accessToken = input('accessToken: ')
    if bool(accessToken) == False:
        sys.exit()
else:
    accessToken, expireTime = result

result = CameraAPI.disableEncryption(accessToken, device, devcode)
liveurl = CameraAPI.GetLiveAddress(accessToken, device, devcode, 2)
if liveurl is False:
    print('Warning: Unable to get the live broadcast address.')
else:
    print(liveurl)

if bool(config['APScheduler']['enable']) == True:
    enableCameraTime = config['APScheduler']['enableCameraTime'].split(':')
    disableCameraTime = config['APScheduler']['disableCameraTime'].split(':')
    enableHour, enableMinute = enableCameraTime
    disableHour, disableMinute = disableCameraTime
    scheduler = BackgroundScheduler()
    scheduler.add_job(SchedulerAction.enableCamera, 'cron', hour=enableHour, minute=enableMinute)
    scheduler.add_job(SchedulerAction.disableCamera, 'cron', hour=disableHour, minute=disableMinute)
    print('Automatic camera masking has been added to the scheduled task.')
    print('Auto enable time: %s:%s, auto disable time: %s:%s.' % (enableHour, enableMinute, disableHour, disableMinute))

while True:
    break

result = CameraAPI.enableEncryption(accessToken, device)

# -*- coding: utf-8 -*-

import requests, json


class CameraAPI:
    def GetToken(appKey, appSecret):
        param = {'appKey': appKey, 'appSecret': appSecret}
        response = requests.post('https://open.ys7.com/api/lapp/token/get', params=param)
        resdata = response.json()
        if resdata['code'] != '200':
            return False
        else:
            data = resdata['data']
            accessToken = data['accessToken']
            expireTime = data['expireTime']
            return (accessToken, expireTime)

    def GetSwitchStatus(accessToken, deviceSerial):
        param = {'accessToken': accessToken, 'deviceSerial': deviceSerial}
        response = requests.post('https://open.ys7.com/api/lapp/device/scene/switch/status', params=param)
        resdata = response.json()
        if resdata['code'] != '200':
            return False
        else:
            data = resdata['data']
            status = data['enable']
            return status

    def GetLiveAddress(accessToken, deviceSerial, code=None, protocol=1):
        param = {'accessToken': accessToken, 'deviceSerial': deviceSerial, 'code': code, 'protocol': protocol}
        response = requests.post('https://open.ys7.com/api/lapp/v2/live/address/get', params=param)
        resdata = response.json()
        if resdata['code'] != '200':
            return False
        else:
            data = resdata['data']
            url = data['url']
            return url
        
    def SwitchScene(accessToken, deviceSerial, status, channelNo=1):
        param = {'accessToken': accessToken, 'deviceSerial': deviceSerial, 'enable': status, 'channelNo': channelNo}
        response = requests.post('https://open.ys7.com/api/lapp/device/scene/switch/set', params=param)
        resdata = response.json()
        if resdata['code'] != '200':
            return False
        else:
            return True

    def ptzControl(accessToken, deviceSerial, action, channelNo=1, speed=None, direction=None):
        if action == 'start' and (direction == None or speed == None):
            raise ValueError("The action %s cannot be without other parameters" % action)
        if action == 'start':
            param = {'accessToken': accessToken, 'deviceSerial': deviceSerial, 'speed': speed, 'direction': direction, 'channelNo': channelNo}
            response = requests.post('https://open.ys7.com/api/lapp/device/ptz/start', params=param)
            resdata = response.json()
            if resdata['code'] != '200':
                return False
            else:
                return True
        elif action == 'stop':
            param = {'accessToken': accessToken, 'deviceSerial': deviceSerial, 'direction': direction, 'channelNo': channelNo}
            response = requests.post('https://open.ys7.com/api/lapp/device/ptz/stop', params=param)
            resdata = response.json()
            if resdata['code'] != '200':
                return False
            else:
                return True
        else:
            raise ValueError('Invaild action')

    def enableEncryption(accessToken, deviceSerial):
        param = {'accessToken': accessToken, 'deviceSerial': deviceSerial}
        response = requests.post('https://open.ys7.com/api/lapp/device/encrypt/on', params=param)
        resdata = response.json()
        if resdata['code'] != '200':
            return False
        else:
            return True
        
    def disableEncryption(accessToken, deviceSerial, validateCode):
        param = {'accessToken': accessToken, 'deviceSerial': deviceSerial, 'validateCode': validateCode}
        response = requests.post('https://open.ys7.com/api/lapp/device/encrypt/off', params=param)
        resdata = response.json()
        if resdata['code'] != '200':
            return False
        else:
            return True


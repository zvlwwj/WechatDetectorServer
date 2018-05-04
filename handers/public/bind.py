import tornado.web

from handers.public import db
import json
import logging
class BindHandler(tornado.web.RequestHandler):
    # 1表示该用户名已存在
    # 0表示用户数据插入成功
    # -1表示用户数据插入失败
    def post(self):
        data = {}
        try:
            user_name = self.get_argument('user_name')
            device_name = self.get_argument('device_name')
            if db.select_user(user_name) is not None:
                data['code'] = 1
            else:
                deviceId = db.add_device(device_name)
                print("deviceId : "+str(deviceId))
                db.bind_user(user_name=user_name, deviceIds=str(deviceId))
                data['user_name'] = user_name
                data['deviceId'] = deviceId
                data['code'] = 0
        except BaseException as e:
            logging.exception(e)
            data['code'] = -1
        self.write(json.dumps(data))


class AddDeviceHandler(tornado.web.RequestHandler):
    def post(self):
        data = {}
        try:
            user_name = self.get_argument('user_name')
            device_name = self.get_argument('device_name')
            deviceId = db.add_device(device_name)
            old_deviceIds = db.select_user(user_name)[2]
            print("old_deviceIds : "+old_deviceIds)
            for id in old_deviceIds.split(","):
                oldDeviceName = db.select_deviceName(deviceId=id)[1]
                if oldDeviceName == device_name:
                    data['code'] = 1
                    self.write(json.dumps(data))
                    return
            data['code'] = 0
            data['user_name'] = user_name
            data['deviceId'] = deviceId
            new_deviceIds = old_deviceIds + "," + str(deviceId)
            db.update_user_device(user_name=user_name,deviceIds=new_deviceIds)

        except BaseException as e:
            logging.exception(e)
            data['code'] = -1
        self.write(json.dumps(data))

class GetDevices(tornado.web.RequestHandler):
    def post(self):
        data = {}
        try:
            user_name = self.get_argument('user_name')
            deviceIds = db.select_user(user_name=user_name)[2]
            deviceList = []
            for deviceId in deviceIds.split(","):
                deviceName = db.select_deviceName(deviceId)[1]
                device = {"deviceId": deviceId, "deviceName": deviceName}
                deviceList.append(device)
            data['code'] = 0
            data['deviceList'] = deviceList
        except BaseException as e:
            logging.exception(e)
            data['code'] = -1
        self.write(json.dumps(data))
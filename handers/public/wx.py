#!/usr/bin/env Python
# coding=utf-8
import hashlib
import time
from datetime import datetime

import tornado.web
import os
from handers.public import receive, reply, tool
from handers.public import db
import qrcode
import media
import basic
import json as json
import material
versionName = "1.0"
base_url = "http://172.16.4.32:80"
price = 5


class WxHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            print("wxHandler")
            signature =self.get_argument("signature")
            timestamp =self.get_argument("timestamp")
            nonce =self.get_argument("nonce")
            echostr = self.get_argument("echostr")
            token  = "zoujingyi2018"
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                self.write(echostr)
            else:
                self.write("")
        except Exception as e:
             self.write(e)

    def post(self):
        try:
            webData = self.request.body
            # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                if recMsg.Content == '#SCAPK':
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    content = "http://www.zoujingyi.cn/app-release.apk"

                    qrcodePath = "imgs/release_apk_qrcode.png"
                    img = qrcode.make(content)
                    img.save(qrcodePath)
                    myMedia = media.Media()
                    accessToken = basic.Basic().get_access_token()
                    path = "/home/zou/WechatDetector/" + qrcodePath
                    mediaType = "image"
                    back = myMedia.uplaod(accessToken, path, mediaType)
                    back_json = json.loads(back)
                    media_id = back_json["media_id"]
                    replyMsg = reply.ImageMsg(toUser, fromUser, media_id)
                    self.write(replyMsg.send())

                elif recMsg.Content == '#OPENID':
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    content = toUser

                    qrcodePath = "imgs/"+toUser+"_qrcode.png"
                    img = qrcode.make(content)
                    img.save(qrcodePath)

                    myMedia = media.Media()
                    accessToken = basic.Basic().get_access_token()
                    path = "/home/zou/WechatDetector/"+qrcodePath
                    mediaType = "image"
                    back = myMedia.uplaod(accessToken, path, mediaType)
                    back_json = json.loads(back)
                    media_id = back_json["media_id"]
                    replyMsg = reply.ImageMsg(toUser, fromUser, media_id)
                    self.write(replyMsg.send())
                elif recMsg.Content == '#DEVICE':
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    content = ""
                    deviceIds = db.select_user(toUser)[2]
                    if deviceIds is not None:
                        for id in deviceIds.split(","):
                            deviceName = db.select_deviceName(deviceId=id)[1]
                            content = content+deviceName+" "+id+"\n"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    self.write(replyMsg.send())
                elif tool.fullmatch(r"(\d{4}-\d{1,2}-\d{1,2}\|\d+)", recMsg.Content):
                    # 日期|deviceId
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    balance = int(db.select_user(user_name=toUser)[1])
                    if balance < price:
                        content = "余额不足，请充值，您的余额为"+str(balance)+"元"
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        self.write(replyMsg.send())
                    else:
                        handleDate(recMsg=recMsg, handler=self, balance=balance)
            else:
                print("暂且不处理")
                self.write("success")
        except Exception as e:
            print(e)



def handleDate(recMsg, handler, balance):
    toUser = recMsg.FromUserName
    fromUser = recMsg.ToUserName

    strDate = recMsg.Content.split("|")[0]
    deviceId = recMsg.Content.split("|")[1]
    dateExpect = datetime.strptime(strDate, '%Y-%m-%d')
    strNow = datetime.now().strftime('%Y-%m-%d')
    dateNow = datetime.strptime(strNow, '%Y-%m-%d')
    delta = dateNow - dateExpect
    if delta.days > 30 or delta.days < 0:
        content = "只能查询7天内的数据"
    else:
        # 查询该用户，设备下指定日期的图片
        pathDir = "imgs/"+recMsg.FromUserName+"_"+deviceId+"/"+strDate
        if os.path.isdir(pathDir):
            userName = recMsg.FromUserName
            date = strDate
            token = hashlib.md5(userName + deviceId + date + "12345678987654321").hexdigest()
            new_balance = balance - price
            db.update_balance(user_name=userName, balance=new_balance)
            content = "http://www.zoujingyi.cn/img?userName="+userName+"&device="+deviceId+"&date="+date+"&token="+token
        else:
            content = "当天数据不存在"
    replyMsg = reply.TextMsg(toUser, fromUser, content)
    handler.write(replyMsg.send())

def build_apk(recMsg,handler):
    toUser = recMsg.FromUserName
    fromUser = recMsg.ToUserName
    current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print("current_time:" + current_time)
    apk_name = "app_v" + versionName + "_" + current_time + "_" + toUser + ".apk"
    print("apk_name:" + apk_name)
    os.system('cd Android &&gradle clean assembleRelease -PUSER_NAME=' + toUser + ' -PAPK_NAME=' + apk_name)
    file_path = base_url + "/Android/apk/" + toUser + "/" + apk_name
    print("file_path:" + file_path)
    content = file_path
    replyMsg = reply.TextMsg(toUser, fromUser, content)
    handler.write(replyMsg.send())
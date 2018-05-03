#!/usr/bin/env Python
# coding=utf-8
import hashlib

import time
import tornado.web
import os

from gevent import thread

from handers.public import receive, reply
from url import base_url


versionName = "1.0"


class WxHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            print("wxHandler")
            signature =self.get_argument("signature")
            timestamp =self.get_argument("timestamp")
            nonce =self.get_argument("nonce")
            echostr = self.get_argument("echostr")
            token  = "zoujingyi1992"
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
                    self.write("")
                    thread.start_new_thread(build_apk, (recMsg, self))
            else:
                print("暂且不处理")
                self.write("success")
        except Exception as e:
            self.write(e)


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
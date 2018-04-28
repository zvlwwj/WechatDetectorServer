#!/usr/bin/env Python
# coding=utf-8
import hashlib
import tornado.web
import os

from handers.public import receive, reply


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
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "test"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                self.write(replyMsg.send())
                if recMsg.Content == '#SCAPK':
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    content = "生成APK中..."
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    self.write(replyMsg.send())
                    os.system('cd androidAppSource/WechatDetector')
                    os.system('gradle clean assembleRelease -PWECHAT_USER_NAME=' + toUser)

            else:
                print("暂且不处理")
                self.write("success")
        except Exception as e:
            self.write(e)

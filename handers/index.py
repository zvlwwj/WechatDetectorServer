#!/usr/bin/env Python
# coding=utf-8
import os
import tornado.web
import hashlib
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        userName = self.get_argument("userName")
        device = self.get_argument("device")
        date = self.get_argument("date")
        get_token = self.get_argument("token")
        token = hashlib.md5(userName + device + date + "12345678987654321").hexdigest()
        if get_token == token:
            pathDir = "statics/"+userName+"_"+device+"/"+date
            print("pathDir:"+pathDir)
            for root, dirs, files in os.walk(pathDir):
                for i in range(len(files)):
                    files[i] = "http://www.zoujingyi.cn/"+pathDir+"/"+files[i]
                self.render("index.html", imgList=files)
        else:
            print("token验证失败")

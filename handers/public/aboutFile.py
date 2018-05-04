#!/usr/bin/env Python
# coding=utf-8
import logging

import tornado.web
import json
import os
from astropy.io.fits import file

import url
class UploadFileHandler(tornado.web.RequestHandler):
    def post(self):
        data = {}
        try:
            wechat_user = self.get_argument("wechat_user")
            date = self.get_argument("date")
            device_id = self.get_argument("device_id")
            relative_url = "statics/"+wechat_user+"_"+device_id+"/"+date+"/"
            files = self.request.files
            file = files.get("file")
            for img in file:
                if not os.path.exists(relative_url):
                    os.makedirs(relative_url)
                with open(relative_url + img['filename'], 'wb') as f:
                    f.write(img['body'])
        except BaseException as e:
            data['code'] = -1
            data['msg'] = "upload file error"
            logging.exception(e)
        else:
            data['code'] = 0
            data['msg'] = "upload file success"
        self.write(json.dumps(data))

class DeleteFileHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = {}
            delete_url = self.get_argument("url")
            relative_url = delete_url.replace(url.base_url, ".")
            os.remove(relative_url)
        except BaseException as e:
            data['code'] = -1
            data['msg'] = "delete file error"
            logging.exception(e)
        else:
            data['code'] = 0
            data['msg'] = "delete file success"
        self.write(json.dumps(data))

class DownLoadFileHandler(tornado.web.RequestHandler):
    def get(self):
        # print('i download file handler : ', self.request.uri)
        filename = self.request.uri
        if filename.endswith(".png"):
            self.set_header("Content-type", "image/png")
        else:
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + filename)
        # 读取的模式需要根据实际情况进行修改
        with open("."+filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        # 记得有finish哦
        self.finish()

# # 获取图片
# class GetImage(tornado.web.RequestHandler):
#     @tornado.web.asynchronous
#     @tornado.gen.coroutine
#     def get(self):
#         # 获得请求的URL
#         url = self.request.uri
#         # 图片地址标识
#         image_path = url.split("/")[2]
#         # 图片名称
#         image_name = url.split("/")[3]
#         rs = FileService()
#         # data = rs.get_image(image_path,image_name,resp)
#         # 回掉函数，参数
#         data = yield tornado.gen.Task(self.get_image,image_path,image_name,resp,rs)
#         self.write(data)
#         # 设置读取的格式
#         self.set_header("Content-type", "image/png")
#         self.finish()

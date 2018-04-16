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
        try:
            data = {}
            wechat_user = self.get_argument("wechat_user")
            date = self.get_argument("date")
            relative_url = "statics/"+wechat_user+"/"+date+"/"
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
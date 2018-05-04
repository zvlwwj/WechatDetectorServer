#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""

import sys     #utf-8，兼容汉字
from importlib import reload
from handers.public.aboutFile import UploadFileHandler, DownLoadFileHandler
from handers.public.bind import BindHandler, GetDevices, AddDeviceHandler
from handers.public.wx import WxHandler

reload(sys)


# base_url ="http://35.229.220.81:80"
base_url ="http://172.16.4.32:80"
url = [
    # ============主页推荐===========
    (r'/statics/.*/.*/.*', DownLoadFileHandler),
    (r'/.*', DownLoadFileHandler),
    (r'/upload', UploadFileHandler),
    (r'/wx', WxHandler),
    (r'/bindUser', BindHandler),
    (r'/selectDevice', GetDevices),
    (r'/addDevice', AddDeviceHandler)
]
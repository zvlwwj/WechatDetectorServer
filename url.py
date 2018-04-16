#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""

import sys     #utf-8，兼容汉字
from importlib import reload

import tornado

from handers.public.aboutFile import UploadFileHandler

reload(sys)


# base_url ="http://35.229.220.81:8000"
base_url ="http://172.16.4.32:8000"
url = [
    # ============主页推荐===========
    (r'/upload', UploadFileHandler)
]
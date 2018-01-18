# coding=utf-8
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")#mysite替换为自己的项目名

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

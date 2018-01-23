#!/bin/bash

pid=`ps aux | grep 'w test_uwsgi' | grep -v grep | awk '{print $2}' | xargs kill -9`
uwsgi -d ../log/uwsgi.log -s 127.0.0.1:2600 -w test_uwsgi

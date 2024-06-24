#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os
rootpath="/"

while True:
    # 打印rootpath
    sys.stdout.write("{} # ".format(rootpath))
    sys.stdout.flush()
    # 读取用户输入
    cmd = sys.stdin.readline().strip()
    # 判断用户输入
    if cmd=="exit":break
    elif cmd=="cd ..":pass
    elif cmd=="cd .":pass
    elif cmd=="cd /":rootpath="/"
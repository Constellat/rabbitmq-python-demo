#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/10 15:30
# @Author: niujianyu
# @File  : MyMessage.py

class MyMessage:
    def __init__(self, func_name, class_name, module_path, kwargs):
        self.func_name = func_name
        self.class_name = class_name
        self.module_path = module_path
        self.kwargs = kwargs

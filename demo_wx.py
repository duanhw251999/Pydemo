#!/usr/bin/env python
# -*-coding:utf-8 -*-
from wxpy import *

bot = Bot(cache_path=True)
bot.file_helper.send("hello")
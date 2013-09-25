# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
from flask_script import Manager
from reddit.common.app import startup_app

manager = Manager(startup_app)


if __name__ == '__main__':
    manager.run()

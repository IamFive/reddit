# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-6-16
#
from reddit.common.app import startup_app
from reddit.common.tools.env import ResourceLoader
import os

__test__ = False


# os.environ.setdefault(ResourceLoader.ENV_VAR_NAME,
#                     '/var/www/vhosts/reddit/resources/prod')

application = startup_app()

# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
from flask.globals import request, g
from reddit.common.tools.utils import get_formdata
from reddit.common.web.renderer import RenderFormat


def setup_formdata_interceptor(app):

    def inject_formdata():
        g.formdata = get_formdata(request)

    app.before_request(inject_formdata)

def setup_render_as_interceptor(app):
    """
        depend on setup_formdata_interceptor
    """

    from string import upper

    def inject_resp_type():

        def set_rf(rf_choice, default):
            rformat = upper(get_formdata(request).get('rformat', default));
            g.rformat = rformat if (rformat in rf_choice) else default

        set_rf(RenderFormat.choices, RenderFormat.DEFAULT)

    app.before_request(inject_resp_type)


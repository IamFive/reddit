# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-9-20
#

from flask import Flask, render_template, request
from flask.globals import g
from flask.wrappers import Response
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from reddit.common import error_code
from reddit.common.exceptions import FriendlyException
from reddit.common.interceptors import setup_formdata_interceptor, \
    setup_render_as_interceptor
from reddit.common.tools.env import ResourceLoader
from reddit.common.tools.utils import mkdirs
from reddit.common.web.renderer import smart_render, JsonResp, RenderFormat, \
    ContentType
from reddit.constants import ROOT, STATIC_URL_PATH
import json
import os
from flask.helpers import send_file


app = None


def init_logger():

    log_format = app.config.get('LOG_FORMAT')
    if app.config.get('LOG_FORMAT'):
        app.debug_log_format = log_format;

    # setup root log format - global filter.
    app.logger.setLevel(app.config.get('LOGGER_ROOT_LEVEL'))
    log_file_folder = app.config.get('FILE_LOG_HANDLER_FODLER')
    mkdirs(log_file_folder, is_folder=True)

    filename = os.path.join(log_file_folder, app.import_name + '.log')
    file_handler = TimedRotatingFileHandler(filename=filename, when="midnight",
                                            backupCount=10)
    file_handler.suffix = "%Y%m%d"
    file_handler.setLevel(app.config.get('FILE_LOG_HANDLER_LEVEL'))
    file_handler.setFormatter(Formatter(log_format))
    app.logger.addHandler(file_handler)


def init_bp_modules():
    """add blueprint modules."""

    global app

    from reddit.views.reddites import bp_reddites
    app.register_blueprint(bp_reddites, url_prefix='/api/r')


    @app.route('/api/version', methods=['GET'])
    @smart_render()
    def version():
        from reddit import version
        return version()

    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    @app.route('/index.html', methods=['GET'])
    def index():
        ''' when deploy we should keep static and html file separated'''
        return send_file('templates/index.html')


def init_error_handler():


    def handler_ex(ex, status=400):

        status = ex.code if ex.code >= 400 and ex.code < 500 else 400

        if g.rformat == RenderFormat.HTML:
            return render_template('{}.html'.format(status), error=ex), status

        if isinstance(ex, FriendlyException) and len(ex.msg_list) == 1:
            message = ex.msg_list[0]
        else:
            message = ex.msg_list
        resp = json.dumps(JsonResp.make_failed_resp(ex.code, message))

        if g.rformat == RenderFormat.JSON:
            return Response(resp, mimetype=ContentType.JSON), status
        elif g.rformat == RenderFormat.JSONP:
            callback = request.args.get('callback', False)
            if callback:
                content = "{}({})".format(callback, resp)
                return Response(content, mimetype=ContentType.JSONP,
                                status=200)
            return Response(resp, mimetype=ContentType.JSON, status=200)


    @app.errorhandler(404)
    def page_not_found(error):
        ex = FriendlyException.fec(error_code.RESOURCE_NOT_EXIST)
        return handler_ex(ex, 404)

    @app.errorhandler(FriendlyException)
    def friendly_ex_handler(ex):
        app.logger.exception(ex)
        status = ex.code if ex.code >= 400 and ex.code < 500 else 400
        return handler_ex(ex, status=status)


    @app.errorhandler(Exception)
    def exception_handler(error, status=400):
        app.logger.exception(error)
        ex = FriendlyException(400, str(error))
        return handler_ex(ex, status)


def init_interceptors():
    setup_render_as_interceptor(app)
    setup_formdata_interceptor(app)


def setup_flask_initial_options():

    static_folder = ResourceLoader.get().configs.get('STATIC_FOLDER')
    template_folder = ResourceLoader.get().configs.get('TEMPLATE_FOLDER')
    if not static_folder:
        static_folder = os.path.join(ROOT, 'static')

    if not template_folder:
        template_folder = os.path.join(ROOT, 'templates')

    options = dict(static_url_path=STATIC_URL_PATH)
    options['static_folder'] = static_folder
    options['template_folder'] = template_folder
    return options



def startup_app():

    global app

    if not app:
        args = setup_flask_initial_options()
        app = Flask('reddit', **args)

        app.config.update(ResourceLoader.get().configs)
        app.debug = app.config.get('DEBUG', True)

        init_logger()

        try:
            init_error_handler()
            init_interceptors()
            init_bp_modules()
            app.logger.info('Start success from ROOT [%s] .', ROOT)
        except Exception, e:
                app.logger.error('Start reddit faild!')
                app.logger.exception(e)
                raise e
    return app

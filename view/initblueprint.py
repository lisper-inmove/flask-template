# -*- coding: utf-8 -*-e

import traceback
from flask import request

from submodules.utils.logger import Logger
from submodules.utils.misc import Misc
from submodules.utils.idate import IDate
from view.unify_response import UnifyResponse
from view.errors import Error
from view.view_port import _view_port

logger = Logger()


class RequestMiddleWare:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        environ["HTTP_MESSAGE_UUID"] = Misc.uuid()
        environ["HTTP_REQUEST_TIME_MSEC"] = IDate.now_millseconds()
        return self.wsgi_app(environ, start_response)


class InitBlueprint:

    @property
    def app(self):
        return self.__app

    def __init__(self, app):
        self.__app = app
        self.__set_filter()
        self.app.register_blueprint(_view_port)
        self.app.wsgi_app = RequestMiddleWare(self.app.wsgi_app)

    def __set_filter(self):

        @self.app.errorhandler(404)
        def error_404(e):
            return UnifyResponse.R(rs=UnifyResponse.PAGE_NOT_FOUND)

        @self.app.errorhandler(Exception)
        def error_handler(e):
            logger.info(e)
            logger.info(traceback.print_tb(e.__traceback__))
            if isinstance(e, Error) or issubclass(e.__class__, Error):
                return UnifyResponse.R(rs=(e.code, e.msg))
            return UnifyResponse.R(rs=UnifyResponse.SYSTEM_ERROR)

        @self.app.before_request
        def app_before_request():
            pass

        @self.app.after_request
        def response_json(response):
            """记录请求参数和返回的errcode和errmsg."""
            user_ip = request.headers.get("X-Real-Ip", None)
            user_id = request.headers.get("userId")
            start_time_msec = float(request.headers.get("Request-Time-Msec"))
            end_time_msec = IDate.now_millseconds()
            url = request.url
            url_rule = request.url_rule
            msg = f"接口使用详情|||{user_ip}|||{user_id}|||{url}|||{url_rule}|||{end_time_msec - start_time_msec}"
            logger.info(msg)
            return response

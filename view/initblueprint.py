# -*- coding: utf-8 -*-e

import os
import importlib.util

from flask import Blueprint
from flask import request

from submodules.utils.logger import Logger
from submodules.utils.misc import Misc
from submodules.utils.idate import IDate
from view.unify_response import UnifyResponse
from view.errors import Error

logger = Logger()


class RequestMiddleWare:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        environ["HTTP_MESSAGE_UUID"] = Misc.uuid()
        environ["HTTP_REQUEST_TIMESTAMP"] = IDate.now_millseconds()
        return self.wsgi_app(environ, start_response)


class InitBlueprint:

    @property
    def app(self):
        return self.__app

    def __init__(self, app):
        self.__app = app
        self.__set_middleware()
        self.__views = list()
        self.__init_project()
        self.__auto_load_views()
        self.__set_filter()

    def __set_middleware(self):
        self.app.wsgi_app = RequestMiddleWare(self.app.wsgi_app)

    def __init_project(self):
        self.root_dir = os.path.abspath(os.path.curdir)

    def __auto_load_views(self):
        self.__load_view_from_directory(self.root_dir, "view")

    def __load_view_from_directory(self, root, directory):
        path = os.path.join(root, directory)
        for curroot, dirs, files in os.walk(path):
            for directory in dirs:
                self.__load_view_from_directory(root, directory)
            for file in files:
                filepath = os.path.join(curroot, file)
                self.__load_view_from_file(filepath)

    def __load_view_from_file(self, filename):
        if not filename.endswith("py"):
            return
        spec = importlib.util.spec_from_file_location("test", filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attribute in module.__dict__.keys():
            if attribute.startswith("__"):
                continue
            view = module.__dict__.get(attribute)
            if view is Blueprint:
                continue
            if not isinstance(view, Blueprint):
                continue
            logger.info(f"load view: {view} {filename}")
            self.app.register_blueprint(view)

    def __set_filter(self):

        @self.app.errorhandler(404)
        def error_404(e):
            return UnifyResponse.R(rs=UnifyResponse.PAGE_NOT_FOUND)

        @self.app.errorhandler(Exception)
        def error_handler(e):
            logger.error(e)
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
            start_time = float(request.headers.get("Request-Timestamp"))
            finish_time = IDate.now_millseconds()
            url = request.url
            url_rule = request.url_rule
            msg = f"接口使用详情|||{user_ip}|||{user_id}|||{url}|||{url_rule}|||{finish_time - start_time}"
            logger.info(msg)
            return response

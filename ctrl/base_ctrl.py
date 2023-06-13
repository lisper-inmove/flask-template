# -*- coding: utf-8 -*-

from flask import request

import api.common_api_pb2 as common_api_pb
from base_cls import BaseCls
from submodules.utils.protobuf_helper import ProtobufHelper
from submodules.utils.logger import Logger
from view.errors import PopupError

logger = Logger()


class BaseCtrl(BaseCls):

    POST = "POST"
    GET = "GET"
    HEAD = "HEAD"
    DELETE = "DELETE"
    PUT = "PUT"

    @property
    def operate(self):
        method = request.method
        if method == self.POST:
            return self._operate
        if method == self.GET:
            return f"{self._operate}_GET"
        if method == self.DELETE:
            return f"{self._operate}_DELETE"
        if method == self.PUT:
            return f"{self._operate}_PUT"
        if method == self.HEAD:
            return f"{self._operate}_HEAD"
        raise PopupError("Method Not Supported")

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.PH = ProtobufHelper
        self._operate = kargs.get('operate', None)
        self.request = request
        self._manager = None
        self._init(*args, **kargs)

    def _init(self, *args, **kargs):
        """子类要有自己的初始化工作就重载此函数."""
        pass

    def get_request_obj(self, cls):
        if request.method == self.POST:
            logger.info(f"请求参数: {request.get_json()}")
            return self.PH.to_obj(request.get_json(), cls)
        if request.method == self.GET:
            return self.PH.to_obj(request.args, cls)
        return None

    def get_header_param(self, key, default=None):
        # logger.info(f"请求头: {request.headers}")
        return request.headers.get(key, default)

    def do_operate(self):
        if self.operate is None:
            raise PopupError(f"操作未实现: {self.operate}")
        if self.operate.startswith("_"):
            raise PopupError(f"操作未实现: {self.operate}")
        cls = self.__class__
        if self.operate not in cls.__dict__:
            raise PopupError(f"操作未实现: {self.operate}")
        return cls.__dict__[self.operate](self)

    def empty_data_response(self):
        return common_api_pb.EmptyResponse()

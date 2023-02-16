# -*- coding: utf-8 -*-

import inspect
from concurrent import futures

import grpc

import gproto.api_pb2_grpc as api_pb_grpc
from base_cls import BaseCls
from submodules.utils.logger import Logger
from view.view_helper import ViewHelper

logger = Logger()


class ApiMeta(type):

    def __new__(cls, name, bases, attrs):
        view_helper = ViewHelper("ctrl/gctrl")
        view_helper.load_ctrl()
        for func in inspect.getmembers(api_pb_grpc.APIServicer, predicate=inspect.isfunction):
            ctrl_name = func[0].split("__")[0]
            func_name = func[0].split("__")[-1]
            ctrl = view_helper.ctrls.get(ctrl_name)
            if not ctrl:
                attrs.update({func[0]: cls.method_not_implemented})
            else:
                attrs.update({func[0]: cls.api_creator(func_name, ctrl)})
        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def api_creator(cls, name, ctrl):
        def func(self, req, ctx):
            obj = ctrl(req, ctx)
            logger.info(f"{name} 被调用: {req}")
            if not hasattr(obj, name):
                raise NotImplementedError("Method not implemented!")
            return getattr(obj, name)()
        return func

    @classmethod
    def method_not_implemented(cls, req, ctx):
        raise NotImplementedError("Method not implemented!")


class Api(BaseCls,  api_pb_grpc.APIServicer, metaclass=ApiMeta):

    def run(self, host, port, max_workers=10):
        logger.info(f">>>>> {self.app_name} grpc 服务已启动: {host} {port} {max_workers} <<<<<")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        api_pb_grpc.add_APIServicer_to_server(self, server)
        server.add_insecure_port(f"{host}{port}")
        server.start()
        server.wait_for_termination()

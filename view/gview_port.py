# -*- coding: utf-8 -*-

from concurrent import futures

import grpc

import gproto.api_pb2_grpc as api_pb_grpc
from submodules.utils.logger import Logger
from view.view_helper import ViewHelper

logger = Logger()


class Api:

    source_ctrls = dict()

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.view_helper = ViewHelper("ctrl/gctrl")
        self.view_helper.load_ctrl()

    def __getattr__(self, key):
        """获取属性."""
        key_split = key.split("__")
        if key_split[0] not in self.view_helper.ctrls:
            return super().__getattr__(key)
        source = key_split[0].replace("_", "-")
        api_name = "_".join(key_split[1:])
        ctrl_obj = self.source_ctrls.get(source)
        if ctrl_obj:
            if hasattr(ctrl_obj, api_name):
                return getattr(ctrl_obj, api_name)
            return self.not_implemented(api_name)
        ctrl_cls = self.view_helper.ctrls[source]
        if not hasattr(ctrl_cls, api_name):
            return self.not_implemented(api_name)
        cls_obj = ctrl_cls()
        self.source_ctrls.update({source: cls_obj})
        return getattr(cls_obj, api_name)

    def not_implemented(self, api_name):
        def m(req, ctx):
            raise NotImplementedError(f"{api_name} Not Implemented!")
        return m

    def run(self, host, port, max_workers=10):
        logger.info(f">>>>> grpc 服务已启动: {host} {port} {max_workers} <<<<<")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        api_pb_grpc.add_APIServicer_to_server(self, server)
        server.add_insecure_port(f"{host}{port}")
        server.start()
        server.wait_for_termination()

import api.demo_api_pb2 as api_pb

from ctrl.base_ctrl import BaseCtrl
from manager.demo.demo import DemoManager
from submodules.utils.logger import Logger

logger = Logger()


class DemoCtrl(BaseCtrl):

    @property
    def manager(self):
        if not self._manager:
            self._manager = DemoManager()
        return self._manager

    def create(self):
        req = self.get_request_obj(api_pb.CreateDemoReq)
        logger.info(f"Request Demo create: {req}")
        obj = self.manager.create_demo(req)
        logger.info(f"Create demo: {obj}")
        return self.empty_data_response()

    def test(self):
        return "Post Test"

    def test_GET(self):
        return "Get Test"

    def test_HEAD(self):
        return "Head Success"

    def update(self):
        req = self.get_request_obj(api_pb.UpdateDemoReq)
        obj = self.manager.update_demo(req)
        resp = api_pb.UpdateDemoResp()
        resp.name = obj.name
        return resp

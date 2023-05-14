import proto.demo.demo_pb2 as demo_pb
from manager.base_manager import BaseManager


class DemoManager(BaseManager):

    def create_demo(self, req):
        demo = self.create_obj(demo_pb.Demo)
        demo.name = req.name
        return demo

    def update_demo(self, req):
        demo = self.get_demo_by_id(req.id)
        demo.name = req.name
        return demo

    def get_demo_by_id(self, id):
        # TODO: Get demo from db
        demo = self.create_obj(demo_pb.Demo)
        return demo

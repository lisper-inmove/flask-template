import api.resource_api_pb2 as resource_api_pb
import proto.user.resource_pb2 as resource_pb
from manager.user.resource import ResourceManager


class ResourceHelper:

    @classmethod
    def help(cls):
        pass

    @classmethod
    def add_one(cls, name, namespace):
        manager = ResourceManager()
        req = resource_api_pb.CreateResourceRequest()
        req.name = name
        req.namespace = namespace
        resource = manager.create_resource(req)
        manager.add_or_update_resource(resource)

    @classmethod
    def list_resources(cls, self):
        manager = ResourceManager()
        r = resource_pb.Resource()
        r.namespace = input("请输入名称空间: ")
        resources = manager.list_resources(r)
        for result in resources:
            print(f"{result.name}")

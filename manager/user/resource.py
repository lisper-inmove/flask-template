import proto.user.resource_pb2 as resource_pb
from manager.base_manager import BaseManager
from dao.user.resource import ResourceDA


class ResourceManager(BaseManager):

    @property
    def resource_da(self):
        if self._resource_da is None:
            self._resource_da = ResourceDA()
        return self._resource_da

    def create_resource(self, req):
        resource = self.create_obj(resource_pb.Resource)
        resource.name = req.name
        resource.namespace = req.namespace
        return resource

    def add_or_update_resource(self, resource):
        self.resource_da.add_or_update_resource(resource)

    def get_resource(self, resource):
        if resource.id != "":
            return self.resource_da.get_resource_by_id(resource.id)
        if resource.name != "" and resource.namespace != "":
            return self.resource_da.get_resource_by_name(
                resource.namespace, resource.name)
        return None

    def list_resources(self, resource):
        return self.resource_da.list_resources(resource.namespace)

    def delete_resource(self, resource):
        return self.resource_da.delete_resource(resource.id)

import proto.user.resource_pb2 as resource_pb
from dao.mongodb import MongoDBHelper


class ResourceDA(MongoDBHelper):

    def add_or_update_resource(self, resource):
        matcher = {"id": resource.id}
        self.update_one(matcher, self.PH.to_json(resource))

    def get_resource_by_id(self, id):
        matcher = {"id": id}
        return self.find_one(matcher, resource_pb.Resource)

    def get_resource_by_name(self, namespace, name):
        matcher = {"namespace": namespace, "name": name}
        return self.find_one(matcher, resource_pb.Resource)

    def list_resources(self, namespace):
        matcher = {"namespace": namespace}
        return self.find_many(matcher)

    def delete_resource(self, id):
        matcher = {"id": id}
        self.delete_one(matcher)

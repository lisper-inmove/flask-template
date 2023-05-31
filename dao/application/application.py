import proto.application.application_pb2 as application_pb
from dao.mongodb import MongoDBHelper


class ApplicationDB(MongoDBHelper):

    coll = "___application_db___applications___"

    def add_or_update_application(self, application):
        matcher = {"id": application.id}
        json_data = self.PH.to_json(application)
        self.update_one(matcher, json_data, upsert=True)

    def get_application_by_id(self, id):
        matcher = {"id": id}
        return self.find_one(matcher, application_pb.Application)

    def get_application_by_name(self, name):
        matcher = {"name": name}
        return self.find_one(matcher, application_pb.Application)

    def list_applications_with_create_time_order(self, last_create_time):
        matcher = {"create_time_sec": {"$lt": str(last_create_time)}}
        applications = self.find_many(matcher)
        return self.PH.batch_to_obj(applications, application_pb.Application)

    def delete_application(self, id):
        matcher = {"id": id}
        self.delete_one(matcher)

import proto.user.user_pb2 as user_pb
from dao.mongodb import MongoDBHelper
from submodules.utils.protobuf_helper import ProtobufHelper


class UserDA(MongoDBHelper):

    coll = "___user_db___users___"

    def add_or_update_user(
        self,
        user: user_pb.User
    ):
        matcher = {"id": user.id}
        json_data = ProtobufHelper.to_json(user)
        self.update_one(matcher, json_data, upsert=True)

    def list_user(self, last_create_time):
        matcher = {"create_time_sec": {"$lt": str(last_create_time)}}
        users = self.find_many(matcher, sortby=[("create_time_sec", -1)])
        return self.PH.batch_to_obj(users, user_pb.User)

    def list_user_by_username(self, last_create_time, username):
        matcher = {
            "username": {
                "$regex": f".*{username}.*"
            }
        }
        users = self.find_many(matcher, sortby=[("create_time_sec", -1)])
        return self.PH.batch_to_obj(users, user_pb.User)

    def get_user_by_id(self, id):
        matcher = {"id": id}
        return self.find_one(matcher, user_pb.User)

    def login_by_phone(self, phone, password):
        matcher = {"phone": phone, 'password': password}
        return self.find_one(matcher, user_pb.User)

    def login_by_username(self, username, password):
        matcher = {"username": username, 'password': password}
        return self.find_one(matcher, user_pb.User)

    def login_by_email(self, email, password):
        matcher = {"email": email, 'password': password}
        return self.find_one(matcher, user_pb.User)

    def check_phone_exists(self, phone):
        return self.find_one({'phone': phone}, user_pb.User)

    def check_email_exists(self, email):
        return self.find_one({'email': email}, user_pb.User)

import proto.user.membership_pb2 as membership_pb
from dao.mongodb import MongoDBHelper


class MembershipDA(MongoDBHelper):

    coll = "___user_db___memberships___"

    def add_or_update_membership(self, membership):
        matcher = {"user_id": membership.user_id}
        json_data = self.PH.to_json(membership)
        self.update_one(matcher, json_data, upsert=True)

    def get_membership_by_user_id(self, user_id):
        matcher = {"user_id": user_id}
        return self.find_one(matcher, membership_pb.Membership)

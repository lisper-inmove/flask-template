import api.user_api_pb2 as api_pb
from ctrl.base_ctrl import BaseCtrl
from manager.user.user import UserManager
from submodules.utils.jwt_util import JWTUtil


class UserCtrl(BaseCtrl):

    def sign_up(self):
        req = self.get_request_obj(api_pb.SignUpRequest)
        manager = UserManager()
        user = manager.create_user(req)
        manager.add_or_update_user(user)
        resp = api_pb.CommonUserResponse()
        resp.username = user.username
        resp.token = JWTUtil().generate_token(
            payload={"username": user.username, "id": user.id})
        return resp

    def login(self):
        req = self.get_request_obj(api_pb.LoginRequest)
        manager = UserManager()
        user = manager.login(req)
        resp = api_pb.CommonUserResponse()
        resp.username = user.username
        resp.token = JWTUtil().generate_token(
            payload={"username": user.username, "id": user.id})
        return resp

import api.user_api_pb2 as api_pb
from ctrl.base_ctrl import BaseCtrl
from manager.user.user import UserManager
from manager.user.recharge_record import RechargeRecordManager
from manager.trade.transaction import TransactionManager
from submodules.utils.jwt_util import JWTUtil
from submodules.utils.idate import IDate
from view.errors import PopupError


class UserCtrl(BaseCtrl):

    def sign_up(self):
        req = self.get_request_obj(api_pb.SignUpRequest)
        manager = UserManager()
        if manager.check_email_exists(req) or \
           manager.check_phone_exists(req):
            raise PopupError("手机号或邮箱已存在")
        user = manager.create_user(req)
        manager.add_or_update_user(user)
        resp = api_pb.CommonUserResponse()
        resp.username = user.username
        resp.token_expire_at = IDate.now_timestamp() + JWTUtil.TOKEN_VALID_TIME_PERIOD
        resp.token = JWTUtil().generate_token(
            payload={"username": user.username, "id": user.id})
        resp.is_plus_user = self.__is_plus_user(user)
        return resp

    def login(self):
        req = self.get_request_obj(api_pb.LoginRequest)
        manager = UserManager()
        if not manager.check_email_exists(req) and \
           not manager.check_phone_exists(req):
            return self.sign_up()
        user = manager.login(req)
        resp = api_pb.CommonUserResponse()
        resp.username = user.username
        resp.token_expire_at = IDate.now_timestamp() + JWTUtil.TOKEN_VALID_TIME_PERIOD
        resp.token = JWTUtil().generate_token(
            payload={"username": user.username, "id": user.id})
        resp.is_plus_user = self.__is_plus_user(user)
        return resp

    def __is_plus_user(self, user):
        """检查是否是高级用户."""
        recharge_record_manager = RechargeRecordManager()
        if not user:
            return False
        record = recharge_record_manager.get_user_latest_paid_recharge_record(user)
        if not record:
            return False
        if IDate.now_timestamp() > record.valid_at:
            return False
        return True

    def check_token(self):
        req = self.get_request_obj(api_pb.CheckTokenRequest)
        if self.get_header_param("token") is None:
            raise PopupError("Token Not Exists")
        req.token = self.get_header_param("token")
        JWTUtil().decode(req.token)
        return self.empty_data_response()

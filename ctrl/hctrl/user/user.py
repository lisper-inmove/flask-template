import api.user_api_pb2 as api_pb
from ctrl.base_ctrl import BaseCtrl
from manager.user.user import UserManager
from manager.user.recharge_record import RechargeRecordManager
from manager.user.membership import MembershipManager
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
        self.__is_vip(user, resp)
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
        self.__is_vip(user, resp)
        return resp

    def __is_vip(self, user, resp):
        """检查是否是高级用户."""
        recharge_record_manager = RechargeRecordManager()
        if not user:
            return
        membership_manager = MembershipManager()
        membership = membership_manager.get_or_create_membership_by_user(user)
        record = recharge_record_manager.get_user_latest_paid_recharge_record(user)
        self.__is_vip_by_record(resp, record)
        self.__is_vip_by_membership(resp, membership)
        self.__is_vip_by_farther(resp, record, membership)

    def __is_vip_by_farther(self, resp, record, membership):
        """比对谁的时间更长,就使用谁"""
        if not record or not membership:
            return
        if membership.vip_expire_at > record.update_time_sec:
            self.__is_vip_by_membership(resp, membership)
        else:
            self.__is_vip_by_record(resp, record)

    def __is_vip_by_record(self, resp, record):
        """只根据用户购买逻辑设置"""
        if not record:
            return
        resp.vip_expire_at = record.valid_at
        if IDate.now_timestamp() > record.valid_at:
            resp.is_vip = False
        else:
            resp.is_vip = True

    def __is_vip_by_membership(self, resp, membership):
        """根据管理员在后台修改设置"""
        if not membership:
            return
        resp.is_disabled = membership.is_disabled
        if membership.is_disabled:
            resp.is_vip = False
        else:
            resp.is_vip = True
        if membership.vip_expire_at == 0:
            resp.is_vip = False
        else:
            resp.vip_expire_at = membership.vip_expire_at

    def check_token(self):
        req = self.get_request_obj(api_pb.CheckTokenRequest)
        if self.get_header_param("token") is None:
            raise PopupError("Token Not Exists")
        req.token = self.get_header_param("token")
        info = JWTUtil().decode(req.token)
        manager = UserManager()
        user = manager.get_user_by_id(info.get("id"))
        resp = api_pb.CommonUserResponse()
        resp.username = user.username
        resp.token = req.token
        resp.token_expire_at = info.get("expire_at")
        self.__is_vip(user, resp)
        return resp

    def list(self):
        req = self.get_request_obj(api_pb.ListUserRequest)
        manager = UserManager()
        users = manager.list_user(req)
        resp = self.__convert_user_to_UserInfoResponses(users)
        resp.count = manager.count_user()
        return resp

    def disable_or_enable_vip(self):
        """禁用某一个用户的vip时间"""
        req = self.get_request_obj(api_pb.DisableOrEnableVipRequest)
        manager = UserManager()
        user = manager.get_user_by_id(req.user_id)
        membership_manager = MembershipManager()
        membership = membership_manager.get_or_create_membership_by_user(user)
        membership_manager.disable_or_enable_vip(
            membership, req.disable)
        membership_manager.add_or_update_membership(membership)
        return self.empty_data_response()

    def extend_vip_expire_time(self):
        """延长某一个用户的vip时限"""
        req = self.get_request_obj(api_pb.ExtendVipExpireTimeRequest)
        manager = UserManager()
        user = manager.get_user_by_id(req.user_id)
        membership_manager = MembershipManager()
        membership = membership_manager.get_or_create_membership_by_user(user)
        membership_manager.extend_vip_expire_time(membership, req.vip_expire_at)
        membership_manager.add_or_update_membership(membership)
        return self.empty_data_response()

    def __convert_user_to_CommonUserResponse(self, user):
        resp = api_pb.CommonUserResponse()
        resp.username = user.username
        self.__is_vip(user, resp)
        return resp

    def __convert_user_to_UserInfoResponse(self, user):
        resp = api_pb.UserInfoResponse()
        resp.id = user.id
        resp.username = user.username
        resp.phone = user.phone
        resp.email = user.email
        resp.create_time = user.create_time_sec
        self.__is_vip(user, resp)
        return resp

    def __convert_user_to_UserInfoResponses(self, users):
        resp = api_pb.ListUserResponse()
        for user in users:
            resp.users.add().CopyFrom(self.__convert_user_to_UserInfoResponse(user))
        return resp

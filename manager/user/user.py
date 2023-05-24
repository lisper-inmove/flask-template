import proto.user.user_pb2 as user_pb
from manager.base_manager import BaseManager
from dao.user.user import UserDA
from view.errors import PopupError


class UserManager(BaseManager):

    @property
    def user_da(self):
        if not self._user_da:
            self._user_da = UserDA()
        return self._user_da

    def _init(self):
        self._user_da = None

    def create_user(self, req):
        user = self.create_obj(user_pb.User)
        user.username = req.username
        user.phone = req.phone
        user.password = req.password
        return user

    def login(self, req):
        user = self.user_da.login_by_phone(req.phone, req.password)
        if not user:
            user = self.user_da.login_by_username(req.username, req.password)
        if not user:
            raise PopupError("账号不存在或密码错误")
        return user

    def add_or_update_user(self, user):
        if not user:
            return None
        self.user_da.add_or_update_user(user)
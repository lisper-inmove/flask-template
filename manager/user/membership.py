import proto.user.membership_pb2 as membership_pb
from manager.base_manager import BaseManager
from dao.user.membership import MembershipDA
from submodules.utils.idate import IDate


class MembershipManager(BaseManager):

    @property
    def membership_da(self):
        if self._membership_da is None:
            self._membership_da = MembershipDA()
        return self._membership_da

    def _init(self, *args, **kargs):
        self._membership_da = None

    def create_membership(self, user):
        obj = self.create_obj(membership_pb.Membership)
        obj.user_id = user.id
        obj.vip_expire_at = IDate.now_timestamp()
        return obj

    def get_or_create_membership_by_user(self, user):
        membership = self.membership_da.get_membership_by_user_id(user.id)
        if not membership:
            membership = self.create_membership(user)
        return membership

    def disable_or_enable_vip(self, membership, disabled):
        membership.is_disabled = disabled

    def set_vip_expire_time(self, membership, expire_at):
        membership.vip_expire_at = expire_at

    def extend_vip_expire_time(self, membership, extend_time):
        membership.vip_expire_at += extend_time

    def add_or_update_membership(self, membership):
        if not membership:
            return
        super().update_obj(membership)
        self.membership_da.add_or_update_membership(membership)

import api.trade_api_pb2 as trade_api_pb
import proto.trade.transaction_pb2 as transaction_pb
import proto.user.membership_pb2 as membership_pb
from ctrl.base_ctrl import BaseCtrl
from manager.trade.transaction import TransactionManager
from manager.user.recharge_record import RechargeRecordManager
from manager.user.recharge_config import RechargeConfigManager
from submodules.payment.proxy import PaymentProxy
from submodules.utils.jwt_util import JWTUtil
from view.errors import PopupError


class TransactionCtrl(BaseCtrl):

    @property
    def transaction_manager(self):
        if self._transaction_manager is None:
            self._transaction_manager = TransactionManager()
        return self._transaction_manager

    def _init(self, *args, **kargs):
        self._transaction_manager = None

    def prepay(self):
        # TODO: 从token中取出用户ID,存入transaction中
        # TODO: 在业务逻辑中将token去除，在网关中处理token
        # TODO: 在Api网关中用token取出userId放到header中
        req = self.get_request_obj(trade_api_pb.PrepayRequest)
        token = self.get_header_param("token")
        decoded_data = JWTUtil().decode(token)
        transaction = self.transaction_manager.create_transaction(req)
        transaction.payer_id = decoded_data.get("id")
        self.__create_order(transaction, req)
        result = self.__prepay(transaction)
        self.transaction_manager.add_or_update_transaction(transaction)
        resp = trade_api_pb.PrepayResponse()
        resp.transaction_id = transaction.id
        resp.qrcode_url = result.qrcode_url
        resp.pay_method = transaction_pb.Transaction.PayMethod.Name(
            transaction.pay_method)
        return resp

    def __create_order(self, transaction, req):
        if transaction.type == transaction_pb.Transaction.CHATBOT_PLUS:
            self.__create_recharge_record(transaction, req)

    def __create_recharge_record(self, transaction, req):
        if transaction.type != transaction_pb.Transaction.CHATBOT_PLUS:
            return
        recharge_config_manager = RechargeConfigManager()
        recharge_config = recharge_config_manager.get_recharge_config_by_id(
            req.commodity_id)
        if not recharge_config:
            raise PopupError(f"{req.commodity_id}商品不存在")
        recharge_record_manager = RechargeRecordManager()
        recharge_record = recharge_record_manager.create_obj(
            membership_pb.RechargeRecord)
        recharge_record.config.CopyFrom(recharge_config)
        transaction.order_id = recharge_record.id
        transaction.pay_fee = recharge_config.price
        recharge_record_manager.add_or_update_recharge_record(recharge_record)

    def notify(self):
        # 暂不用回调
        pass

    def query(self, req=None):
        if req is None:
            req = self.get_request_obj(trade_api_pb.QueryRequest)
        transaction = self.transaction_manager.get_transaction(req)
        result = self.__query(transaction)
        resp = trade_api_pb.QueryResponse()
        resp.transaction_id = transaction.id
        resp.success = result.success
        resp.msg = result.msg
        resp.sub_msg = result.sub_msg
        return resp

    def __prepay(self, transaction):
        obj = PaymentProxy()
        if transaction.pay_method == transaction_pb.Transaction.ALIPAY_F2F:
            result = obj.alipay_f2f_prepay(transaction.id, transaction.pay_fee)
        return result

    def __query(self, transaction):
        obj = PaymentProxy()
        if transaction.pay_method == transaction_pb.Transaction.ALIPAY_F2F:
            result = obj.query_alipay_trade(transaction.id)
            if not result.success:
                return result
            transaction.third_party_id = result.third_party_id
            self.transaction_manager.add_or_update_transaction(transaction)
        return result

from manager.trade.transaction import TransactionManager
from submodules.payment.proxy import PaymentProxy
from submodules.utils.idate import IDate


class TradeChecker:

    def query(self):
        manager = TransactionManager()
        end_timestamp = IDate.now_timestamp()
        start_timestamp = end_timestamp - IDate.ONE_MIN


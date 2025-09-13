from typing import Optional

class TradingAccountBTO:
    def __init__(self,
                 id: Optional[int],
                 user_id,

                 broker_name,
                 account_id,
                 server,
                 password,

                 balance: Optional[float] = None,
                 equity: Optional[float] = None
                 ):

        self.id = id
        self.user_id = user_id

        self.broker_name = broker_name
        self.account_id = account_id
        self.server = server
        self.password = password

        self.balance = balance
        self.equity = equity

class Entity:
    def __init__(self,entity_id: int):
        self.id:int = entity_id


class Client(Entity):
    def __init__(self,client_id: int, name:str):
        super().__init__(client_id)
        self.name:str = name
        self.accounts: dict[str, Account] = {}

        def __str__(self):
            account_info = "\n".join(str(acc) for acc in self.accounts.values())
            return f"Client ID: {self.id} | Name: {self.name}\nAccounts:\n{account_info if account_info else 'No accounts'}"

class Account(Entity):
    def __init__(self, acc_id:int, owner_id:int, currency:str, balance: float = 0.0):
        super().__init__(acc_id)
        self.owner_id:int = owner_id
        self.currency:str = currency
        self.balance:float = balance

        def __str__(self):
            return f"Account {self.id} | {self.currency} | Balance: {self.balance}"


class Bank:
    def __init__(self):
        self.clients:dict[int, Client] = {}
        self.accounts:dict[int, Account] = {}
        self.next_client_id:int = 1
        self.next_account_id:int = 1
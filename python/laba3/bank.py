class Entity:
    def __init__(self,entity_id: int):
        self.id:int = entity_id



class Client(Entity):
    def __init__(self,client_id: int, name:str):
        super().__init__(client_id)
        self.name:str = name
        self.accounts: dict[str, Account] = {}

class Account(Entity):
    def __init__(self, acc_id:int, owner_id:int, currency:str, balance: float = 0.0):
        super().__init__(acc_id)
        self.owner_id:int = owner_id
        self.currency:str = currency
        self.balance:float = balance


class Bank:
    def __init__(self):
        self.clients:dict[str, Client] = {}
        self.accounts:dict[str, Account] = {}
        self.next_client_id:int = 1
        self.next_account_id:int = 1
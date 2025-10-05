import json
import os


class BankError(Exception):
    pass

class ClientNotFound(BankError):
    def __init__(self, client_id):
        super().__init__(f"Client with ID {client_id} not found")

class AccountExistsError(BankError):
    def __init__(self, currency):
        super().__init__(f"The client already has an account in the {currency} currency")

class InsufficientFundsError(BankError):
    def __init__(self, balance, amount):
        super().__init__(f"Insufficient funds: balance {balance}, attempt to withdraw {amount}")

class AccountNotFoundError(BankError):
    def __init__(self, currency):
        super().__init__(f"The account in the {currency} currency was not found")


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

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        print(f"Withdrawn {amount}. New balance: {self.balance}")


class Bank:
    def __init__(self):
        self.clients:dict[int, Client] = {}
        self.accounts:dict[int, Account] = {}
        self.next_client_id:int = 1
        self.next_account_id:int = 1

    def open_account(self, client_id:int, currency:str, initial_balance:float = 0.0):
        if client_id not in self.clients:
            raise ClientNotFound(client_id)
        client = self.clients[client_id]

        if currency in client.accounts:
            raise AccountExistsError(currency)
        account = Account(self.next_account_id, client_id, currency, initial_balance)
        self.accounts[self.next_account_id] = account

        client.accounts[currency] = account
        self.next_account_id += 1
        print(f"Account opened {account.id } ({currency}) for the client {client.name } with the {initial_balance} balance")

    def deposit(self, client_id:int, currency:str, amount:float):
        if client_id not in self.clients:
            raise ClientNotFound(client_id)
        client = self.clients[client_id]

        if currency not in client.accounts:
            raise AccountNotFoundError(currency)
        account = client.accounts[currency]

        if amount <= 0:
            raise ValueError('Amount must be positive')
        account.balance += amount
        print(f"Account {account.id } ({currency}) credited to {amount}. New balance sheet: {account.balance}")

    def transfer(self, from_client_id:int, from_currency:str, to_client_id:int, to_currency:str, amount:float):
        if from_client_id not in self.clients:
            raise ClientNotFound(from_client_id)
        if to_client_id not in self.clients:
            raise ClientNotFound(to_client_id)

        from_client = self.clients[from_client_id]
        to_client = self.clients[to_client_id]

        if from_currency not in from_client.accounts:
            raise AccountNotFoundError(from_currency)
        if to_currency not in to_client.accounts:
            raise AccountNotFoundError(to_currency)

        if amount <= 0:
            raise ValueError('Amount must be positive')
        from_account = from_client.accounts[from_currency]
        from_account.withdraw(amount)

        to_account = to_client.accounts[to_currency]
        to_account.balance += amount
        print(f"Transferred {amount} {from_currency} from {from_client.name} to {to_client.name} ({to_currency})")

    def save_data(self, filename = "clients.json"):
        data = {}
        for client_id, client in self.clients.items():
            account_data = {currency: account.balance for currency, account in client.accounts.items()}
            data[client_id] = {
                "name" : client.name,
                "accounts" : account_data,
            }
        with open(filename, "w") as f:
            json.dump(data, f)

    def load_data(self, filename="clients.json"):
        if not os.path.exists(filename):
            return
        with open(filename, "r") as f:
            data = json.load(f)
        for client_id_str, client_data in data.items():
            client_id = int(client_id_str)
            client = Client(client_id, client_data["name"])
            self.clients[client_id] = client
            self.next_client_id = max(self.next_client_id, client_id+1)
            for currency, balance in client_data["accounts"].items():
                account = Account(self.next_account_id, client_id, currency, balance)
                self.accounts[self.next_account_id] = account
                client.accounts[currency] = account
                self.next_account_id += 1



bank = Bank()
bank.load_data()
while True:
    print("1. Creating a new account")
    print("2. Open an account")
    print("3. Top up your account")
    print("4. Withdraw from the account")
    print("5. Transfer money")
    print("6. Show all accounts")
    print("7. Exit")

    choice = input("Enter your choice: ")

    try:
        if choice == "1":
            name = input("Enter your name: ")
            new_client_id = bank.next_client_id
            bank.clients[new_client_id] = Client(new_client_id, name)
            bank.next_client_id += 1
            print(f"Client {name} create with ID {new_client_id}")
            bank.save_data()
        else:
            client_id = int(input("Enter client ID: "))

        if choice == "2":
            currency = input("Enter your currency: ")
            initial = float(input("Start balance: "))
            bank.open_account(client_id, currency, initial)
            bank.save_data()

        elif choice == "3":
            currency = input("Enter your currency: ")
            amount = float(input("Enter your amount: "))
            bank.deposit(client_id, currency, amount)
            bank.save_data()

        elif choice == "4":
            currency = input("Enter your currency: ")
            amount = float(input("Enter your amount: "))
            account = bank.clients[client_id].accounts[currency]
            account.withdraw(amount)
            bank.save_data()

        elif choice == "5":
            to_id = int(input("Recipient's ID: "))
            from_currency = input("Enter your currency: ")
            to_currency = input("Recipient's currency: ")
            amount = float(input("Enter amount: "))
            bank.transfer(client_id, from_currency, to_id, to_currency, amount)
            bank.save_data()

        elif choice == "6":
            client = bank.clients[client_id]
            print(client)

        elif choice == "7":
            break

        else:
            print("Invalid choice")

    except BankError as e:
        print("Error: ", e)
    except ValueError as e:
        print("Error: ", e)


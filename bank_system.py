import sqlite3 
import pandas as pd

class Consultant:
    def __init__(self, name):
        self.name = name
    
    def query_user(self):
        return f"SELECT * FROM accounts WHERE name = '{self.name}'"
    
class Transactor:
    def __init__(self, user1, user2, amount):
        self.user1 = user1
        self.user2 = user2
        self.amount = amount
    
    def make_transaction(self):
        return [
            f"UPDATE accounts SET balance = balance + {self.amount} WHERE name = '{self.user1}';",
            f"UPDATE accounts SET balance = balance - {self.amount} WHERE name = '{self.user2}';"
        ]
    
    def check_balance(self):
        return f"SELECT balance FROM accounts WHERE name = '{self.user2}'"
        

def query():
    with sqlite3.connect("C:/Users/tobia/OneDrive/Desktop/Projects/Bank_Exercise/accounts.db") as connect:
        while True:
            my_account = Consultant(input("Enter your name: ").lower())
            query = my_account.query_user()
            try:
                show_query = pd.read_sql_query(query, connect)
                if show_query.empty:
                    print("User not found")
                else:
                    print(show_query)
                    break
            except Exception as e:
                print(f"Unexpected error: {e}")

def transaction():
    with sqlite3.connect("C:/Users/tobia/OneDrive/Desktop/Projects/Bank_Exercise/accounts.db") as connect:
        cursor = connect.cursor()
        person1 = input("Which user is requesting money?: ").lower()
        person2 = input("Which user is giving the money?: ").lower()
        money = abs(int(input("How much money is being requested?: ")))
        
        cursor.execute(f"SELECT COUNT(*) FROM accounts WHERE name = '{person1}'")
        user1_exists = cursor.fetchone()[0] > 0

        cursor.execute(f"SELECT COUNT(*) FROM accounts WHERE name = '{person2}'")
        user2_exists = cursor.fetchone()[0] > 0

        if not user1_exists or not user2_exists:
            print("Error: One or both users do not exist in the database.")
            return

        form_transaction = Transactor(person1, person2, money)
        balance_check = form_transaction.check_balance()
        cursor.execute(balance_check)
        current_balance = cursor.fetchone()

        if current_balance and current_balance[0] < money:
            print("Insufficient balance")
        else:
            try:
                cursor.execute("BEGIN TRANSACTION;")
                for query in form_transaction.make_transaction():
                    cursor.execute(query)
                connect.commit()
                show_query = pd.read_sql_query(f"SELECT * FROM accounts WHERE name IN ('{person1}', '{person2}')", connect)
                print(show_query)
            except Exception as e:
                connect.rollback()
                print(f"Unexpected error: {e}")

class Checkbook:
    def __init__(self):
        self.balance = 0.0

    def deposit(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        self.balance += amount
        print(f"Deposited: ${amount:.2f}")
        self.get_balance()

    def withdraw(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
        elif amount > self.balance:
            print("Insufficient funds to complete the withdrawal.")
        else:
            self.balance -= amount
            print(f"Withdrew: ${amount:.2f}")
            self.get_balance()

    def get_balance(self):
        print(f"Current Balance: ${self.balance:.2f}")

def main():
    cb = Checkbook()
    print("Welcome to your Checkbook!")
    while True:
        action = input("\nChoose an action (deposit, withdraw, balance, exit): ").strip().lower()

        if action == 'exit':
            print("Goodbye!")
            break

        elif action in ['deposit', 'withdraw']:
            try:
                amount = float(input("Enter amount: $"))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if action == 'deposit':
                cb.deposit(amount)
            else:
                cb.withdraw(amount)

        elif action == 'balance':
            cb.get_balance()

        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()


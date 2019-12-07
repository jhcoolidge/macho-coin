try:
    from greetings import random_greeting
    from utilities import validate_input  # Disallows users from making silly options.
    from wallet import generate_wallet, verify_ownership  # Simple wallet functions. Docstrings within.
    import block  # Allows the blockchain to initialize and allows main.py to utilize its functions.
except [ImportError, ModuleNotFoundError] as e:
    print("Main files failed to load! Program exiting. Error: " + e)
    exit(1)


def main():
    # Basic greetings and selection screen. Validates user input.
    print("Please enter your wallet address to get started! Or if you don't have one, make one here!")
    login = input("(select) wallet/(install) wallet")
    login = validate_input(choice=login, parameters=["select", "install"])

    current_wallet = ""
    address = ""

    if login == "select":
        # This verifies that the user has access to the private key for this wallet address.
        # If verification is not possible, the user cannot use this address for transactions.

        verified = False

        while not verified:
            address = input("Please input your wallet address.")
            private_key_directory = input("Please input the file containing the private key. (Copy the whole directory)")
            verified = verify_ownership(address=address, private_key_directory=private_key_directory)

        current_wallet = address

    elif login == "install":
        # This selection allows the user to create a new wallet address and related key pair.
        # This code also automatically verifies the user as someone with an address but zero coins.

        wallet = generate_wallet()

        print("Your wallet address is: " + wallet[0] + "\n")
        print("Your public key is: " + wallet[1])
        print("Your private key has been written to a file.")

        with open(wallet[0] + ".txt", "w") as f:
            f.write("Wallet address: " + wallet[0] + "\n")
            f.write("Public key: " + wallet[1])

        with open(wallet[0] + "private.txt", "wt") as p:
            p.write(wallet[2])

        print("Do not lose these! They cannot be recovered!\n\n\n")
        current_wallet = wallet[0]

    blockchain = block.BlockChain()
    print("\n\n\n\n\n\n\n\n\n\n")
    random_greeting()

    # Below print statement only prints Genesis block, only needed for testing and can be removed
    # print(blockchain.chain)

    print("Welcome to the MachoCoin miner and wallet utility! What would you like to do?")
    while True:
        # Basic greetings and selection screen. Validates user input.
        # Gives some more advanced options as the user had verified the ownership of current_wallet.
        choice = input("validate/access/mine/transfer/stop")
        print("\n")

        choice = validate_input(choice=choice, parameters=["mine", "access", "transfer", "stop", "validate"])

        if choice == "access":
            # Simply prints out how many coins you have for the given address.

            print("Here are your wallet contents.")
            current_amount = blockchain.validate_coins_for_address(current_wallet)
            print("You have " + str(current_amount) + " MachoCoins for this address.")

        elif choice == "mine":
            # Mines a transaction that is not currently on the blockchain.
            # If there are no transactions, this code exits automatically.

            print("Beginning to mine!")
            blockchain.mine(current_wallet)
            print(blockchain)

        elif choice == "transfer":
            # This code allows the user to make a transaction to be added to the blockchain.
            # This will also validate that the user has enough MachoCoins to make the requested transaction.
            # Also, this code automatically attempts to digitally sign and verify the transaction, exiting if it cannot.

            done = False
            current_amount = blockchain.validate_coins_for_address(current_wallet)
            print("You have " + str(current_amount) + " MachoCoins for this address.")

            while not done:
                recipient_address = input("Which wallet do you want to transfer to? "
                                          "(You should copy and paste the address.)")
                sender_private = input("Please input your private key.")
                amount = input("How much would you like to send them?")

                if int(amount) > int(current_amount):
                    print("You do not have enough coins to make this transaction!")
                    break

                done = blockchain.generate_transaction(sender=current_wallet, recipient=recipient_address,
                                                       sender_private_key=sender_private, amount=amount)

        elif choice == "stop":
            print("OK, I'll see you later then.")
            exit(0)

        elif choice == "validate":
            print(blockchain)
            blockchain.validate_blockchain()

        print("Would you like to do anything else?")


if __name__ == "__main__":
    main()

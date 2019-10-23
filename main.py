try:
    from utilities import validate_input
    from wallet import generate_wallet
    import block
except (ImportError, generate_wallet.ImportError, validate_input.ImportError) as e:
    print("Main files failed to load! Program exiting. Error: " + e)
    exit(1)


def main():
    # Optional features?
    # Command line support, GUI, Web app support
    # Creation of hash function
    # Creation of asymmetric key generation

    print("Please enter your wallet address to get started! Or if you don't have one, make one here!")
    login = input("(select) wallet/(install) wallet")
    login = validate_input(choice=login, parameters=["select", "install"])

    if login == "select":
        # TODO: MAKE A LOOKUP/VERIFICATION OF WALLETS!
        address = input("Please input your wallet address.")
        pass
    elif login == "install":
        # Wallets can be just public keys? Have to be verified? Find out later.
        wallet = generate_wallet()
        print("Your wallet address is: " + wallet[0] + "\n")
        print("Your public key is: " + wallet[1])
        print("Your private key is: " + wallet[2] + "\nDon't share it with anyone!!!")
        print("Do not lose these! They cannot be recovered!\n")

    print("Welcome to the MachoCoin miner and wallet utility! What would you like to do?")
    choice = input("access/mine/transfer")

    choice = validate_input(choice=choice, parameters=["mine", "access", "transfer"])

    if choice == "access":
        # This will hopefully be a simple lookup. Don't doubt the difficulty of this.
        # TODO: MAKE AND PRINT OUT WALLET CONTENTS
        print("Here are your wallet contents.")

    elif choice == "mine":
        # Add wallet addresses to the blockchain as well.
        # TODO: CREATE THE BLOCKCHAIN AND THE MINING UTILITY
        print("Beginning to mine!")
    elif choice == "transfer":
        # TODO: CONNECT TO OTHER WALLETS AND UPDATE THEIR CONTENTS
        # This can be done by having the sender address, which is already logged into.
        # Other requirements is the private key of the sender, or
        # TODO: VERIFY OWNER OF THE WALLET!!!! SIGN THE PUBLIC WITH THE PRIVATE KEY.
        # and also the recipient address, as well as the transaction amount. Don't forget to verify the amount taken
        # from the sender.
        print("Which wallet do you want to transfer to? (You should copy and paste the address.)")
        address = input()


if __name__ == "__main__":
    main()

try:
    from utilities import validate_input
    import block
except ImportError:
    print("Files failed to load! Program exiting.")
    exit(1)


def main():

    print("Welcome to the MachoCoin miner and wallet utility! What would you like to do?")
    choice = input("access/mine/transfer")

    choice = validate_input(choice=choice, parameters=["mine", "access", "transfer"])

    if choice == "access":
        # TODO: MAKE AND PRINT OUT WALLET CONTENTS
        print("Here are your wallet contents.")

    elif choice == "mine":
        # TODO: CREATE THE BLOCKCHAIN AND THE MINING UTILITY
        print("Beginning to mine!")
    elif choice == "transfer":
        # TODO: CONNECT TO OTHER WALLETS AND UPDATE THEIR CONTENTS
        print("Which wallet do you want to transfer to? (You should copy and paste the address.)")
        address = input()


if __name__ == "__main__":
    main()

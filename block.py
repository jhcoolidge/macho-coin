try:
    from time import time
    from datetime import datetime
    from Crypto.Signature import DSS
    from Crypto.PublicKey import ECC
    from Crypto.Hash import SHA3_256
    import hashlib
    import re
except [ImportError, ModuleNotFoundError] as e:
    print("Failed to import a module! Program quitting.")
    exit(1)


class Block(object):

    def __init__(self, position, signature, previous_hash, timestamp, sender, recipient, amount, nonce):
        self.position = position
        self.previous_hash = previous_hash
        self.signature = signature
        self.timestamp = timestamp
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.nonce = nonce

    def __repr__(self):
        value = "Position: " + str(self.position) + \
                "\nSender: " + str(self.sender) + \
                "\nRecipient: " + str(self.recipient) + \
                "\nAmount: " + str(self.amount) + \
                "\nTime: " + str(self.timestamp) + \
                "\nPrevious Hash Value: " + str(self.previous_hash) + \
                "\nSignature: " + str(self.signature)
        return value


class BlockChain(object):

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_genesis()

    def create_genesis(self):
        # Creates the first block on the chain.
        # The first block will ALWAYS have the same data.

        genesis_block = Block(position=0,
                              previous_hash="0000000000000000000000000000000000000000000000000000000000000000",
                              signature="Genesis",
                              timestamp="1970",
                              sender="MachoCoin Admin",
                              recipient="2wDRK4nXfvFZJPxNxYEAd43ynst6Ec6cheWtVTD6t8xJ6vqSuR7zp4RmWUUnUPh5xmuA9fZD5Z9mF6qy5",
                              amount=100,
                              nonce=160631)

        self.chain.append(genesis_block)
        return

    def prove_work(self, block):
        """
        Will do an exhaustive search of nonce values until an arbitrarily signed hash is found.

        Parameters:
        -----------
        :param block:
            The block of transaction information to find the nonce for. This is the block to be mined.

        Returns:
        --------
        :return:
            The block with the updated nonce value.
        """

        done = False
        while not done:
            check = self.hash(block)

            if check.startswith("0000"):
                done = True
            else:
                block.nonce = block.nonce + 1

        return block

    def current_block(self):
        # Returns the last block in the chain, or the current block.
        return self.chain[-1]

    def mine(self, mining_address):
        """
        Will create a block object for the transactions waiting. Will reward the miner with 1 MachoCoin.

        Parameters:
        -----------
        :param mining_address:
            The wallet address of the currently signed in user.

        Returns:
        --------
        :return:
            True if the block was successfully mined. False if there are no transactions waiting to be mined.
        """

        transactions = self.transactions
        no_reward = False

        if len(transactions) == 0:
            print("No transactions to process!")
            return False

        # Initializes beginning data for a block from non-mined transactions.
        sender = transactions[0][0]
        recipient = transactions[0][1]
        amount = transactions[0][2]
        signature = transactions[0][3]

        # Stops people from infinitely mining blocks and gaining MachoCoin.
        if sender == "MachoCoin Mining Rewards":
            no_reward = True

        # Initializes the previous hash of the last block along with its position + 1
        current = self.current_block()
        position = current.position + 1
        previous_hash = self.hash(current)

        # Creates a timestamp in human-readable format.
        timestamp = datetime.fromtimestamp(datetime.timestamp(datetime.now())).isoformat()

        block = Block(position=position, previous_hash=previous_hash, signature=signature, nonce=0,
                      timestamp=timestamp, sender=sender, recipient=recipient, amount=amount)
        block = self.prove_work(block)

        self.chain.append(block)
        del self.transactions[0]

        # Gain a possible reward amount for mining a transaction!
        if not no_reward:
            print("Congratulations! You earned a reward!")
            self.transactions.append(["MachoCoin Mining Rewards", mining_address, 1, "Mining Reward"])
        else:
            print("Sorry! No reward for mining a mining reward!")
        return True

    @staticmethod
    def hash(block):
        """
        Creates a hash of the block for use in creating new blocks.
        Also a function in mining for a provable nonce.

        Parameters:
        -----------
        :param block:
            A block of transaction information.

        Returns:
        --------
        :return:
            The hash value in ASCII format.
        """

        block_binary = str({"position": block.position,
                            "previous_hash": block.previous_hash,
                            "signature": block.signature,
                            "timestamp": block.timestamp,
                            "sender": block.sender,
                            "recipient": block.recipient,
                            "amount": block.amount,
                            "nonce": block.nonce}).encode("utf-8")

        function = hashlib.sha3_256()
        function.update(block_binary)
        value = function.hexdigest()
        return value

    def generate_transaction(self, sender=None, recipient=None, amount=None, sender_private_key=None):
        """
        Creates a transaction to be mined using the transfer information from user to user.

        Parameters:
        -----------
        :param sender:
            A wallet address that the user signed in as.
        :param recipient:
            A wallet address to send MachoCoin to.
        :param amount:
            The amount of MachoCoin to send.
        :param sender_private_key:
            The Private key of the signed in user, for digital signatures.

        Returns:
        --------
        :return:
            True if the transaction was added, False if not.
        """

        if sender is None or recipient is None or amount is None or sender_private_key is None:
            print("One of the required arguments is missing.\n")
            return False

        try:
            with open(sender_private_key, "rt") as f:
                private_key = ECC.import_key(f.read())

            with open(sender + ".txt", "rt") as f1:
                public_key = re.findall("ecdsa-sha2-nistp256(\W.*)", f1.read())
                public_key = "ecdsa-sha2-nistp256" + public_key[0]
                public_key = ECC.import_key(public_key)

        except FileNotFoundError:
            print("A file was not found.")
            return False

        # Creates a ECDSA Signature using the Private key provided by the user.
        sign_method = DSS.new(private_key, "fips-186-3")
        hashed = SHA3_256.new()
        hashed.update(amount.encode("utf-8"))
        signature = sign_method.sign(hashed)

        # Verifies the above Signature using the public key in the wallet file.
        received_message = hashed.digest()
        h = SHA3_256.new(received_message)
        h.update(received_message)
        verifier = DSS.new(public_key, 'fips-186-3')

        try:
            verifier.verify(hashed, signature)
        except ValueError:
            print("The signature could not be verified!")
            return False

        self.transactions.append([sender, recipient, amount, signature])
        print("Transaction successfully added to the blockchain!")
        return True

    def validate_blockchain(self):
        """
        Validates the hashes and the signatures of each block on the blockchain.
        Ensures that the blockchain was not tampered with.

        Returns:
        --------
        :return:
            True if the blockchain is successfully validated. False if not.
        """

        for block in self.chain:
            address = block.sender

            # Skips non-signed transactions, as these are not meant to be signed at all.
            # Also skips the genesis block, for the same reason.
            if address == "MachoCoin Mining Rewards" or block.position == 0:
                continue

            if not block.previous_hash.startswith("0000"):
                print("Hash at " + block.position + "was not signed!")
                return False

            try:
                with open(address + ".txt", "rt") as f1:
                    public_key = re.findall("ecdsa-sha2-nistp256(\W.*)", f1.read())
                    public_key = "ecdsa-sha2-nistp256" + public_key[0]
                    public_key = ECC.import_key(public_key)

                verifier = DSS.new(public_key, "fips-186-3")

            except FileNotFoundError:
                print("Sender's public key could not be found.")
                return False

            try:
                hashed = SHA3_256.new()
                hashed.update(block.amount.encode("utf-8"))
                verifier.verify(hashed, block.signature)

            except ValueError:
                print("Signature at " + block.position + "failed to verify!")

        print("Blockchain successfully validated.")
        return True

    def validate_coins_for_address(self, address):
        """
        Checks how many MachoCoins the user has at the current time.
        Utilizes both mined and pre-mined blocks so that the user cannot spend more than they have.

        Parameters:
        -----------
        :param address:
            The wallet address of the currently signed in user.

        Returns:
        --------
        :return:
            The integer amount of MachoCoin that the user currently has.
        """

        total_amount = 0

        for block in self.chain:

            if block.sender == address:
                total_amount = total_amount - int(block.amount)
            elif block.recipient == address:
                total_amount = total_amount + int(block.amount)

            if total_amount < 0:
                print("Error! Coins are a negative value!")
                raise

        transaction = self.transactions
        for index in range(len(self.transactions)):

            if transaction[index][0] == address:
                total_amount = total_amount - int(transaction[index][2])
            elif transaction[index][1] == address:
                total_amount = total_amount + int(transaction[index][2])

        return total_amount

    def __repr__(self):

        print("---------------------------------------------------------------------------------------------------")
        for block in self.chain:
            print(block)
            print("---------------------------------------------------------------------------------------------------")

        return ""

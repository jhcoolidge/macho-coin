try:
    from time import time
    from hashlib import sha3_256
except (time.ImportError, sha3_256.ImportError):
    print("Failed to import a module! Program quitting.")
    exit(1)


class Block:

    def __init__(self, position, proof_number, previous_hash, data, timestamp=None):
        self.position = position
        self.proof_number = proof_number
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp or time()

    def hash(self):
        return

    def get_information(self):
        return


class BlockChain:

    def __init__(self):
        self.chain = []
        self.start_chain()

    def start_chain(self):
        # Creates the first block in the chain. This is known as the genesis block.

        return

    def current_block(self):
        # Returns the last block in the chain, or the current block.
        return self.chain[-1]

    def create_block(self, proof_number, previous_hash, data=[]):
        # Creates a block based on the given parameters. Appends it to the end of the blockchain.
        return

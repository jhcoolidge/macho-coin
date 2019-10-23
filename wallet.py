try:
    import os
    from utilities import strip_keys
    from Crypto.PublicKey import ECC
    from utilities import strip_keys
    import hashlib
    from base58 import b58encode_check as b58check
except (ECC.ImportError, os.ImportError) as e:
    print("There was an error importing wallet packages. Exiting program. Error: " + e)
    exit(1)


def generate_keys():
    """
    This function creates ECC public/private key pairs for wallet generation.
    :returns a list of keys in the format [private, public]:
    """
    private = ECC.generate(curve="P-256")
    public = private.public_key()
    private = private.export_key(format="PEM")
    public = public.export_key(format="OpenSSH")

    return [private, public]


def generate_wallet_address(public):
    # TODO: Wallet addresses are not 25 bytes long.
    """
    This function generates a Bitcoin-esque wallet address using the procedure listed on their wiki:
    https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
    :param public:
    :returns a valid wallet address:
    """

    # Taking the SHA-256 hash value of the public key.
    hash_function = hashlib.sha256()
    hash_function.update(public.encode("utf-8"))
    address = hash_function.hexdigest()

    # Taking the RIPEMD-160 hash value of the hashed public key.
    hash_function = hashlib.new('ripemd160')
    hash_function.update(address.encode("utf-8"))
    address = hash_function.hexdigest()

    # The zeros represent what network this wallet is meant to be used on. "00" is main network.
    address = "00" + address

    # Produce the checksum and append it to the end of the address.
    checksum = produce_wallet_checksum(address)
    address = address + checksum

    # Finally, produce the Base58Check encoded value, and this is the actual wallet address.
    address = b58check(address.encode("utf-8"))
    address = address.decode("utf-8")
    return address


def produce_wallet_checksum(hash_value):
    checksum = ""

    # We take the SHA-256 value of the previous hash twice.
    for x in range(2):
        hash_function = hashlib.sha256()
        hash_function.update(hash_value.encode("utf-8"))
        hash_value = hash_function.hexdigest()

    # We then take the first 4 bytes of the string. This is the checksum.
    checksum = hash_value[:4]
    return checksum


def generate_wallet():
    key_pair = generate_keys()
    public = strip_keys(key_pair[1], "ecdsa-sha2-nistp256 ")
    private = strip_keys(key_pair[0], "-----.*?-----")
    address = generate_wallet_address(public)
    return [address, public, private]


def verify_ownership(address, private_key):
    """
    Takes a wallet address and a private key, and signs a message with the private key to be decrypted by the wallet
    address. This will authenticate that the user of the address has the private key corresponding to the
    public key of the wallet.
    :returns True if validated, False if not:
    """
    message = "Challenge"
    return False
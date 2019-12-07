try:
    import re
    from Crypto.PublicKey import ECC
    from Crypto.Signature import DSS
    from Crypto.Hash import SHA3_256, RIPEMD160
    from base58 import b58encode_check as b58check
except [ImportError, ModuleNotFoundError] as e:
    print("There was an error importing wallet packages. Exiting program. Error: " + e)
    exit(1)


def generate_keys():
    """
    This function creates ECC public/private key pairs for wallet generation.

    Returns:
    --------
    :returns:
        A list of keys in the format [private, public].
    """
    private = ECC.generate(curve="P-256")
    public = private.public_key()
    private = private.export_key(format="PEM")
    public = public.export_key(format="OpenSSH")

    return [private, public]


def generate_wallet_address(public):
    """
    This function generates a Bitcoin-esque wallet address using the procedure listed on their wiki:
    https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses

    Parameters:
    -----------
    :param public:
        The ECC public key to be converted to the wallet address.

    Returns:
    --------
    :returns:
        The finalized routable wallet address.
    """

    # Taking the SHA-256 hash value of the public key.
    hash_function = SHA3_256.new(public.encode("ASCII"))
    address = hash_function.digest()

    # Taking the RIPEMD-160 hash value of the hashed public key.
    hash_function = RIPEMD160.new(address)
    address = hash_function.hexdigest()

    # The zeros represent what network this wallet is meant to be used on. "00" is main network.
    address = "00" + address

    # Produce the checksum and append it to the end of the address.
    checksum = produce_wallet_checksum(address)
    address = address + checksum

    # Finally, produce the Base58Check encoded value, and this is the actual wallet address.
    address = b58check(address.encode("ASCII"))
    address = address.decode("ASCII")
    return address


def produce_wallet_checksum(hash_value):

    hash_function = SHA3_256.new(hash_value.encode("ASCII"))
    hash_value = hash_function.digest()
    hash_function = SHA3_256.new(hash_value)
    hash_value = hash_function.digest()

    # We then take the first 4 bytes of the string. This is the checksum.
    checksum = hash_value[:4]
    return str(checksum)


def generate_wallet():
    key_pair = generate_keys()
    public = key_pair[1]
    private = key_pair[0]
    address = generate_wallet_address(public)
    return [address, public, private]


def verify_ownership(address, private_key_directory):
    """
    Takes a wallet address and a private key, and signs a message with the private key to be decrypted by the wallet
    address. This will authenticate that the user of the address has the private key corresponding to the
    public key of the wallet.

    Returns:
    --------
    :returns:
        True if the signature validates, False if not.
    """

    try:
        with open(private_key_directory, "rt") as f:
            private_key = ECC.import_key(f.read())

        with open(address + ".txt", "rt") as f1:
            public_key = re.findall("ecdsa-sha2-nistp256(\W.*)", f1.read())
            public_key = "ecdsa-sha2-nistp256" + public_key[0]
            public_key = ECC.import_key(public_key)

    except FileNotFoundError:
        print("A file was not found.")
        return False

    # Creates a ECDSA Signature using the Private key provided by the user.
    sign_method = DSS.new(private_key, "fips-186-3")
    hashed = SHA3_256.new()
    hashed.update(b"Bet")
    signature = sign_method.sign(hashed)

    # Verifies the above Signature using the public key in the wallet file.
    received_message = hashed.digest()
    h = SHA3_256.new(received_message)
    h.update(received_message)
    verifier = DSS.new(public_key, 'fips-186-3')

    try:
        verifier.verify(hashed, signature)
        print("The signature was verified!")
        return True
    except ValueError:
        print("The signature could not be verified!")
        return False

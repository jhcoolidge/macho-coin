try:
    import os
    from Crypto.PublicKey import ECC
    from utilities import strip_keys
except (ECC.ImportError, os.ImportError) as e:
    print("There was an error importing wallet packages. Exiting program. Error: " + e)
    exit(1)


def generate_keys():
    """
    This function creates ECC public/private key pairs for wallet generation.
    :returns a list of keys in the format [private, public]:
    """
    print("Generating key pairs! This may take awhile....")
    private = ECC.generate(curve="P-256")
    public = private.public_key()
    private = private.export_key(format="PEM")
    public = public.export_key(format="OpenSSH")
    return [private, public]


def verify_ownership(address, private_key):
    """
    Takes a wallet address and a private key, and signs a message with the private key to be decrypted by the wallet
    address. This will authenticate that the user of the address has the private key corresponding to the
    public key of the wallet.
    :returns True if validated, False if not:
    """
    message = "Challenge"
    return False


def generate_wallet_address(public, private):
    address = private
    return address
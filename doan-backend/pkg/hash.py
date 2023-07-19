import binascii
import hashlib
import os


def get_hash(string):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    pwd_hash = hashlib.pbkdf2_hmac("sha512", string.encode("utf-8"), salt, 100000)
    pwd_hash = binascii.hexlify(pwd_hash)
    result = (salt + pwd_hash).decode("ascii")
    return result


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""

    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha512", provided_password.encode("utf-8"), salt.encode("ascii"), 100000
    )
    return stored_password == binascii.hexlify(pwd_hash).decode("ascii")

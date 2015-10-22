#!/usr/bin/env python
# TODO: Add optional master password argument
# TODO: Better help.

import string, hashlib, argparse, getpass

DEFAULT_ALLOWED_CHARS = string.ascii_letters + string.digits
DEFAULT_PASSWORD_LENGTH = 12

def derive_password(master, website, allowed_chars, length):
    hash_bytes = hashlib.pbkdf2_hmac(
        'sha256',
        bytes(master, 'utf-8'),
        bytes(website + str(length), 'utf-8'),
        100000)
    password = ''
    i = 0
    while len(password) < length:
        password += allowed_chars[hash_bytes[i] % len(allowed_chars)]
        i = (i + 1) % len(hash_bytes)
    return password

parser = argparse.ArgumentParser()
parser.add_argument('--allowed',
    default=DEFAULT_ALLOWED_CHARS,
    help='list of allowed characters.'
)
parser.add_argument('--length',
    default=DEFAULT_PASSWORD_LENGTH,
    type=int,
    help='password length.'
)
parser.add_argument('website')

args = parser.parse_args()
master_password = getpass.getpass(prompt='Master password:')
print(derive_password(master_password, args.website, args.allowed, args.length))

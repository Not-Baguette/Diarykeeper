from twofish import Twofish


def encrypt_file_two(key, data):
    # check the length of the plaintext and add "a" to it if it is not a multiple of 16 cuz im too lazy to do padding
    if len(key) % 16 != 0:
        key_fill = 16 - len(key) % 16
        key += "a" * key_fill
    if len(key) > 32:
        key = key[:32]

    # convert plaintext to bytes
    try:
        if len(data) % 16 != 0:
            plaintext_fill = 16 - len(data) % 16
            data += b"a" * plaintext_fill
    except TypeError:
        data = str.encode(data)
        if len(data) % 16 != 0:
            plaintext_fill = 16 - len(data) % 16
            data += b"a" * plaintext_fill

    cipher = Twofish()
    cipher.set_key(str.encode(key))

    try:
        return cipher.encrypt(data)
    except TypeError:
        return None  # User might be accessing the diary via another account


def decrypt_file_two(key, data):
    if len(key) % 16 != 0:
        key_fill = 16 - len(key) % 16
        key += "a" * key_fill
    if len(key) > 32:
        key = key[:32]

    cipher = Twofish()
    cipher.set_key(str.encode(key))

    plaintext = cipher.decrypt(data)

    while plaintext.endswith(b"a"):
        plaintext = plaintext[:-1]

    return plaintext


def save_diary(file_path, acc_id, data):
    """
    Saves the diary. Encrypt it with the id too as the key via Twofish
    """
    if file_path == "" or file_path is None:
        return False
    encrypted_data = encrypt_file_two(acc_id, data)

    # Save the diary
    if encrypted_data is not None:
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        return True
    else:
        return False


def open_diary(file_path, acc_id):
    """
    Open the diary. Decrypt it with the id too as the key via Twofish
    """
    with open(file_path, "rb") as file:
        diary_var = file.read()

    # decrypt the text
    return decrypt_file_two(acc_id, diary_var)

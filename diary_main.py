from twofish import Twofish


def encrypt_file_two(key, data):
    # check the length of the plaintext and add "a" to it if it is not a multiple of 16 cuz im too lazy to do padding
    if len(key) % 16 != 0:
        key_fill = 16 - len(key) % 16
        key += "a" * key_fill

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

    return cipher.encrypt(data)


def decrypt_file_two(key, data):
    if len(key) % 16 != 0:
        key_fill = 16 - len(key) % 16
        key += "a" * key_fill

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
    encrypted_data = encrypt_file_two(acc_id, data)

    # Save the diary
    with open(file_path, "wb") as file:
        file.write(encrypted_data)


def open_diary(file_path, acc_id):
    """
    Open the diary. Decrypt it with the id too as the key via Twofish
    """
    with open(file_path, "rb") as file:
        diary_var = file.read()

    # decrypt the text
    return decrypt_file_two(acc_id, diary_var)

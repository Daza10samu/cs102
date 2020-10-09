def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword_len = len(keyword)
    shifts = []
    for char in keyword:
        if char.islower():
            shifts.append(ord(char) - ord('a'))
        else:
            shifts.append(ord(char) - ord('A'))
    for index, char in enumerate(plaintext):
        if not char.isalpha():
            ciphertext += char
            continue
        char_index = ord(char)
        is_lower = char.islower()
        if is_lower:
            alphabet_start_number = ord('a')
        else:
            alphabet_start_number = ord('A')
        letter_number = char_index - alphabet_start_number
        cipher_number = (letter_number + shifts[index % keyword_len]) % 26
        ciphertext += chr(cipher_number + alphabet_start_number)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword_len = len(keyword)
    shifts = []
    for char in keyword:
        if char.islower():
            shifts.append(ord(char) - ord('a'))
        else:
            shifts.append(ord(char) - ord('A'))
    for index, char in enumerate(ciphertext):
        if not char.isalpha():
            plaintext += char
            continue
        char_index = ord(char)
        is_lower = char.islower()
        if is_lower:
            alphabet_start_number = ord('a')
        else:
            alphabet_start_number = ord('A')
        cipher_number = char_index - alphabet_start_number
        letter_number = (26 + cipher_number - shifts[index % keyword_len]) % 26
        plaintext += chr(letter_number + alphabet_start_number)
    return plaintext

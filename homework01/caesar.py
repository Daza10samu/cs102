import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
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
        cipher_number = (letter_number + shift) % 26
        ciphertext += chr(cipher_number + alphabet_start_number)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
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
        letter_number = (26 + cipher_number - shift) % 26
        plaintext += chr(letter_number + alphabet_start_number)
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift

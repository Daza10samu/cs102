package vigenere

func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string

	var shift int32
	for index, char := range plaintext {
		key_char_index := int32(keyword[index%len(keyword)])
		if 'a' <= key_char_index && key_char_index <= 'z' {
			shift = key_char_index - 'a'
		} else {
			shift = key_char_index - 'A'
		}
		if 'a' <= char && char <= 'z' {
			ciphertext += string('a' + (char+shift-'a')%26)
		} else if 'A' <= char && char <= 'Z' {
			ciphertext += string('A' + (char+shift-'A')%26)
		} else {
			ciphertext += string(char)
		}
	}

	return ciphertext
}

func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string

	var shift int32
	for index, char := range ciphertext {
		key_char_index := int32(keyword[index%len(keyword)])
		if 'a' <= key_char_index && key_char_index <= 'z' {
			shift = key_char_index - 'a'
		} else {
			shift = key_char_index - 'A'
		}
		if 'a' <= char && char <= 'z' {
			plaintext += string('a' + (26+char-shift-'a')%26)
		} else if 'A' <= char && char <= 'Z' {
			plaintext += string('A' + (26+char-shift-'A')%26)
		} else {
			plaintext += string(char)
		}
	}

	return plaintext
}

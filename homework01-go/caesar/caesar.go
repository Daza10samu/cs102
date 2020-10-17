package caesar

func EncryptCaesar(plaintext string, shift int) string {
	var ciphertext string

	for _, char := range plaintext {
		if 'a' <= char && char <= 'z' {
			ciphertext += string('a' + (char+int32(shift)-'a')%26)
		} else if 'A' <= char && char <= 'Z' {
			ciphertext += string('A' + (char+int32(shift)-'A')%26)
		} else {
			ciphertext += string(char)
		}
	}

	return ciphertext
}

func DecryptCaesar(ciphertext string, shift int) string {
	var plaintext string

	for _, char := range ciphertext {
		if 'a' <= char && char <= 'z' {
			plaintext += string('a' + (26-'a'+char-int32(shift))%26)
		} else if 'A' <= char && char <= 'Z' {
			plaintext += string('A' + (26-'A'+char-int32(shift))%26)
		} else {
			plaintext += string(char)
		}
	}

	return plaintext
}

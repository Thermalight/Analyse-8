import hashlib

valid_chars = [chr(i) for i in range(32,127)]

toInt = lambda letter: ord(letter) - ord(valid_chars[0])
toChar = lambda number: chr(number + ord(valid_chars[0]))
add_char = lambda a,b: toChar(((toInt(a)+toInt(b)) % (ord(valid_chars[-1]) - ord(valid_chars[0]))))
subtract_char = lambda a,b: toChar(((toInt(a)-toInt(b))) % (ord(valid_chars[-1]) - ord(valid_chars[0])))

key = "Key!"

def shift(text, key, shiftFunction) -> str:
	encrypted = ""
	idx = 0
	keyLen = len(key)

	for char in text:
		if char in valid_chars:
			keyLetter = key[idx]
			newChar = shiftFunction(char, keyLetter)
			idx += 1
			idx = idx%keyLen
			encrypted += newChar
		else:
			encrypted += char

	return encrypted

def encrypt(plaintext) -> str:
    return shift(plaintext, key, add_char)

def decrypt(ciphertext) -> str:
    return shift(ciphertext, key, subtract_char)

def get_hash(password) -> str:
    byte_pass = bytes(password, "UTF-8")
    return hashlib.sha256(byte_pass).hexdigest()

if __name__ == "__main__":
    print("Hashing")
    print(get_hash("Password321") == get_hash("Password321"))
    print(get_hash("Bedug321!"))
    print(get_hash("Admin321!"))
    print(get_hash(""))
    print(get_hash("!@#)(!)(@#)U*!@"))
    
    print("encrypting")
    print(encrypt("bruh123!@# []"))
    print(decrypt(encrypt("Test123!@# []")))
    print(decrypt(encrypt("Test123!@# []")) == "Test123!@# []")
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def encrypt_message(message):
    # Generate RSA keys
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    
    # Serialize keys to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Convert keys to hexadecimal
    private_key_hex = private_key_pem.hex()
    public_key_hex = public_key_pem.hex()
    
    # Encrypt the message with the public key
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Convert ciphertext to hexadecimal
    ciphertext_hex = ciphertext.hex()
    
    return ciphertext_hex, public_key_hex, private_key_hex

def decrypt_message(ciphertext_hex, private_key_hex):
    private_key_pem = bytes.fromhex(private_key_hex)
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    
    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted_message = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return decrypted_message.decode('utf-8')

# # Example usage
# message = "Hello, World!"
# ciphertext_hex, public_key_hex, private_key_hex = encrypt_message(message)

# print("Private Key (hex):")
# print(private_key_hex)

# print("Public Key (hex):")
# print(public_key_hex)

# print("Encrypted message (hex):", ciphertext_hex)

# # Decrypt the message
# decrypted_message = decrypt_message(ciphertext_hex, private_key_hex)
# print("Decrypted message:", decrypted_message)

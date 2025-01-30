import secrets

def generate_secret_key():
    # Generate a secure 64-character hexadecimal key (32 bytes)
    return secrets.token_hex(32)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    jwt_secret_key = generate_secret_key()
    
    print(f"SECRET_KEY: {secret_key}")
    print(f"JWT_SECRET_KEY: {jwt_secret_key}")

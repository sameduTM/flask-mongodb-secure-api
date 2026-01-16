import jwt
import datetime

SECRET = "my_super_secret_key"


# create a token
def create_token():
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "admin": True,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=5),
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256", headers=header)
    return token


# Decode without verifying
def decode_token(token):
    return jwt.decode(token, options={"verify_signature": False})


# Verify with secret
def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid Token"


if __name__ == "__main__":
    token = create_token()
    print("Generated JWT:\n", token)

    print("\nDecoded (no signature check):")
    print(decode_token(token))

    print("\nVerified token:")
    print(verify_token(token))

    # Tampering test
    parts = token.split(".")
    tampered_payload = parts[1][:-1] + ("A" if parts[1][-1] != "A" else "B")
    tampered = parts[0] + "." + tampered_payload + "." + parts[2]
    print("\nTampered token:")
    print(tampered)

    print("\nVerification of tampered token:")
    print(verify_token(tampered))
    
    b'email=jane@doe.com'.decode()

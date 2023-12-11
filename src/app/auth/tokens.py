import jwt
import datetime

def create_token(user, secret, authz: bool) -> str:
    token = jwt.encode(
        {
            "user": user,
            "exp": (datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=45)).isoformat(),
            "issuedat": datetime.datetime.utcnow().isoformat(),
            "admin": authz
        },
        secret,
        algorithm="HS256",
    )

    return token

def decode_token(encoded_token: str, secret: str):
        decoded = jwt.decode(encoded_token, secret, algorithms=["HS256"])
        return decoded
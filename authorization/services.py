import jwt
from datetime import datetime, timedelta


def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id'] 
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None 

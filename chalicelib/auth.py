import jwt
import datetime
from chalice import UnauthorizedError, UnauthorizedError

SECRET_KEY = 'sua_chave_secreta'

class AuthService:
    @staticmethod
    def generate_token(username):
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload['username']
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token expirado.")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Token inválido.")


# Classe para centralizar lógica da API
class APIService:
    def __init__(self):
        self.auth_service = AuthService()

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise UnauthorizedError("Autenticação necessária.")
        token = auth_header.split(" ")[1]
        return self.auth_service.verify_token(token)
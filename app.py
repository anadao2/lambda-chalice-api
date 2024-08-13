from chalice import Chalice, Response
from chalicelib.auth import APIService

app = Chalice(app_name='myapi')

# Instância da API Service
api_service = APIService()

@app.route('/generate-token', methods=['POST'])
def generate_token():
    request = app.current_request
    body = request.json_body
    username = body.get('username')

    if not username:
        return Response(body={'error': 'Usuário é necessário.'}, status_code=400)

    token = api_service.auth_service.generate_token(username)
    return {'token': token}

@app.route('/protected', methods=['GET'])
def protected():
    request = app.current_request
    username = api_service.authenticate(request)
    return {'message': f'Bem-vindo, {username}!'}

@app.route('/public', methods=['GET'])
def public():
    return {'message': 'Esta é uma rota pública.'}


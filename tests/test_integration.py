import json
from chalice.test import Client
import pytest
from app import app

@pytest.fixture
def client():
    with Client(app) as client:
        yield client

class TestAPI:
    def test_generate_token(self, client):
        request_body = json.dumps({'username': 'testuser'})
        response = client.http.post(
            '/generate-token', 
            body=request_body,
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 200
        assert 'token' in response.json_body

    def test_protected_route_with_valid_token(self, client):
        # Gera um token válido
        token_response = client.http.post(
            '/generate-token', 
            body=json.dumps({'username': 'testuser'}),
            headers={'Content-Type': 'application/json'}
        )
        
        token = token_response.json_body['token']
        
        # Acessa a rota protegida com o token
        response = client.http.get('/protected', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        body = response.json_body
        assert body['message'] == 'Bem-vindo, testuser!'

    def test_public_route(self, client):
        response = client.http.get('/public')
        assert response.status_code == 200
        body = response.json_body
        assert body == {'message': 'Esta é uma rota pública.'}

    def test_protected_route_with_invalid_token(self, client):
        # Acessa a rota protegida com um token inválido
        response = client.http.get('/protected', headers={'Authorization': 'Bearer invalid_token'})
        assert response.status_code == 401
        body = response.json_body
        assert body == {'Code': 'UnauthorizedError', 'Message': 'Token inválido.'}

    def test_protected_route_without_token(self, client):
        # Acessa a rota protegida sem fornecer um token
        response = client.http.get('/protected')
        assert response.status_code == 401
        body = response.json_body
        assert body == {'Code': 'UnauthorizedError', 'Message': 'Autenticação necessária.'}

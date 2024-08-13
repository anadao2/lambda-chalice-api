import pytest
from chalice.test import Client
from app import app

@pytest.fixture
def client():
    with Client(app) as client:
        yield client

def test_generate_token(client):
    response = client.http.post('/generate-token', json_body={'username': 'testuser'})
    assert response.status_code == 200
    body = response.json_body
    assert 'token' in body

def test_protected_route_with_valid_token(client):
    # Gera um token válido
    token_response = client.http.post('/generate-token', json_body={'username': 'testuser'})
    token = token_response.json_body['token']
    
    # Acessa a rota protegida com o token
    response = client.http.get('/protected', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    body = response.json_body
    assert body['message'] == 'Bem-vindo, testuser!'

def test_protected_route_with_invalid_token(client):
    # Acessa a rota protegida com um token inválido
    response = client.http.get('/protected', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    body = response.json_body
    assert 'Token inválido' in body['Code']

def test_protected_route_without_token(client):
    # Acessa a rota protegida sem fornecer um token
    response = client.http.get('/protected')
    assert response.status_code == 401
    body = response.json_body
    assert 'Autenticação necessária' in body['Code']

def test_public_route(client):
    response = client.http.get('/public')
    assert response.status_code == 200
    body = response.json_body
    assert body['message'] == 'Esta é uma rota pública.'

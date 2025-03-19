"""
Test suite for WebChat application
"""
import pytest
from flask import Flask
from unittest.mock import Mock, patch
import json
from WebChat import WebChat, ChatConfig

@pytest.fixture
def app():
    """Create a test Flask application"""
    config = ChatConfig(debug=True, api_key="test_key")
    webchat = WebChat(config)
    return webchat.app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

def test_send_data_without_api_key(client):
    """Test that requests without API key are rejected"""
    response = client.post('/send', 
                         json={'data': 'test query'},
                         headers={})
    assert response.status_code == 401
    assert b'Invalid API key' in response.data

def test_send_data_with_api_key(client):
    """Test that requests with valid API key are accepted"""
    response = client.post('/send',
                         json={'data': 'test query'},
                         headers={'X-API-Key': 'test_key'})
    assert response.status_code == 200
    assert b'Processing your query' in response.data

def test_send_data_invalid_query(client):
    """Test that invalid queries are rejected"""
    # Test empty query
    response = client.post('/send',
                         json={'data': ''},
                         headers={'X-API-Key': 'test_key'})
    assert response.status_code == 400
    
    # Test query with XSS attempt
    response = client.post('/send',
                         json={'data': '<script>alert("xss")</script>'},
                         headers={'X-API-Key': 'test_key'})
    assert response.status_code == 400

def test_get_settings_without_api_key(client):
    """Test that settings endpoint requires API key"""
    response = client.get('/settings')
    assert response.status_code == 401

def test_get_settings_with_api_key(client):
    """Test that settings endpoint works with valid API key"""
    response = client.get('/settings',
                         headers={'X-API-Key': 'test_key'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_select_item_without_api_key(client):
    """Test that select endpoint requires API key"""
    response = client.post('/select',
                         json={'id': 1})
    assert response.status_code == 401

def test_select_item_with_api_key(client):
    """Test that select endpoint works with valid API key"""
    response = client.post('/select',
                         json={'id': 1},
                         headers={'X-API-Key': 'test_key'})
    assert response.status_code == 200
    assert b'Selected item with id 1' in response.data

def test_select_item_invalid_id(client):
    """Test that select endpoint handles invalid IDs"""
    response = client.post('/select',
                         json={'id': None},
                         headers={'X-API-Key': 'test_key'})
    assert response.status_code == 400

@patch('WebChat.LlmThread')
def test_start_llm_thread(mock_llm_thread):
    """Test LLM thread initialization"""
    config = ChatConfig()
    webchat = WebChat(config)
    webchat.start_llm_thread("test-model")
    mock_llm_thread.assert_called_once_with("test-model", "You are a helpful assistant")

def test_security_headers(client):
    """Test that security headers are present in responses"""
    response = client.get('/settings',
                         headers={'X-API-Key': 'test_key'})
    headers = response.headers
    assert headers['X-Content-Type-Options'] == 'nosniff'
    assert headers['X-Frame-Options'] == 'DENY'
    assert headers['X-XSS-Protection'] == '1; mode=block'
    assert 'Strict-Transport-Security' in headers
    assert 'Content-Security-Policy' in headers

def test_rate_limiting(client):
    """Test rate limiting functionality"""
    headers = {'X-API-Key': 'test_key'}
    # Make multiple requests quickly
    for _ in range(11):  # Should hit the 10 per minute limit
        client.post('/send',
                   json={'data': 'test query'},
                   headers=headers)
    
    # The last request should be rate limited
    response = client.post('/send',
                         json={'data': 'test query'},
                         headers=headers)
    assert response.status_code == 429
    assert b'Rate limit exceeded' in response.data 
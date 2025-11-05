# cursor_test.py


def validate_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'No authorization header'}), 401
    
    try:
        # Extract token from "Bearer <token>"
        token = auth_header.split(' ')[1]
        
        # Verify and decode the JWT token
        # Note: You'll need to replace 'your-secret-key' with your actual secret key
        payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
        
        # Token is valid, you can access claims like:
        # user_id = payload.get('user_id')
        return jsonify({'message': 'Token is valid', 'user': payload}), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

# Decorator for routes that require token validation
def token_required(f):
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
            
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
            # Add the decoded payload to the request context
            request.user = payload
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
    return decorated

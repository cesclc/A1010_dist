""" 
WebChat.py - Chatbot from chat03.py, plus Angular Web UI
"""
import json
import logging
from flask import Flask, jsonify, request, Response
import time
from flask_cors import CORS
import threading
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import secrets
import re

from llms.llm_thread import LlmThread
from llms.llm_thread import Llm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('webchat.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ChatConfig:
    """Configuration for the chat application"""
    version: str = "1.01"
    allowed_origins: list = None
    port: int = 8000
    debug: bool = False
    model: str = "anthropic:claude-3-5-sonnet-20241022"
    rate_limit: str = "100 per minute"  # Default rate limit
    max_query_length: int = 1000  # Maximum length of query in characters
    api_key: str = None  # API key for authentication
    
    def __post_init__(self):
        if self.allowed_origins is None:
            self.allowed_origins = ["http://localhost:4200", "http://localhost:4201"]
        if self.api_key is None:
            self.api_key = secrets.token_urlsafe(32)

class WebChat:
    def __init__(self, config: Optional[ChatConfig] = None):
        self.config = config or ChatConfig()
        self.app = Flask(__name__)
        
        # Configure CORS with specific origins
        CORS(self.app, 
             resources={r"/*": {"origins": self.config.allowed_origins}},
             supports_credentials=True,
             max_age=3600)
        
        # Configure rate limiting
        self.limiter = Limiter(
            app=self.app,
            key_func=get_remote_address,
            default_limits=[self.config.rate_limit]
        )
        
        self.platform = None  # LLM family
        self.model = ""  # LLM Model
        self.cost = 0
        self.llm = None
        self.messages = []
        self.llm_thread = None
        self.die = threading.Event()
        self.data_list = [  # Demo data...
            {"id": 1, "name": "Item 1", "value": 10},
            {"id": 2, "name": "Item 2", "value": 20},
            {"id": 3, "name": "Item 3", "value": 30},
        ]
        self.query = ""
        self.credit = 100  # Mock credit value
        
        self.configure_routes()
        self._setup_error_handlers()
        self._setup_security_headers()

    def _setup_security_headers(self):
        """Setup security headers for all responses"""
        @self.app.after_request
        def add_security_headers(response):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['Content-Security-Policy'] = "default-src 'self'"
            return response

    def _validate_query(self, query: str) -> bool:
        """Validate the query for security and length"""
        if not query or len(query) > self.config.max_query_length:
            return False
            
        # Basic XSS prevention
        if re.search(r'<[^>]*>', query):
            return False
            
        return True

    def _require_api_key(self, f):
        """Decorator to require API key authentication"""
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            if not api_key or api_key != self.config.api_key:
                return jsonify({"error": "Invalid API key"}), 401
            return f(*args, **kwargs)
        return decorated_function

    def _setup_error_handlers(self):
        """Setup error handlers for the Flask application"""
        @self.app.errorhandler(400)
        def bad_request(error):
            logger.error(f"Bad request: {error}")
            return jsonify({"error": "Bad request", "message": str(error)}), 400

        @self.app.errorhandler(401)
        def unauthorized(error):
            logger.error(f"Unauthorized: {error}")
            return jsonify({"error": "Unauthorized", "message": "Invalid API key"}), 401

        @self.app.errorhandler(404)
        def not_found(error):
            logger.error(f"Not found: {error}")
            return jsonify({"error": "Not found", "message": str(error)}), 404

        @self.app.errorhandler(429)
        def too_many_requests(error):
            logger.error(f"Rate limit exceeded: {error}")
            return jsonify({"error": "Too many requests", "message": "Rate limit exceeded"}), 429

        @self.app.errorhandler(500)
        def internal_error(error):
            logger.error(f"Internal server error: {error}")
            return jsonify({"error": "Internal server error", "message": str(error)}), 500

    def configure_routes(self):
        """Configure routes for the Flask application"""
        @self.app.route('/send', methods=['POST'])
        @self.limiter.limit("10 per minute")  # Stricter rate limit for send endpoint
        @self._require_api_key
        def send_data():
            try:
                data = request.json.get('data')
                if not data:
                    raise ValueError("No data provided in request")
                    
                if not self._validate_query(data):
                    raise ValueError("Invalid query format or length")
                    
                self.query = data
                logger.info(f"Received query: {data}")
                
                if not self.llm_thread:
                    raise RuntimeError("LLM thread not initialized")
                    
                self.llm_thread.set_query(self.query)
                return jsonify({"reply": f"Processing your query: {self.query}"})
                
            except Exception as e:
                logger.error(f"Error processing send request: {str(e)}", exc_info=True)
                return jsonify({"error": str(e)}), 400

        @self.app.route('/settings', methods=['GET'])
        @self._require_api_key
        def get_settings():
            try:
                return jsonify(self.data_list)
            except Exception as e:
                logger.error(f"Error getting settings: {str(e)}", exc_info=True)
                return jsonify({"error": str(e)}), 500

        @self.app.route('/select', methods=['POST'])
        @self._require_api_key
        def select_item():
            try:
                item_id = request.json.get('id')
                if not item_id:
                    raise ValueError("No item ID provided")
                    
                logger.info(f"Selected item with id: {item_id}")
                return jsonify({"message": f"Selected item with id {item_id}"})
                
            except Exception as e:
                logger.error(f"Error processing select request: {str(e)}", exc_info=True)
                return jsonify({"error": str(e)}), 400

        @self.app.route('/stream', methods=['GET'])
        @self._require_api_key
        def stream():
            def stream_data():
                try:
                    while not self.die.is_set():
                        resp = self.llm_thread.read_response()
                        if (not isinstance(resp, str)) and resp == self.llm_thread.END_OF_REPLY_QUEUE:
                            logger.debug("Closing event stream")
                            yield f"event: close\ndata: {json.dumps({'type': 'close'})}\n\n"
                        else:
                            logger.debug(f"Streaming response: {resp}")
                            yield resp
                except Exception as e:
                    logger.error(f"Error in stream_data: {str(e)}", exc_info=True)
                    yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

            return Response(
                stream_data(),
                content_type='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive'
                }
            )

        @self.app.route('/status', methods=['GET'])
        @self._require_api_key
        def status():
            def generate():
                try:
                    while True:
                        time.sleep(5)
                        yield f"data:{self.credit}\n\n"
                except Exception as e:
                    logger.error(f"Error in status stream: {str(e)}", exc_info=True)
                    yield f"data:error:{str(e)}\n\n"
                    
            return Response(generate(), mimetype='text/event-stream')

    def start_llm_thread(self, pmodel: str):
        """Start the LLM thread with the specified model"""
        try:
            logger.info(f"Starting LLM thread with model: {pmodel}")
            self.llm_thread = LlmThread(pmodel, "You are a helpful assistant")
        except Exception as e:
            logger.error(f"Error starting LLM thread: {str(e)}", exc_info=True)
            raise

    def stop_llm_thread(self):
        """Stop the LLM thread"""
        try:
            if self.llm_thread:
                logger.info("Stopping LLM thread")
                self.llm_thread.stop()
        except Exception as e:
            logger.error(f"Error stopping LLM thread: {str(e)}", exc_info=True)
            raise

if __name__ == '__main__':
    try:
        config = ChatConfig()
        wc = WebChat(config)
        logger.info(f"Starting SMArt app V{WebChat.version} with LLMs V{Llm.version}")
        logger.info(f"API Key: {config.api_key}")  # Log API key for development
        wc.start_llm_thread(config.model)
        wc.app.run(debug=config.debug, port=config.port)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        wc.stop_llm_thread()




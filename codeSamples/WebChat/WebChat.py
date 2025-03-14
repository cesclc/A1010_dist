""" 
WebChat.py - Chatbot from chat03.py, plus Angular Web UI
"""
import json
import logging
from flask import Flask, jsonify, request, Response
import time
from flask_cors import CORS
import threading

from llms.llm_thread import LlmThread
from llms.llm_thread import Llm


class WebChat:
    version = "1.01"

    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": ["http://localhost:4200", "http://localhost:4201"]}})
        #  ^^ **MB 2 items to show array syntax
        logging.basicConfig(level=logging.DEBUG)  # Or .INFO
        self.LOG = logging.getLogger(__name__)
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
        self.query = "a"
        self.credit = 100  # Mock credit value
        self.configure_routes()

    def configure_routes(self):
        """**MB Decided to use a class, with Flask this makes handlers weird, they need to be methods within this method
        Or for large methods, in here just do call to self.detailed_impl()"""
        @self.app.route('/send', methods=['POST'])
        def send_data():  # Note can't pass `self` here (!!)
            data = request.json.get('data')
            self.query = data
            self.LOG.info(f"Received data: {data}, have set query to:{self.query}")
            response = {"reply": f"Running your query: {self.query}"}
            self.llm_thread.set_query(self.query)
            return jsonify(response)

        @self.app.route('/settings', methods=['GET'])
        def get_settings():
            return jsonify(self.data_list)

        @self.app.route('/select', methods=['POST'])
        def select_item():
            item_id = request.json.get('id')
            # Process the selected item
            response = {"message": f"Selected item with id {item_id}"}
            return jsonify(response)

        @self.app.route('/stream', methods=['GET'])
        def stream():
            def stream_data():
                while not self.die.is_set():
                    resp = self.llm_thread.read_response()
                    if (not isinstance(resp, str)) and resp == self.llm_thread.END_OF_REPLY_QUEUE:
                        self.LOG.debug("In stream_data) - Closing event stream")
                        yield f"event: close\ndata: {json.dumps({'type': 'close'})}\n\n"
                    else:
                        self.LOG.debug("In stream_data() - resp = " + resp)
                        yield resp
                # Dead code, but keep as example / doco:
                # 2. test data based on caller's POST
                # s = "Result of your Query : " + self.query + " : is being cooked for you right now and is . . . . now DONE!"
                # for word in s.split():
                #     time.sleep(0.2)  # Seconds
                #     hms = datetime.now().strftime('%H:%M:%S')
                #     yield f"{word}\n"  # Need trailing \n for curl-testing to work
                # 1. Simple test data:
                # for i in range(10):
                #     time.sleep(0.2)  # Seconds
                #     yield f"data:{self.query}:{i} at {hms}\n"

            return Response(stream_data(),
                content_type='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive'
                })

        @self.app.route('/status', methods=['GET'])
        def status():
            def generate():
                while True:
                    time.sleep(5)
                    yield f"data:{self.credit}\n\n"
            return Response(generate(), mimetype='text/event-stream')
    # ( end of configure_routes() )

    def start_llm_thread(self, pmodel):
        self.llm_thread = LlmThread(pmodel, "You are a helpful assistant")  # Creates and starts thread for LLM operations

    def stop_llm_thread(self):
        self.llm_thread.stop()


if __name__ == '__main__':
    wc = WebChat()
    wc.LOG.info("Starting SMArt app V%s with LLMs V%s", WebChat.version, Llm.version)
    pmodel = "anthropic:claude-3-5-sonnet-20241022"
    wc.start_llm_thread(pmodel)
    wc.app.run(debug=True, port=8000)  # With IPV6, port 5000 conflicts with Mac ControlCentre (!!) so use 8000
    wc.stop_llm_thread()




import logging
import threading
from queue import Queue

from llms.llm import Llm


class LlmThread():
    def __init__(self, pmodel, sysprompt):
        self.pmodel = pmodel
        self.model = ""
        self.sysprompt = sysprompt
        self.messages = None
        self.llm = None
        self.lock = threading.Lock()
        self.die = threading.Event()
        self.query_queue = Queue()
        self.reply_queue = Queue()
        self.END_OF_REPLY_QUEUE = object()  # Unique sentinel object

        logging.basicConfig(level=logging.DEBUG)  # Or .INFO
        self.LOG = logging.getLogger(__name__)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def theLlm(self, platform_=""):  # Sort of singleton method, when need llm inst vbl in case not created yet
            # ^ Pass a value into platform_ to force re-creation of llm inst vbl, using that platform
            if platform_ != "":
                self.platform = platform_
                self.llm = None  # Force re-create below
            if self.llm is None:
                self.llm = Llm.create_platform(self.platform)
            return self.llm

    def start(self):
        self.thread.start()

    def stop(self):
        self.die.set()
        self.thread.join()

    def set_query(self, qry):
        self.query_queue.put(qry)

    def read_response(self):
        """Read 1 item from response Q / stream"""
        resp = self.reply_queue.get()
        return resp

    def write_reply(self, resp):
        """Write an item to response Q / stream"""
        self.reply_queue.put(resp)

    def close_reply(self):
        self.reply_queue.put(self.END_OF_REPLY_QUEUE)  # Send end-sentinel

    def run(self):
        self.new_session(self.pmodel, self.sysprompt)
        while (not self.die.is_set()):
            query = self.query_queue.get()
            self.messages.append({'role': 'user', 'content': query})
            self.LOG.info("llm thr rx: " + query)
            res = self.theLlm().invoke(self.messages, self.write_reply, self.close_reply)
            # Here is too early: self.close_reply()

    def new_session(self, platform_and_model, sysprompt):
        """eg anthropic:claude-3-5-sonnet-20241022"""
        # self.LOG.info("zzzz DBG: " + platform_and_model)  # DIAG
        pm = platform_and_model.split(":")
        self.new_session_pm(pm[0], pm[1], sysprompt)

    def new_session_pm(self, platform_, model_, sysprompt):
        self.theLlm(platform_).create_client(model_)
        # ^Pass platform_ to theLlm() to force recreation of `llm` instance vbl, using that platform
        self.model = model_
        self.LOG.info("Starting new session with %s:%s  Cost$ %s per mn in/out tokens  Ctxw: %sk",
                      platform_, model_, self.llm.scosts, (self.llm.ctxw_remain / 1024))
        self.messages = [
            {'role': 'system', 'content': sysprompt}
        ]


"""
llama_llm.py - LlamaLlm class , for accessing different Llama LLMs
NOTE LlamaAPI can also accept OpenAI API format, by adding base_url param eg:
client = OpenAI(
api_key = "<your_llamaapi_token>",
base_url = "https://api.llama-api.com"
)

See:
  https://www.llama-api.com
  https://docs.llamaindex.ai/en/stable/examples/llm/openllm/
  https://www.llama.com/docs/get-started/
"""
import os
import time
import traceback
from datetime import datetime


from .llm import Llm
from llamaapi import LlamaAPI


class LlamaLlm(Llm):
    platform = "llama"
    # Context window size no of IN+OUT tokens:
    """They were not listed, depends on deployment, RAM, etc  
        Perplexity estimated them as below  
        Where not known I estimated at 7k, as a conservative and unusual number.
        Likewise for Qwen I think they're 32k, so put 33k as an estimate below.
    """
    # MANY Qwen models listed on LlamaAPI site aren't valid, see (deleted) or commented out below,
    #  maybe use HuggingFace for them instead, see https://huggingface.co/Qwen/Qwen2-7B-Instruct
    #  LlamaAPI site says has Qwen models:  Qwen1.5-72B-Chat ( replace 72B with 110B / 32B / 14B / 7B / 4B / 1.8B / 0.5B)
    ctxw_sizes = {'llama3.2-11b-vision': '32k', 'llama3.2-1b': '8k', 'llama3.2-3b': '8k', 'llama3.2-90b-vision': '64k',
        'llama3.1-405b': '128k',
        'llama3.1-70b': '64k', 'llama3.1-8b': '32k', 'llama3-70b': '64k', 'llama3-8b': '32k',
        'llama2-13b': '7k', 'llama2-70b': '7k', 'llama2-7b': '7k',
        'gemma2-27b': '7k', 'gemma2-9b': '7k',
        'mixtral-8x22b-instruct': '32k', 'mixtral-8x7b-instruct': '32k',
        # 'mistral-7b-instruct': '32k',  # Removed, see costper below
        'Nous-Hermes-2-Mixtral-8x7B-DPO': '32k',
        # 'Nous-Hermes-2-Yi-34B': '32k',   # Removed, see costper below
        # 'Qwen/Qwen2-72B-Instruct': '128k',  # Try
        # 'Qwen2-72B': '128k',
        # 'Qwen2-72B-chat': '128k',  # Try
        # 'Qwen2-72B-instruct': '128k',  # Try
        # 'Qwen2.5-72B': '128k',
        # 'Qwen1.5-1.8B-Chat': '32k',   #
        # 'Qwen1.5-110B-Chat': '33k',
        # 'Qwen1.5-14B-Chat': '33k',
        # 'Qwen1.5-32B-Chat': '33k',
        # 'Qwen1.5-4B-Chat': '33k',
        # 'Qwen1.5-72B-Chat': '128k',
        # 'Qwen1.5-7B-Chat': '128k',
        # 'Qwen2-72B-Instruct': '128k'
                  }
    # Cost per million tokens In/Out
    costper = {'llama3.2-11b-vision': '0.4/0.4', 'llama3.2-1b': '0.4/0.4', 'llama3.2-3b': '0.4/0.4',
        'llama3.2-90b-vision': '2.8 / 2.8',
        'llama3.1-405b': '3.6/3.6', 'llama3.1-70b': '2.8/2.8',
        'llama3.1-8b': '0.4/0.4', 'llama3-70b': '2.8/2.8', 'llama3-8b': '0.4/0.4',
        'llama2-13b': '1.6/1.6', 'llama2-70b': '2.8/2.8', 'llama2-7b': '1.6/1.6',
        'gemma2-27b': '1.6/1.6', 'gemma2-9b': '0.4/0.4',
        'mixtral-8x22b-instruct': '2.8/2.8', 'mixtral-8x7b-instruct': '2.8/2.8',
        # 'mistral-7b-instruct': '0.4/0.4',  # mistral-7b-instruct replied "failed to process your request"
        'Nous-Hermes-2-Mixtral-8x7B-DPO': '0.4/0.4',
        # 'Nous-Hermes-2-Yi-34B': '2.8/2.8',  # Remove, it replied "failed to process your request"
        # 'Qwen/Qwen2-72B-Instruct': '.00038/.0004',  # Try
        # 'Qwen2-72B': '.00038/.0004',
        # 'Qwen2-72B-chat': '.00038/.0004',  # Try
        # 'Qwen2-72B-instruct': '.00038/.0004',  # Try
        # 'Qwen2.5-72B': '.00038/.0004',
        #  'Qwen1.5-1.8B-Chat': '0.4/0.4',
        # 'Qwen1.5-110B-Chat': '2.8/2.8',
        # 'Qwen1.5-14B-Chat': '1.6/1.6',
        # 'Qwen1.5-32B-Chat': '2.8/2.8',
        # 'Qwen1.5-4B-Chat': '0.4/0.4',
        # 'Qwen1.5-72B-Chat': '2.8/2.8',
        # 'Qwen1.5-7B-Chat': '0.4/0.4',
        # 'Qwen2-72B-Instruct': '2.8/2.8'
               }

    def __init__(self):  # Allow no-arg ctor so that callers can use Llm before knowing which platfomr:model they want
        super().__init__(self.platform)

    @classmethod
    def list_models(cls):
        return list(cls.costper.keys())

    def list_models_aspy(self, prefix_model=True):
        """Get a list of models for this platform, as Python code for editing"""
        pass

    def create_client(self, model_):
        self.init_client(model_, self.ctxw_sizes[model_], self.costper[model_])  # Init costs etc
        self.client = LlamaAPI(os.environ.get("LLAMA_API_KEY"))
        # TODO try using OpenAI API, see comment at top, and see if token stats are returned in the same way

    def invoke(self, messages):  # TODO Maybe delegate to super for common / repeated API forms
        try:
            api_request_json = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 2048,  # **M014b Llama models default to low, useless value.
            }
            millis0 = round(time.time() * 1000)
            response = self.client.run(api_request_json)
            self.millis = round(time.time() * 1000) - millis0
            if "error" in response.text:
                # TODO log the response.txt, fnow show in TT: eg during tests:
                tnow = datetime.now().strftime("%y%m%d_%H%M")
                print("Unexpected response containing 'error' : " + response.text)
                return f"(AI Error see log at {tnow})"  # TODO is that a suitable thing to return?
            completion = response.json()
            # response.text = {"created":1731522190,"model":"llama3.1-70b","usage":{"prompt_tokens":38,"completion_tokens":22,"total_tokens":60},"choices":[{"finish_reason":"stop","index":0,"logprobs":null,"message":{"content":"Hello","refusal":null,"role":"assistant","function_call":null,"tool_calls":null}}]}
            res = completion['choices'][0]['message']['content']
            self.update_cost_and_context(completion)
        except Exception as e:
            # **M014 for occasions when LLM throws exep, return brief msg maybe will get to user, just datim so we can check logs..
            tnow = datetime.now().strftime("%y%m%d_%H%M")
            msg = f"(error at {tnow})"
            traceback.print_exc()  # TODO Log!!
            print(msg)  # TODO Log!!
            return msg
        return res

    def update_cost_and_context(self, completion) -> float:
        itk = completion['usage']['prompt_tokens']
        otk = completion['usage']['completion_tokens']
        icost = itk * self.cost_per_intoken
        ocost = otk * self.cost_per_outtoken
        self.tkns = itk + otk
        self.ctxw_remain -= self.tkns
        self.cumulative_cost += icost + ocost  # **M014 Store in instance vbl so tests can access it
        self.last_cost = icost + ocost
        return self.last_cost

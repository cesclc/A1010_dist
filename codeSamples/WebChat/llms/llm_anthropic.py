"""
mistral_llm.py - AnthropicLlm class , for accessing different Anthropic LLMs
"""
import os
import time
import traceback
from datetime import datetime


from .llm import Llm
from openai import OpenAI
from anthropic import Anthropic


class AnthropicLlm(Llm):
    platform = "anthropic"
    # We DO need the snapshot date, for consistency -latest is not recomended
    # Context window size no of IN+OUT tokens:
    ctxw_sizes = {'claude-3-5-sonnet-20241022': '200k',
                  'claude-3-5-haiku-20241022': '200k',
                  'claude-3-opus-20240229': '200k',
                  'claude-3-sonnet-20240229': '200k',
                  'claude-3-haiku-20240307': '200k'}
    costper = {'claude-3-5-sonnet-20241022': '.003/.015',
               'claude-3-5-haiku-20241022': '.001/.005',
               'claude-3-opus-20240229': '.015/.075',
               'claude-3-sonnet-20240229': '.003/.015',
               'claude-3-haiku-20240307': '.00025/.00125'}
    def __init__(self):  # Allow no-arg ctor so that callers can use Llm before knowing which platfomr:model they want
        super().__init__(self.platform)

    @classmethod
    def list_models(cls):
        return list(cls.costper.keys())

    def create_client(self, model_):
        self.init_client(model_, self.ctxw_sizes[model_], self.costper[model_])  # Init costs etc
        self.client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def invoke(self, messages, streamer_func=None, stream_closer_func=None):  # TODO Maybe delegate to super for common / repeated API forms
        """NOTE we need to pass system prompt separatley! See "eg, to pass `system` message: " below
        else it gives err:
         anthropic.BadRequestError: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'messages: Unexpected role "system". The Messages API accepts a top-level `system` parameter, not "system" as an input message role.'}}
        """
        if (streamer_func):
            return self.invoke_streaming(messages, streamer_func, stream_closer_func)

        try:
            sysprompt = None
            (sysprompt, msgs) = self.extract_sysprompt(messages)
            if len(msgs) == 0:
                msgs.append({'role': 'user', 'content': sysprompt})  # API needs at least 1 (user) message
            millis0 = round(time.time() * 1000)
            completion = self.client.messages.create(
                model=self.model,
                max_tokens=4000,  # Anthropic models DO need this, and cant be > their max of 4096
                system=sysprompt,
                messages=msgs
            )
            self.millis = round(time.time() * 1000) - millis0
            res = completion.content[0].text
            self.update_cost_and_context(completion)
        except Exception as e:
            # **M014 for occasions when LLM throws exep, return brief msg maybe will get to user, just datim so we can check logs..
            tnow = datetime.now().strftime("%y%m%d_%H%M")
            msg = f"(error at {tnow})"
            traceback.print_exc()  # TODO Log!!
            print(msg)  # TODO Log!!
            return msg
        return res

    def invoke_streaming(self, messages, streamer_func, stream_closer_func):
        (sysprompt, non_sys_msgs) = self.extract_sysprompt(messages)
        res = ""
        with self.client.messages.stream(
            model=self.model,
            max_tokens=4000,  # Anthropic models DO need this, and cant be > their max of 4096
            system=sysprompt,
            messages=non_sys_msgs
        ) as stream:
            for chunk in stream.text_stream:
                print(chunk)  # DBG , maybe add:  , end="", flush=True
                streamer_func(chunk)
                res += chunk
            self.update_cost_and_context(stream.current_message_snapshot)
            stream_closer_func()
        return res

    def extract_sysprompt(self, messages):
        sysprompt = ""
        newmsgs= []
        for msg in messages:
            if msg['role'] == 'system':
                if sysprompt != "":
                    raise ValueError("Got >1 role:system messages!")
                sysprompt = msg['content']
            else:
                newmsgs.append(msg)
        return (sysprompt, newmsgs)

    def update_cost_and_context(self, completion) -> float:
        itk = completion.usage.input_tokens
        otk = completion.usage.output_tokens
        icost = itk * self.cost_per_intoken
        ocost = otk * self.cost_per_outtoken
        self.tkns = itk + otk
        self.ctxw_remain -= self.tkns
        self.cumulative_cost += icost + ocost  # **M014 Store in instance vbl so tests can access it
        self.last_cost = icost + ocost
        return self.last_cost

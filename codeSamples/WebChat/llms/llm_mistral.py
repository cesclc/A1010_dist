"""
mistral_llm.py - MistralLlm class , for accessing different Mistral LLMs
Mistral LLMs (some?) are also available on bedrock & IBM watsonx.ai
"""
from datetime import datetime
import os
import time
import traceback

from .llm import Llm
from mistralai import Mistral


class MistralLlm(Llm):
    platform = "mistral"
    # Context window size no of IN+OUT tokens:
    ctxw_sizes = {'ministral-3b-latest': '128k',
                  'ministral-8b-latest': '128k',
                  'mistral-large-latest': '128k',
                  'mistral-small-latest': '32k',
                  'codestral-latest': '32k',
                  'mistral-embed': '8k',
                  'mistral-moderation-latest': '8k',
                  'pixtral-12b-2409': '128k',
                  'open-mistral-nemo': '128k',
                  'open-codestral-mamba': '256k',
                  'open-mistral-7b': '32k',
                  'open-mixtral-8x7b': '32k',
                  'open-mixtral-8x22b': '64k'}
    costper = {'ministral-3b-latest': '.00004/.00004',
               'ministral-8b-latest': '.0001/.0001',
               'mistral-large-latest': '.002/.006',
               'mistral-small-latest': '.0002/.0006',
               'codestral-latest': '.0002/.0006',
               'mistral-embed': '.0001/0',
               'mistral-moderation-latest': '.0001/0',
               'pixtral-12b-2409': '.00015/.00015',
               'open-mistral-nemo': '.00015/.00015',
               'open-codestral-mamba': '.00015/.00015',
               'open-mistral-7b': '.00025/.00025',
               'open-mixtral-8x7b': '.0007/.0007',
               'open-mixtral-8x22b': '.002/.006'}

    def __init__(self):  # Allow no-arg ctor so that callers can use Llm before knowing which platfomr:model they want
        super().__init__(self.platform)

    @classmethod
    def list_models(cls):
        return list(cls.costper.keys())

    def create_client(self, model_):
        self.init_client(model_, self.ctxw_sizes[model_], self.costper[model_])  # Init costs etc
        self.client = Mistral(os.environ["MISTRAL_API_KEY"])

    def invoke(self, messages):  # TODO Maybe delegate to super for common / repeated API forms
        try:
            millis0 = round(time.time() * 1000)
            completion = self.client.chat.complete(
                model=self.model,
                messages=messages
            )
            self.millis = round(time.time() * 1000) - millis0
            res = completion.choices[0].message.content
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
        itk = completion.usage.prompt_tokens
        otk = completion.usage.completion_tokens
        icost = itk * self.cost_per_intoken
        ocost = otk * self.cost_per_outtoken
        self.tkns = itk + otk
        self.ctxw_remain -= self.tkns
        self.cumulative_cost += icost + ocost  # **M014 Store in instance vbl so tests can access it
        self.last_cost = icost + ocost
        return self.last_cost

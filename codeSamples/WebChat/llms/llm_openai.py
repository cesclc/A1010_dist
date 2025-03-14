"""
openai_llm.py - OpenAILlm class , for accessing different OpenAI LLMs
"""

import time
import traceback
from datetime import datetime


from .llm import Llm
from openai import OpenAI


class OpenAILlm(Llm):
    platform = "openai"
    # Context window size no of IN+OUT tokens:
    ctxw_sizes = {'gpt-3.5-turbo': '16k',
        'gpt-4o': '128k',
        'gpt-4-turbo': '128k',
        'gpt-4': '8k',
        'gpt-4o-mini': '128k',
        'o1-preview': '128k',
        'o1-mini': '128k',
        'dall-e-3': '99k',
        'tts-1': '99k'}
    # Cost per million tokens In/Out
    costper = {'gpt-3.5-turbo': '.5/1.5',
        'gpt-4o': '5/15',
        'gpt-4-turbo': '10/30',
        'gpt-4': '30/60',
        'gpt-4o-mini': '.00015/.00060',
        'o1-preview': '0.015/0.0075',
        'o1-mini': '0.003/0.0015',
        'dall-e-3': '99/99',
        'tts-1': '99/99'}
    # dall-e-3 "from" $0.04 per image so doesnt fit "chat" cost model above, so note as 99/99
    # tts-1 $0.015 per 1,000 characters so doesnt fit "chat" cost model above, so note as 99/99
    # **M014 ^ was:
    # ctxw_sizes = {'gpt-3.5-turbo': '16k', 'gpt-4o': '128k', 'gpt-4-turbo': '128k', 'gpt-4': '8k', 'gpt-4-32k': '32k'}
    # # Cost per million tokens In/Out
    # costper = {'gpt-3.5-turbo': '.5/1.5', 'gpt-4o': '5/15', 'gpt-4-turbo': '10/30', 'gpt-4': '30/60', 'gpt-4-32k': '60/120'}

    def __init__(self):  # Allow no-arg ctor so that callers can use Llm before knowing which platfomr:model they want
        super().__init__(self.platform)

    @classmethod
    def list_models(cls):
        return list(cls.costper.keys())

    @classmethod
    def list_models_aspyx(cls, prefix_model=True):
        """Get a list of models for this platform, as Python code for editing"""
        ret = cls.convert_modellist_topy(cls.costper.keys(), prefix_model)
        return ret

    def create_client(self, model_):
        self.init_client(model_, self.ctxw_sizes[model_], self.costper[model_])  # Init costs etc
        self.client = OpenAI(
            #    api_key=os.environ.get("OPENAI_API_KEY"), # Dont need, reads that env vbl by default, just `export` it
            # Test "per course" keys, to see if a deleted / revoked API key still works
            #   unfortunately deleted keys will still work for (2 hours?) after they're deleted: (in OpenAI dashboard)
            # eg the below key was revoked on 16/9/24:  api_key=(See AI/setenv "Course_240916_key")
        )
        if self.client is None:
            raise RuntimeError("Cant create OpenAI client")

    def invoke(self, messages):  # TODO Maybe delegate to super for common / repeated API forms
        try:
            millis0 = round(time.time() * 1000)
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            self.millis = round(time.time() * 1000) - millis0
            # No need to check for completion containing "error" as we did for LlamaAPI, OpenAI API already throws exep in cases like that
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

"""
bedrock_llm.py - BedrockLlm class , for accessing different Bedrock LLMs
"""
import time
import traceback
from datetime import datetime


from .llm import Llm
from openai import OpenAI


class BedrockLlm(Llm):
    platform = "bedrock"
    # Context window size no of IN+OUT tokens:
    ctxw_sizes = {'TODO... gpt-3.5-turbo': '16k', 'gpt-4o': '128k', 'gpt-4-turbo': '128k', 'gpt-4': '8k', 'gpt-4-32k': '32k'}
    costper = {'TODO... gpt-3.5-turbo': '.5/1.5', 'gpt-4o': '5/15', 'gpt-4-turbo': '10/30', 'gpt-4': '30/60', 'gpt-4-32k': '60/120'}
    # TODO add models: Titan, Cohere command, A121 (and maybe its *-text which are "chat models"
    #   and Bedrock's Anthropic, Llams, Mistral

    def __init__(self):  # Allow no-arg ctor so that callers can use Llm before knowing which platfomr:model they want
        super().__init__(self.platform)

    @classmethod
    def list_models(cls):
        return list(cls.costper.keys())

    def create_client(self, model_):
        self.init_client(model_, self.ctxw_sizes[model_], self.costper[model_])  # Init costs etc
        self.client = OpenAI(  # TODO, Bedrock call...
            #    api_key=os.environ.get("OPENAI_API_KEY"), # Dont need, reads that env vbl by default, just `export` it
        )

    def invoke(self, messages):  # TODO Maybe delegate to super for common / repeated API forms
        try:
            millis0 = round(time.time() * 1000)
            completion = self.client.chat.completions.create(
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

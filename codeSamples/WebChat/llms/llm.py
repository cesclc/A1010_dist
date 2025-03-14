"""
llm.py - Llm class , for accessing different LLM platforms & models
TODO move into separate module, maybe named llms or llm_apis ??
TODO (later / maybe?) Add other platforms: AppleELM, Google, IBM/Granite..., Rhymes-ai-MOE, TitanML, Meta-Spirit,
  and others from HuggingFace(add that before the others, HF has Qwen models)

Change History:
| Ver   | Date     | Description |
| ---   | -------- | ----------- |
| (na)  | /6-/9/24 | Not-versioned, files in main dir of AIE_PlantingGuide project / repo |
| 1.01  | 22/1/25  | Initial release, need to add state etc for multiple callers |

"""


class Llm:
    version = "1.01"
    platforms = ["openai", "llama", "mistral", "anthropic", "bedrock", "huggingface"]

    def __init__(self, platform_):  # Allow no-arg ctor so that callers can use Llm before knowing which platfomr:model they want
        self.platform = platform_
        self.model = None
        self.client = None  # The LLM 'client' vbl that we invoke, will be set by sub-class
        self.ctxw_size = ""  # Context window size description eg "64k"
        self.scosts = "Descriptive cost eg  .5/1.5  for openai:gpt-3.5-turbo"
        self.cost_per_intoken = 0
        self.cost_per_outtoken = 0
        self.cumulative_cost = 0
        self.last_cost = 0
        self.tkns = 0  # Total (in+out) tokens for last request
        self.millis = 0  # Elapsed Milliseconds thet last req took
        self.ctxw_remain = 0

    @classmethod
    def create_platform(cls, platform_name):  # To programatically use different platforms eg openai
        # Import here rather than at the top, to avoid circular dependencies...
        from .llm_openai import OpenAILlm
        from .llm_llama import LlamaLlm
        from .llm_mistral import MistralLlm
        from .llm_anthropic import AnthropicLlm
        from .llm_bedrock import BedrockLlm
        from .llm_huggingface import HuggingFaceLlm
        match platform_name.lower():
            case "openai":
                return OpenAILlm()
            case "llama":
                return LlamaLlm()
            case "mistral":
                return MistralLlm()
            case "anthropic":
                return AnthropicLlm()
            case "bedrock":
                return BedrockLlm()  # TODO
            case "huggingface":
                return HuggingFaceLlm()  # TODO
            case other:
                raise ValueError("Unsupported LLM: "+ other)


    @classmethod
    def list_platforms(cls):
        return cls.platforms

    @classmethod
    def list_modelsfor(cls, platform_):
        # Import here to avoid circular dependency
        from llm_openai import OpenAILlm
        from llm_llama import LlamaLlm
        from llm_mistral import MistralLlm
        from llm_anthropic import AnthropicLlm
        from llm_bedrock import BedrockLlm
        from llm_huggingface import HuggingFaceLlm
        match platform_.lower():
            case "openai":
                return OpenAILlm.list_models()
            case "llama":
                return LlamaLlm().list_models()
            case "mistral":
                return MistralLlm().list_models()
            case "anthropic":
                return AnthropicLlm().list_models()
            case "bedrock":
                return BedrockLlm().list_models()  # TODO
            case "huggingface":
                return HuggingFaceLlm().list_models()  # TODO
            case other:
                raise ValueError("Unsupported LLM: "+ other)

    @classmethod
    def list_models_aspy_for(cls, platform_, prefix_platform=True):
        """Get a list of models for a platform, as Python code for editing"""
        models = cls.list_modelsfor(platform_)
        ret = cls.convert_modellist_topy(platform_, models, prefix_platform)
        return ret

    @classmethod
    def convert_modellist_topy(cls, platform_, models, prefix_platform=True):
        ret = 'models = ["'
        first = True
        # eg if prefix model:  models = ["openai:gpt-3.5-turbo", "openai:gpt-4o"]
        # eg without prefixing model:  models = ["gpt-3.5-turbo", "gpt-4o"]
        for model in models:
            if not first:
                ret += '", "'
            if prefix_platform:
                ret += platform_ + ":"
            ret += model
            if first:
                first = False
        ret += '"]'
        return ret

    def init_client(self, model_, ctxw_size_, costper_):
        self.model = model_
        self.cumulative_cost = 0
        self.last_cost = 0
        self.ctxw_size = ctxw_size_  # eg  "32k"
        self.ctxw_remain = int(ctxw_size_[:-1]) * 1024  # :-1 = drop the trailing "k"
        self.scosts = costper_
        costs = costper_.split("/")
        self.cost_per_intoken = float(costs[0]) / 1_000_000
        self.cost_per_outtoken = float(costs[1]) / 1_000_000


    def calc_ctxw_size(self):
        """ calc size in bytes from the eg "16k" string"""
        return int(self.ctxw_size[:-1]) * 1024 # :-1 = drop the final "k" char


    def getCtxwUsagePcnt(self):  # **M014(b?!) Added, to calc  context window usage %
        """Calc context window usage as %"""
        size = self.calc_ctxw_size()
        cwu = (size - self.ctxw_remain) / size * 100
        return cwu





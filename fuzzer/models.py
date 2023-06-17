import functools
import gc
import inspect
from abc import ABC, abstractmethod

import openai
import tiktoken
import torch

def greedy_sampler(logits):
    return logits.argmax()


class EmbeddingModel(ABC):
    # Embedding models can be queried for embeddings

    @abstractmethod
    def embed(self, text):
        pass


class BlackBoxModel(ABC):
    # BlackBox Models can only be queried for completions

    @abstractmethod
    def complete(self, text) -> str:
        pass

    @abstractmethod
    def tokenize(self, text):
        pass

    @abstractmethod
    def decode(self, tokens) -> str:
        pass


class WhiteBoxModel(BlackBoxModel):
    # WhiteBox Models provides logits for each completion and
    # their sampling can be controlled by the caller

    def complete(self, text, max_tokens=100, live_print=False, **kwargs) -> str:
        completion = None
        for _, (_, completed_tokens) in zip(range(max_tokens), self.complete_stream(text, **kwargs)):
            completion = completed_tokens

            if live_print:
                # Keep overwriting the same line but send newlines to update remote logs
                # should be compatible with jupyter notebooks
                print(f"\r{repr(self.decode(tuple(completion)))}", end="", flush=True)
        return self.decode(tuple(completion))

    @abstractmethod
    def complete_stream(self, text, **kwargs):
        # Yields (logits, completed_tokens) tuple
        pass


class TransformersModel(WhiteBoxModel):
    def __init__(self, model, tokenizer, device="cuda"):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    @functools.lru_cache(maxsize=1000)
    def tokenize(self, text, **kwargs):
        text = ''.join(text)
        return self.tokenizer.encode(text, **kwargs)

    @functools.lru_cache(maxsize=1000)
    def decode(self, tokens, **kwargs):
        return self.tokenizer.decode(tokens, **kwargs)
    
    @torch.inference_mode()
    def complete_stream(self, text, max_tokens=None, **kwargs):
        input_tokens = self.tokenize(text)
        completed_tokens = []
        stop_token_ids = kwargs.get("stop_token_ids", None) or []
        stop_token_ids.append(self.tokenizer.eos_token_id)
        sampler = kwargs.get("sampler", greedy_sampler)

        last_selected_token = None
        past_key_values = None

        while max_tokens is None or len(completed_tokens) < max_tokens:
            if not past_key_values:
                out = self.model(torch.as_tensor([input_tokens],
                                                 device=self.device),
                                 use_cache=True)
            else:
                out = self.model(torch.as_tensor([[last_selected_token]],
                                                 device=self.device),
                                 use_cache=True,
                                 past_key_values=past_key_values)

            # Only retrieve last layer of logits
            logits = out.logits[0][-1]
            past_key_values = out.past_key_values

            response = yield logits, completed_tokens

            if response is None:
                should_continue = True
                # do not pass self to sampling function
                selected_token = sampler(logits)
            else:
                (selected_token, should_continue) = response

            completed_tokens.append(selected_token)
            last_selected_token = selected_token

            if selected_token in stop_token_ids or not should_continue:
                break

        # clean
        del past_key_values, out
        gc.collect()
        torch.cuda.empty_cache()


class OpenAIChatModel(BlackBoxModel):

    def __init__(self, model_name, prompt_template_func=None, temperature=0.9, max_tokens=100):
        self.model_name = model_name
        self.prompt_template_func = prompt_template_func or \
                                    (lambda text: [{"role": "user", "content": text}])
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.encoding_for_model(model_name)

    def complete(self, text, **kwargs):
        prompt = self.prompt_template_func(text)
        chat_completion = openai.ChatCompletion. \
            create(model="gpt-3.5-turbo",
                   messages=prompt,
                   **kwargs)
        return chat_completion.choices

    def tokenize(self, text):
        return self.tokenizer.encode(text)

    def decode(self, tokens):
        return self.tokenizer.decode(tokens)


class OpenAIEmbeddingModel(EmbeddingModel):
    def __init__(self, model_name="text-embedding-ada-002"):
        self.model_name = model_name

    def embed(self, text):
        return openai.Embedding.create(input=text, model=self.model_name)["data"][0]["embedding"]


class SentenceTransformerEmbeddingModel(EmbeddingModel):
    def __init__(self, model_name="all-mpnet-base-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        return self.model.encode(text)
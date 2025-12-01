import asyncio
from openai import AsyncOpenAI

vllm_embed = AsyncOpenAI(
    api_key="dummy",
    base_url="http://192.168.104.253:8111/v1"
)

class VLLMEmbeddingWrapper:
    def __init__(self, model="nomic-ai/nomic-embed-text-v1"):
        self.model = model

    async def embed_query(self, text):
        return await self._async_embed(text)

    async def embed_documents(self, docs):
        return [await self._async_embed(d) for d in docs]
    
    async def _async_embed(self, text):
        try:
            resp = await vllm_embed.embeddings.create(
                model=self.model,
                input=text,
                encoding_format="float"
            )
            return resp.data[0].embedding
        except Exception as e:
            print(f"VLLM Embedding Error: {e}")
            return [0.0] * 768

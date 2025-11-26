from openai import AsyncOpenAI

vllm_client = AsyncOpenAI(
    api_key="gmmgpt",
    # base_url="http://192.168.104.253:8000/v1"
    base_url="http://192.168.104.253:8011/v1"
)

async def ask_vllm(model, prompt):
    """Simple wrapper to call vLLM using OpenAI chat completion format."""
    resp = await vllm_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return resp.choices[0].message.content

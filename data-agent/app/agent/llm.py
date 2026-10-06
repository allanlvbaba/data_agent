import asyncio

import httpx
from langchain.chat_models import init_chat_model

from app.config.app_config import app_config

model_name = app_config.llm.model_name
api_key = app_config.llm.api_key

# llm = init_chat_model(model=model_name, api_key=api_key, temperature=0)
llm = init_chat_model(
    model=model_name,
    api_key=api_key,
    temperature=0,
    model_provider="openai",          # GLM 走 OpenAI 兼容协议
    base_url=app_config.llm.base_url,
    # 智谱为国内直连服务:禁用 trust_env,避免终端残留的代理变量
    # (如 HTTPS_PROXY=127.0.0.1:7897 而 Clash 未开)把请求路由进死代理,
    # 导致 LLM 调用报 APIConnectionError: Connection error.
    http_async_client=httpx.AsyncClient(trust_env=False),
)

if __name__ == '__main__':
    async def test():
        print(await llm.ainvoke("中国的首都是哪里？"))


    print(asyncio.run(test()))

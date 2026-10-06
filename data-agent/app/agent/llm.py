import asyncio

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
)

if __name__ == '__main__':
    async def test():
        print(await llm.ainvoke("中国的首都是哪里？"))


    print(asyncio.run(test()))

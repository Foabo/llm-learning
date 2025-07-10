import os
from langchain_openai import ChatOpenAI

doubao = ChatOpenAI(
    model="doubao-seed-1-6-250615",
    api_key=os.getenv("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    temperature=0.0,
)
chat_model = doubao

if __name__ == "__main__":
    print(chat_model.invoke("你好，我是小爱同学，请问你是谁？").content)

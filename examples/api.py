from openai import OpenAI
import os
import asyncio

def call_chat_completions(model_id, messages, max_tokens, temperature, api_key):
    # 创建 OpenAI 客户端实例
    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
    try:
        # 尝试调用 API
        completion = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        # 如果成功，返回完成的消息
        print('使用了非流式传输，返回的消息为：\n', str(completion.choices[0].message.content))
        return completion.choices[0].message
    except Exception as e:
        # 如果发生异常，打印错误信息
        print(f"An error occurred: {e}")
        return None

def call_chat_completions_stream(model_id, messages, max_tokens, temperature, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
    try:
        # 尝试调用 API
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )
        partial_message = ""
        print('使用了流式传输，返回的消息为：')
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message = partial_message + chunk.choices[0].delta.content
                print(partial_message)
                yield partial_message
        response.close()
    except Exception as e:
        # 如果发生异常，打印错误信息
        print(f"An error occurred: {e}")

def get_model_list(api_key):
    # 创建 OpenAI 客户端实例
    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
    
    # 获取模型列表
    model_list = client.models.list()
    model_data = model_list.data
    print(model_data)
    return model_data




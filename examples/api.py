from openai import OpenAI
from pathlib import Path
import traceback
import asyncio
import os


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
    return model_list.data

def upload_file(files, api_key):
    try:
        # 创建 OpenAI 客户端实例
        client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
        file_object = client.files.create(
            file=Path(files),
            purpose="file-extract",
        )
        print(f"文件 {file_object} 上传成功")
        return file_object
    
    except Exception as e:
        print(f"上传文件 {files} 时发生错误:")
        print(traceback.format_exc())
        # 返回 None 表示上传失败
        return None

def file_extract(file_id, api_key):
    # 创建 OpenAI 客户端实例
    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
    # 获取文件内容
    file_content = client.files.content(file_id=file_id).text
    return file_content

def delete_file(file_id, api_key):
    # 创建 OpenAI 客户端实例
    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
    # 删除文件
    client.files.delete(file_id=file_id)
    return 0

def list_files(api_key):
    # 创建 OpenAI 客户端实例
    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
    # 获取文件列表
    file_list = client.files.list()
    #print(file_list)
    return file_list
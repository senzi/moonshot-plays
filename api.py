from openai import OpenAI
from pathlib import Path
import requests
import traceback
import logging
from requests.exceptions import RequestException


# 定义一个类来模拟 OpenAI 完成消息的结构
class FakeCompletionMessage:
    def __init__(self, content):
        self.content = content

# 伪造一个错误消息的函数
def create_error_message(error_content):
    return FakeCompletionMessage(content=error_content)

# 使用伪造的错误消息代替真实的 API 调用错误
def call_chat_completions(model_id, messages, max_tokens, temperature, api_key):
    error_openai_format = create_error_message("api_key is 'None' !")
    
    if api_key:
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
            print('使用了非流式传输，返回的消息为：\n', str(completion))
            return completion.choices[0].message
        except Exception as e:
            # 如果发生异常，使用伪造的错误消息
            print(f"An error occurred: {e}")
            return create_error_message(f"An error occurred: {e}")
    else:
        # 如果没有提供 API 密钥，也使用伪造的错误消息
        return error_openai_format



# 配置日志记录
logging.basicConfig(level=logging.INFO)

def call_chat_completions_stream(model_id, messages, max_tokens, temperature, api_key):
    if not api_key:
        raise ValueError("api_key is not provided or is invalid.")
    
    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")  
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
            timeout=30  # 设置30秒超时
        )
        partial_message = ""
        logging.info('使用了流式传输，返回的消息为：')
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message += chunk.choices[0].delta.content
                yield partial_message
        logging.info(partial_message)
    except RequestException as e:
        raise e  # 重新抛出请求异常
    except TimeoutError:
        raise TimeoutError("API调用超时，可能需要检查网络连接或服务器状态。")  # 重新抛出超时异常
    except Exception as e:
        logging.error(f"发生错误: {e}")
        raise e  # 重新抛出其他所有异常

        

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
        print(f"上传文件 {files} 时发生错误:"+e)
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

def estimate_token_count(messages, api_key):
    # 构建请求 URL 和头部
    url = 'https://api.moonshot.cn/v1/tokenizers/estimate-token-count'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    # 构建请求体
    payload = {
        "model": "moonshot-v1-8k",
        "messages": messages
    }
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=payload)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容
        response_data = response.json()
        # 提取 total_tokens 值
        total_tokens = response_data.get('data', {}).get('total_tokens')
        if total_tokens is not None:
            return total_tokens
        else:
            # 如果 total_tokens 不存在，打印错误信息并返回 None
            print(f"Error: 'total_tokens' not found in response data. Response: {response_data}")
            return None
    else:
        # 如果响应状态码不是 200，返回响应状态码
        print(f"Error: {response.status_code}, {response.text}")
        return "Error:"+ str(response.status_code)

def query_balance(api_key):

    # 接口请求地址
    url = "https://api.moonshot.cn/v1/users/me/balance"

    # 构建请求头，包含认证信息
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析响应内容
            balance_data = response.json()
            
            # 检查响应数据中的status字段
            if balance_data["status"]:
                return {
                    "available_balance": balance_data["data"]["available_balance"],
                    "voucher_balance": balance_data["data"]["voucher_balance"],
                    "cash_balance": balance_data["data"]["cash_balance"]
                }
            else:
                # 如果status不为true，返回错误信息
                return {"error": "查询失败，服务端返回错误状态。"}
        else:
            # 如果HTTP请求失败，返回错误信息
            return {"error": f"请求失败，状态码：{response.status_code}"}

    except requests.RequestException as e:
        # 如果请求过程中出现异常，返回错误信息
        return {"error": str(e)}
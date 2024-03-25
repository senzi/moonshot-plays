from ichingshifa import ichingshifa
import json
import api
import os
from openai import OpenAI
from dotenv import load_dotenv
import random


def generate_random_string(length=6, allowed_digits='6789'):
    return ''.join(random.choice(allowed_digits) for _ in range(length))

# Example usage:
random_string = generate_random_string()
qigua = generate_random_string()
gua = ichingshifa.Iching().mget_bookgua_details(qigua)

print('\n'+str(gua)+'\n')

load_dotenv()
api_key = os.getenv("MOONSHOT_API_KEY")
model_id = "moonshot-v1-8k"
max_tokens = 2000
temperature = 0.5

sys_prompt = """
你是一个周易解卦大师，请根据提供的卦象信息和用户的问题，进行专业且详细的易经解卦分析。
输出的结果不要模棱两可，要根据卦象信息，针对用户的问题，给出一个十分肯定的答案。
"""

query = "李西北什么时候结婚"

openai_format = []
openai_format.append({"role": "system", "content": sys_prompt})
openai_format.append({"role": "system", "content": "卦象信息如下："+str(gua)})
openai_format.append({"role": "user", "content": "用户问题："+query})
messages = openai_format

response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key)
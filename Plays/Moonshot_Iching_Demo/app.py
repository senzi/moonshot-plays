from ichingshifa import ichingshifa
import json
import api
import os
from openai import OpenAI
from dotenv import load_dotenv
import random
import config
import gradio as gr
import config


def generate_random_string(length=6, allowed_digits='6789'):
    return ''.join(random.choice(allowed_digits) for _ in range(length))

def run():
    print("Starting Moonshot_Iching_Demo ")
    qigua = generate_random_string()
    gua = ichingshifa.Iching().mget_bookgua_details(qigua)
    load_dotenv()
    api_key = config.api_key
    model_id = "moonshot-v1-8k"
    max_tokens = 2000
    temperature = 0.5
    sys_prompt = """
    你是一个周易解卦大师，请根据提供的卦象信息和用户的问题，进行专业且详细的易经解卦分析。
    输出的结果不要模棱两可，要根据卦象信息，针对用户的问题，给出一个十分肯定的答案。
    """
    query = "明天出行是否安全"
    openai_format = []
    openai_format.append({"role": "system", "content": sys_prompt})
    openai_format.append({"role": "system", "content": "卦象信息如下："+str(gua)})
    openai_format.append({"role": "user", "content": "用户问题："+query})
    messages = openai_format
    response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key).content

def handle_qigua_click(query):
    qigua = generate_random_string()
    gua = ichingshifa.Iching().mget_bookgua_details(qigua)
    api_key = config.api_key
    model_id = "moonshot-v1-8k"
    max_tokens = 2000
    temperature = 0.5
    sys_prompt = """
    你是一个周易解卦大师，请根据提供的卦象信息和用户的问题，进行专业且详细的易经解卦分析。
    输出的结果不要模棱两可，要根据卦象信息，针对用户的问题，给出一个十分肯定的答案。
    """
    openai_format = []
    openai_format.append({"role": "system", "content": sys_prompt})
    openai_format.append({"role": "system", "content": "卦象信息如下："+str(gua)})
    openai_format.append({"role": "user", "content": "用户问题："+query})
    messages = openai_format
    response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key).content  
    return str(response)  

def tab_iching():
    with gr.Tab("iching"):
        with gr.Row():
            gr.Markdown("# 赛博周易")
        # 文本输入组件
        with gr.Row():
            text_input = gr.Textbox(label="你想问的事情")
        # 按钮组件，点击后调用handle_button_click函数
        with gr.Row():
            click_me_button = gr.Button("起卦")
        # 文本输出组件，显示handle_button_click函数的返回值
        with gr.Row():
            output = gr.Textbox(label="解卦", interactive=False)
            click_me_button.click(handle_qigua_click, inputs=text_input, outputs=output)    

if __name__ == '__main__':
    run()
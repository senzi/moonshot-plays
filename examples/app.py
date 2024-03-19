from openai import OpenAI
import gradio as gr
import os
import api
import json
from dotenv import load_dotenv

# 加载上一级目录中的 .env 文件
load_dotenv(dotenv_path="../.env")
# 从环境变量中获取 API 密钥
api_key = os.getenv("MOONSHOT_API_KEY")

async def predict(message, history, model_id, max_tokens, temperature, stream):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    messages = history_openai_format
    
    if stream == "True":
        response = api.call_chat_completions_stream(model_id, messages, max_tokens, temperature, api_key)
        for chunk in response:
            yield chunk
    else:
        response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key)
        if response:
            yield response.content


with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("# Moonshot Chat Demo")

    with gr.Row():
        with gr.Column(scale=1):
            model_id = gr.Radio(["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],value="moonshot-v1-8k",label="model_id", info="只有上下文长度不一样",)
            max_tokens = gr.Slider(label="Max Tokens", minimum=100, maximum=8000, value=100, step=10)
            temperature = gr.Slider(label="Temperature", minimum=0.0, maximum=1.0, value=0.3, step=0.1)
            stream = gr.Radio(["True", "False"],value="True",label="stream", info="是否开启流式传输",)
        with gr.Column(scale=4):
            chat = gr.ChatInterface(
                predict,
                additional_inputs=[model_id, max_tokens, temperature, stream],
            )

    with gr.Row():
        gr.Markdown("""
        这是一个基于 Gradio 的聊天机器人应用程序,它利用了 OpenAI 的 API。
        
        该应用程序允许用户与聊天机器人进行对话,并自定义模型参数。
        
        这个应用程序的主要功能包括:

        1. **模型选择**: 用户可以选择使用 `moonshot-v1-8k`、`moonshot-v1-32k` 或 `moonshot-v1-128k` 三种不同的模型。这些模型的主要区别在于上下文长度不同,可以根据需求进行选择。
        2. **参数配置**: 用户可以调整以下参数:
           - **最大令牌数**: 设置生成文本的最大长度,可选范围为 100 到 8000 个令牌。
           - **温度**: 控制生成文本的随机性,取值范围为 0.0 到 1.0。温度越高,生成的文本越随机。
           - **流式传输**: 用户可以选择是否开启流式传输模式。在流式传输模式下,聊天机器人的响应会分段显示,而非一次性返回完整的响应。
        3. **聊天界面**: 应用程序提供了一个聊天界面,允许用户输入消息并查看聊天历史。聊天机器人的响应会根据用户的输入和配置的参数进行生成。
        """)

demo.launch()
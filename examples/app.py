from openai import OpenAI
import gradio as gr
import os
import api
import json
from dotenv import load_dotenv
import md_content

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

def on_get_models_clicked():
    model_list = api.get_model_list(api_key)
    model_data = [(model.id, model.created, model.object, model.owned_by, str(model.permission)) for model in model_list]
    return model_data

with gr.Blocks() as demo:
    with gr.Tab("Chat"):
        with gr.Row():
            gr.Markdown("# Moonshot Chat Demo")

        with gr.Row():
            with gr.Column(scale=1):
                model_id = gr.Radio(["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"], value="moonshot-v1-8k", label="model_id", info="模型的区别在于它们的最大上下文长度")
                max_tokens = gr.Slider(label="Max Tokens", minimum=100, maximum=8000, value=100, step=10)
                temperature = gr.Slider(label="Temperature", minimum=0.0, maximum=1.0, value=0.3, step=0.1)
                stream = gr.Radio(["True", "False"], value="True", label="stream", info="是否开启流式传输")
            with gr.Column(scale=4):
                chat = gr.ChatInterface(
                    predict,
                    additional_inputs=[model_id, max_tokens, temperature, stream],
                )

        with gr.Row():
            gr.Markdown(md_content.CHAT_CONTENT)

    with gr.Tab("Model List"):
        with gr.Row():
            # model_list_output = gr.Textbox(label="Model List", placeholder="Click 'Get Model List' to retrieve available models.")
            model_table = gr.Dataframe(None, headers=['id', 'created', 'object', 'owned_by', 'permission'])
        with gr.Row():
            get_models_button = gr.Button("Get Model List")
            get_models_button.click(on_get_models_clicked, inputs=None, outputs=model_table)

        with gr.Row():
            gr.Markdown(md_content.MODEL_LIST_CONTENT)


    demo.queue()
    demo.launch()


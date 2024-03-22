import os
import api
import json
import md_content
import pretty_errors
import traceback
import gradio as gr
import pandas as pd
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# 初始化全局变量
api_key = None
masked_key = None

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

def upload_file(file):
    print("file 类型:", type(file))
    print("file 内容:", file)
    
    try:
        file_object = api.upload_file(file, api_key)
        if file_object:
            file_id = file_object.id
            print("文件 ID:", file_id)
            return file_id
        else:
            print("文件上传失败,file_object 为 None")
            return "上传失败,可能是不支持的文件类型"
    
    except Exception as e:
        print("文件上传时发生错误:")
        print(traceback.format_exc())
        return "文件上传时发生错误"

def file_extract(file_id):
    file_content = api.file_extract(file_id, api_key)
    return str(file_content)

def copy_file_id(file_id):
    return file_id

def file_list():
    try:
        file_list = api.list_files(api_key)
        files_info = []
        for file_object in file_list.data:
            file_info = {
                "ID": file_object.id,
                "大小 (字节)": file_object.bytes,
                "创建时间": datetime.fromtimestamp(file_object.created_at).strftime('%Y-%m-%d %H:%M:%S'),
                "文件名": file_object.filename
            }
            files_info.append(file_info)
        # 创建 Pandas DataFrame
        df = pd.DataFrame(files_info)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame(columns=["ID", "大小 (字节)", "创建时间", "文件名"])
    
def delete_all_files():
    df_files = file_list()
    file_ids_to_process = df_files['ID'].tolist()
    for file_id in file_ids_to_process:
        api.delete_file(file_id,api_key)
        print(f"删除文件 {file_id} 成功")
    return "成功删除所有文件!"
    
def delete_file(file_id):
    api.delete_file(file_id,api_key)
    re_turn = str(file_id)+"已经删除成功！"
    return re_turn

def token_count(role, content):
    message = {"role": role, "content": content}
    messages = [message]
    token = api.estimate_token_count(messages, api_key)
    message_json = json.dumps(message, indent=4)
    markdown_output = f"```json\n{message_json}\n```\n# token_count: {token}"
    return markdown_output

def api_key_import_env():
    global api_key
    load_dotenv()
    if os.path.exists(".env"):
        api_key_env = os.getenv("MOONSHOT_API_KEY")
    result = api_key_validation(api_key_env)
    return result

def api_key_validation(key_input):
    global api_key, masked_key
    if key_input:
        message = {"role": 'user', "content": 'ping'}
        messages = [message]
        try:
            ping = api.call_chat_completions("moonshot-v1-8k", messages, 100, 0, key_input)
            print(ping)
            if ping is not None and hasattr(ping, 'content') and "pong" in getattr(ping, 'content', '').lower():
                api_key = key_input
                masked_key = key_mask(api_key)
                return "Verification successful!!\nCurrent API Key:" + str(masked_key)
            else:
                return "Invalid: Moonshot didn't SAY 'pong'.\nCurrent API Key:" + str(masked_key)
        except Exception as e:
            return  "Invalid:"+ str(e) + "\nCurrent API Key:" + str(masked_key)
    else:
        return "Please provide your key\nCurrent API Key:" + str(masked_key)

def key_mask(key_to_mask):
    global masked_key
    if key_to_mask:
        prefix = "sk-"
        if key_to_mask.startswith(prefix):
            remaining_key = key_to_mask[len(prefix):]
            masked_key = prefix + remaining_key[:2] + "*****" + remaining_key[-5:]
        else:
            masked_key = None
        return masked_key
    else:
        return None

def api_key_deactivate():
    global masked_key, api_key
    masked_key = None
    api_key = None
    return "API Key Deactivated\nCurrent API Key:" + str(masked_key)

with gr.Blocks() as demo:
    with gr.Row(): 
        with gr.Column(scale=5):
            gr.Markdown(md_content.HOME)
        with gr.Column(scale=2):
            with gr.Group():
                with gr.Row(): import_key_button = gr.Button("从env导入API Key")
                with gr.Row(): current_key = gr.Textbox(label="API Key")
                with gr.Row(): check_key_button = gr.Button("尝试导入上述API Key")
                with gr.Row(): deactivate_key_button = gr.Button("清空 API_KEY")
                import_key_button.click(api_key_import_env, None, current_key)
                check_key_button.click(api_key_validation, current_key, current_key)
                deactivate_key_button.click(api_key_deactivate, None, current_key)
    with gr.Row():
        with gr.Tab("Chat Completion"):
            with gr.Row():
                gr.Markdown("# Moonshot Chat Demo")
            with gr.Row():
                with gr.Column(scale=1):
                    model_id = gr.Radio(["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"], value="moonshot-v1-8k", label="Model ID", info="模型的区别在于它们的最大上下文长度")
                    max_tokens = gr.Slider(label="Max Tokens", minimum=100, maximum=8000, value=100, step=10)
                    temperature = gr.Slider(label="Temperature", minimum=0.0, maximum=1.0, value=0.3, step=0.1)
                    stream = gr.Radio(["True", "False"], value="True", label="Stream", info="是否开启流式传输")
                with gr.Column(scale=4):
                    chat = gr.ChatInterface(
                        predict,
                        additional_inputs=[model_id, max_tokens, temperature, stream],
                    )
            with gr.Row():
                gr.Markdown(md_content.CHAT_CONTENT)
        with gr.Tab("Model List"):
            with gr.Row(): gr.Markdown("# Get Moonshot Model List")
            with gr.Row():
                model_table = gr.Dataframe(None, headers=['model_id', 'created', 'object', 'owned_by', 'permission'])
            with gr.Row():
                get_models_button = gr.Button("Get Model List")
                get_models_button.click(on_get_models_clicked, inputs=None, outputs=model_table)
            with gr.Row():
                gr.Markdown(md_content.MODEL_LIST_CONTENT)
        with gr.Tab("File operations"):
            with gr.Row(): gr.Markdown("# Moonshot Files API Demo")
            with gr.Row():
                with gr.Column(scale=3): 
                    with gr.Row(): gr.Markdown("## Upload File")
                    with gr.Row():
                        with gr.Column(scale=2): 
                            file_output = gr.Textbox(label="File ID", interactive=False)
                        with gr.Column(scale=1): 
                            copy_button = gr.Button("发送ID到右边")
                    with gr.Row():
                        upload_button = gr.UploadButton("Click to Upload a File", file_types=["text"], file_count="single")
                        upload_button.upload(upload_file, upload_button, file_output)
                with gr.Column(scale=5): 
                    with gr.Row(): gr.Markdown("## Get Content")
                    with gr.Row():
                        with gr.Column(scale=1): 
                            file_id_input = gr.Textbox(label="File ID")
                            copy_button.click(copy_file_id, file_output, file_id_input)
                            file_extract_button = gr.Button("Extract")
                        with gr.Column(scale=2): 
                            file_extract_content = gr.Textbox(label="Extracted Content", interactive=False)
                            file_extract_button.click(file_extract, file_id_input, file_extract_content)
            with gr.Row():
                with gr.Column(scale=1): 
                    gr.Markdown("## List Files")
                    file_list_output = gr.Dataframe()
                    file_list_button = gr.Button("List Files")
                    file_list_button.click(file_list, None, file_list_output)
                with gr.Column(scale=1): 
                    gr.Markdown("## Delete Files")
                    file_id_delete = gr.Textbox(label="File ID To Delete")
                    with gr.Row():
                        delete_file_button = gr.Button("Delete File")
                        delete_file_button.click(delete_file, file_id_delete, file_id_delete)
                        delete_file_button = gr.Button("!! Delete All Files !!")
                        delete_file_button.click(delete_all_files, None, file_id_delete)
            with gr.Row():
                gr.Markdown(md_content.FILE_CONTENT)
        with gr.Tab("Token Count"):
            with gr.Row():
                gr.Markdown("# Moonshot Token Count Demo")
            with gr.Row():
                tc_role = gr.Radio(["system", "user", "assistant"],
                        value="system",
                        label="Select Role",
                        info="Choose the role of the message sender")
            with gr.Row():
                tc_content = gr.Textbox("Enter message content", label="Content", placeholder="Type your message here...")
            with gr.Row():
                tc_button = gr.Button("Calculate Token Count")
            with gr.Row():
                with gr.Column():
                    tc_token = gr.Markdown("结果显示在这里", label="result")
                    tc_button.click(token_count, [tc_role,tc_content], tc_token)
            with gr.Row():
                gr.Markdown(md_content.TOKEN_CONTENT)
 
    demo.queue()
    demo.launch()


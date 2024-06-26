import os
import api
import config
import gradio as gr
import md_content
from dotenv import load_dotenv
import Plays.Moonshot_Iching_Demo.app as iching
import Plays.Moonshot_API_Demo.app as api_demo
import Plays.Tab_Template.app as template
import Plays.AutoWriter_Demo.app as writer

# 初始化全局变量
api_key = config.api_key
masked_key = None



def api_key_import_env():
    load_dotenv()
    api_key_env = None
    masked_key = "None"
    if os.path.exists(".env"):
        api_key_env = os.getenv("MOONSHOT_API_KEY")
        config.api_key = api_key_env
        masked_key = key_mask(config.api_key)
    return  "Current API Key:" + str(masked_key)

def just_import_key(key_input):
    global masked_key
    config.api_key = key_input
    masked_key = key_mask(config.api_key)
    return  "Current API Key:" + str(masked_key)

def api_key_validation(key_input):
    global masked_key
    if key_input:
        message = {"role": 'user', "content": 'ping'}
        messages = [message]
        try:
            ping = api.call_chat_completions("moonshot-v1-8k", messages, 100, 0, key_input)
            print(ping)
            if ping is not None and hasattr(ping, 'content') and "pong" in getattr(ping, 'content', '').lower():
                config.api_key = key_input
                masked_key = key_mask(config.api_key)
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
    global masked_key
    masked_key = None
    config.api_key = None
    return "API Key Deactivated\nCurrent API Key:" + str(masked_key)

def gr_block_header():
    with gr.Group():
        with gr.Row(): 
            with gr.Column(scale=5):
                gr.Markdown(md_content.HOME)
            with gr.Column(scale=2):
                with gr.Group():
                    if config.Config.DEBUG:
                        with gr.Row(): 
                            import_key_button = gr.Button("从env导入API Key[DEBUG]")
                    with gr.Row(): 
                        current_key = gr.Textbox(label="API Key")
                    with gr.Row(): 
                        check_key_button = gr.Button("验证并导入Key")
                        just_import_button = gr.Button("直接导入Key")
                    with gr.Row(): 
                        deactivate_key_button = gr.Button("清空 API_KEY")
                    if config.Config.DEBUG:
                        import_key_button.click(api_key_import_env, None, current_key)
                    check_key_button.click(api_key_validation, current_key, current_key)
                    just_import_button.click(just_import_key, current_key, current_key)
                    deactivate_key_button.click(api_key_deactivate, None, current_key)

if config.Config.DEBUG:
    api_key_import_env()

with gr.Blocks() as demo:
    gr_block_header()
    print("show gr_block_header")
    api_demo.tab_chat()
    api_demo.tab_model_list()
    api_demo.tab_file_operations()
    api_demo.tab_token_count()
    api_demo.tab_query_balanc()
    iching.tab_iching()
    writer.Autowriter_tab()
    template.template_tab()

demo.queue()
demo.launch(inbrowser=True)
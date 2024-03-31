from escpos import *
from PIL import Image
import api
import os
import gradio as gr
import config
import md_content
from datetime import datetime
import calendar
import hashlib

def hash_str(input):
    # 创建一个新的sha256哈希对象（您也可以选择其他哈希算法，如md5, sha1等）
    hash_object = hashlib.sha256()
    # 对字符串进行编码，因为hashlib只能处理字节类型数据
    encoded_string = input.encode('utf-8')
    # 使用update方法更新哈希对象
    hash_object.update(encoded_string)
    # 获取十六进制格式的哈希值
    hex_hash = hash_object.hexdigest()
    # 保留哈希值的前16位
    first_16_chars = hex_hash[:32]
    return first_16_chars

def print_logo(printer_object):
    logo = Image.open("normal-light.png")
    # 计算新的尺寸以适应打印纸
    new_width = 330  # 期望的宽度，以像素为单位
    new_height = int(logo.height * new_width / logo.width)
    # 调整图片尺寸
    logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
    printer_object.set(align="center")
    printer_object.image(logo)

def get_date_time():
    # 获取当前时间
    now = datetime.now()
    # 获取中文星期几
    chinese_weekday = calendar.day_name[now.weekday()]  # 星期几的中文表示
    # 格式化时间
    formatted_time = "{} ({}) {}:{}:{}".format(
        now.strftime("%Y-%m-%d"),  # 年月日
        chinese_weekday,  # 中文星期几
        now.strftime("%H"),  # 小时（24小时制）
        now.strftime("%M"),  # 分钟
        now.strftime("%S")  # 秒
    )
    return formatted_time

def handle_button_click(query):
    p = printer.Usb(0x0483,0x5743)
    api_key = config.api_key
    model_id = "moonshot-v1-8k"
    max_tokens = 2000
    temperature = 0.5
    sys_prompt = """
    """
    openai_format = []
    # openai_format.append({"role": "system", "content": sys_prompt})
    openai_format.append({"role": "user", "content": query})
    messages = openai_format
    
    #打印
    p.set(align="left")
    p.textln(get_date_time())
    p.textln("model_id:"+ model_id )
    p.set(align="center")
    p.textln("----------")
    p.set(align="left")
    print_logo(p)
    p.set(align="center")
    p.textln("----------")
    p.set(align="left")
    p.textln("[User]")
    p.textln(query)
    p.textln("")
    p.textln("[Moonshot]")
    response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key).content
    p.textln(response)
    p.set(align="center")
    p.textln("----------")
    p.textln("hash:" + hash_str(response))
    p.textln("")
    p.textln("")
    p.cut()
    p.close()
    return str(response)  
# 创建Gradio界面的函数
def tab_print_chat():
    with gr.Tab("Print"):
        with gr.Row():
            gr.Markdown("# Print Demo")
        # 使用Markdown组件显示一些文本
        with gr.Row():
            text_input = gr.Textbox(label="输入文本")
        # 按钮组件，点击后调用handle_button_click函数
        with gr.Row():
            click_me_button = gr.Button("打印")
        # 文本输出组件，显示handle_button_click函数的返回值
        with gr.Row():
            output = gr.Textbox(label="输出", interactive=False)
            click_me_button.click(handle_button_click, inputs=text_input, outputs=output)
        with gr.Row():
            gr.Markdown(md_content.TEMPLATE_CONTENT)
#Tab_Template/app.py
import api
import os
import gradio as gr
import config
import md_content

# 假设这是您的Markdown内容
mdcontent = "这里是模板的描述。"

# 如果需要用到Moonshot的API,请使用config.api_key作为key传入
# 但无论任何时候，都不应该直接暴露config.api_key的值(显示、打印)

# 定义一个简单的函数，用于处理按钮点击事件
def handle_button_click(text_input):
    # 这里可以添加任何逻辑，现在只是简单地返回一个字符串
    return "按钮被点击了,你的输入是："+str(text_input)

# 创建Gradio界面的函数
def template_tab():
    with gr.Tab("Template"):
        with gr.Row():
            gr.Markdown("# Template")
        # 使用Markdown组件显示一些文本
        with gr.Row(): gr.Markdown(mdcontent)
        # 文本输入组件
        with gr.Row():
            text_input = gr.Textbox(label="输入文本")
        # 按钮组件，点击后调用handle_button_click函数
        with gr.Row():
            click_me_button = gr.Button("点击我")
        # 文本输出组件，显示handle_button_click函数的返回值
        with gr.Row():
            output = gr.Textbox(label="输出", interactive=False)
            click_me_button.click(handle_button_click, inputs=text_input, outputs=output)
        with gr.Row():
            gr.Markdown(md_content.TEMPLATE_CONTENT)
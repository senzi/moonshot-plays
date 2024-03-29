import api
import os
import gradio as gr
import config
import md_content
import json

# 如果需要用到Moonshot的API,请使用config.api_key作为key传入
# 但无论任何时候，都不应该直接暴露config.api_key的值(显示、打印)

def xxx(query):
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
    openai_format.append({"role": "system", "content": "卦象信息如下："})
    openai_format.append({"role": "user", "content": "用户问题："+query})
    messages = openai_format
    response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key).content  
    return str(response)  


def extract_json_from_string(json_string):
    try:
        # 尝试解析整个字符串为 JSON
        json_data = json.loads(json_string)
        return json_data
    except json.JSONDecodeError:
        # 如果解析失败，返回错误信息
        return "Invalid JSON data"

def generate_catalog(length, topic):
    string1 = """
    需要你组织一篇文章的大纲，篇幅为{length}，文章的主题是：{topic}。你还需要构想大纲中每个章节的标题和梗概，以及预计的章节字数。
    """.format(length=length,topic=topic)

    string2 = """
    输出的格式是JSON，需要包含每个章节的标题、内容梗概、章节字数}
    """
    api_key = config.api_key
    model_id = "moonshot-v1-8k"
    max_tokens = 2000
    temperature = 0.5
    sys_prompt = string1+string2
    openai_format = []
    openai_format.append({"role": "system", "content": sys_prompt})
    messages = openai_format
    response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key).content
    print(response)
    re_json = extract_json_from_string(response)
    return re_json
    



    

def Autowriter_tab():
    with gr.Tab("Autowriter"):
        with gr.Row():
            gr.Markdown("# Autowriter Demo")
        with gr.Row():test = gr.Textbox(label="test")
        with gr.Row():
            with gr.Group():
                with gr.Row(): length = gr.Radio(["短篇", "中篇", "长篇"], label="篇幅", info="请选择文章篇幅")
                with gr.Row(): topic  = gr.Textbox(label="简述主题")
            catalog = gr.JSON(label = "大纲JSON")
        with gr.Row(): json_button = gr.Button("生成大纲")
        json_button.click(fn=generate_catalog, inputs=[length, topic], outputs=catalog)
	
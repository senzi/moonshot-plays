import api
import os
import gradio as gr
import config
import md_content
import json

# 如果需要用到Moonshot的API,请使用config.api_key作为key传入
# 但无论任何时候，都不应该直接暴露config.api_key的值(显示、打印)

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
    temperature = 0.1
    sys_prompt = string1+string2
    openai_format = []
    openai_format.append({"role": "system", "content": sys_prompt})
    messages = openai_format
    response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key).content
    print(response)
    re_json = extract_json_from_string(response)
    return re_json

def generate_full_article(catalog, topic):
    string1 = """
    需要用Markdown格式写一篇文章，文章的主题是"{topic}"。请按以下要求实现这个章节的内容：
    """.format(topic=topic)
    full_article = ""
    for chapter_key in catalog:
        string2 = (f"### {catalog[chapter_key]}")
        sys_prompt = string1+string2
        api_key = config.api_key
        model_id = "moonshot-v1-8k"
        max_tokens = 2000
        temperature = 0.1
        openai_format = []
        openai_format.append({"role": "system", "content": sys_prompt})
        messages = openai_format
        print("正在编写："+str(chapter_key))
        response = api.call_chat_completions(model_id, messages, max_tokens, temperature, api_key).content
        full_article = full_article + "\n" + response
    return [full_article,full_article]

    

def Autowriter_tab():
    with gr.Tab("Autowriter"):
        with gr.Row():
            gr.Markdown("# Autowriter Demo")
        with gr.Row():
            with gr.Group():
                with gr.Row(): length = gr.Radio(["短篇", "中篇", "长篇"], label="篇幅", info="请选择文章篇幅")
                with gr.Row(): topic  = gr.Textbox(label="简述主题")
            catalog = gr.JSON(label = "大纲JSON")
        with gr.Row(): json_button = gr.Button("生成大纲")
        with gr.Row(): full_article_button = gr.Button("生成全文")
        json_button.click(fn=generate_catalog, inputs=[length, topic], outputs=catalog)
        with gr.Row():full_article = gr.Textbox(label="全文输出")
        with gr.Row():full_article_md = gr.Markdown(label="全文渲染")
        full_article_button.click(fn=generate_full_article, inputs=[catalog, topic], outputs=[full_article, full_article_md])
            
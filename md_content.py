HOME = """
# Moonshot Playground

## 步骤

1. **导入API Key**: 在页面右侧，手动输入您自己的API Key并进行验证导入。离开页面前，点击清空 API_KEY以免个人key泄露。
   
2. **选择Demo**: 在下方区域，浏览并选择您想要体验的Demo。选择后，您将能够直接在Playground中测试和体验搭载Moonshot的各种应用Demo。

## 备注

- 为了验证您的API Key是否有效，会尝试给Moonshot发送一个"ping"消息。这将是一个简单的请求，只会消耗极少量的Token。
- 未进行充值满50元的用户，RPM: request per minute 是3，其中"ping"消息会有一次request。
"""

CHAT_CONTENT = """
# Moonshot AI Chat Completion

## Introduction

The Moonshot AI Chat Completion API is a powerful tool that allows developers to integrate advanced conversational AI into their applications. It provides a simple and flexible interface for generating human-like responses to user inputs, leveraging the capabilities of Moonshot AI's large models.

## Quick Start

To get started with the Chat Completion API, you'll need to make a POST request to the following endpoint:

```
POST https://api.moonshot.cn/v1/chat/completions
```

Here's an example of what the request body might look like:

```json
{
  "model": "moonshot-v1-8k",
  "messages": [
    {
      "role": "system",
      "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
    },
    {
      "role": "user",
      "content": "你好，我叫李雷，1+1等于多少？"
    }
  ],
  "temperature": 0.3
}
```

### Fields Explanation

- `messages`: A list of dictionaries containing the conversation history. Each dictionary must have a `role` (either "system", "user", or "assistant") and a `content` string.
- `model`: The ID of the model to use. Available options are `moonshot-v1-8k`, `moonshot-v1-32k`, and `moonshot-v1-128k`. The model ID determines the maximum context length.
- `max_tokens`: The maximum number of tokens to generate in the completion. If not specified, a default value will be used.
- `temperature`: A value between 0 and 1 that controls the randomness of the output. A lower value (e.g., 0.2) will produce more deterministic responses, while a higher value (e.g., 0.7) will result in more varied outputs.
- `stream`: A boolean indicating whether to stream the response. The default is `false`, but you can set it to `true` for a streaming response.

### Additional Parameters

- `top_p`: Another form of temperature control. Default is 1.0.
- `n`: The number of completions to generate for each input message. The default is 1, and the maximum is 5.

## UI Integration Example

Below is an example of how you might integrate the Chat Completion API into a UI using the gradio library:

```python
import gradio as gr

def predict(model_id, messages, max_tokens, temperature, stream):
    # Your code to make the API call and process the response goes here
    pass

md_content = {
    "CHAT_CONTENT": "这里是聊天内容的Markdown格式展示"
}

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
        gr.Markdown(md_content["CHAT_CONTENT"])

# Run the interface
iface = gr.Interface()
iface.launch()
```

## Official Documentation

For more detailed information on the Chat Completion API, including error handling and rate limits, please refer to the [official documentation](https://platform.moonshot.cn/docs/api-reference#chat-completion).
"""




MODEL_LIST_CONTENT = """
# Moonshot AI Model List

## Overview

This document provides a guide on how to use the Moonshot AI Open Platform API to retrieve a list of available models. This API is essential for understanding the models supported by Moonshot AI, their capabilities, and selecting the appropriate model for tasks such as chat generation or other AI-based interactions.

## Quick Start

To fetch the list of models supported by Moonshot AI, you need to send a GET request to the following endpoint:

```
GET https://api.moonshot.cn/v1/models
```

### Python Example

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key="MOONSHOT_API_KEY",
    base_url="https://api.moonshot.cn/v1",
)

model_list = client.models.list()
model_data = model_list.data

for i, model in enumerate(model_data):
    print(f"model[{i}]: {model.id}")
```

### CURL Example

```bash
curl https://api.moonshot.cn/v1/models -H "Authorization: Bearer $MOONSHOT_API_KEY"
```

Make sure to replace `MOONSHOT_API_KEY` with your actual API key before making the request.

## UI Integration

For a user interface (UI) integration example, you can use the gradio library to create a simple interface that allows users to fetch the model list with a single click:

```python
import gradio as gr

def on_get_models_clicked():
    client = OpenAI(
        api_key="MOONSHOT_API_KEY",
        base_url="https://api.moonshot.cn/v1",
    )
    model_list = client.models.list()
    model_data = model_list.data
    model_table = [['model[{}]: {}'.format(i, model.id) for i, model in enumerate(model_data)]]
    return model_table

with gr.Tab("Model List"):
    with gr.Row():
        gr.Markdown("# Get `Moonshot` Model List")
    with gr.Row():
        model_table = gr.Dataframe(None, headers=['Model ID'])
    with gr.Row():
        get_models_button = gr.Button("Get Model List")
        get_models_button.click(on_get_models_clicked, inputs=None, outputs=model_table)
    with gr.Row():
        gr.Markdown(md_content.MODEL_LIST_CONTENT)

# Launch the interface
iface = gr.Interface()
iface.launch()
```

## Official Documentation

For more detailed information on the List Models API and other related APIs, please refer to the [official documentation](https://platform.moonshot.cn/docs/api-reference#list-models).
"""

FILE_CONTENT = """
# Moonshot AI File Operations API

## Introduction

The Moonshot AI File Operations API allows developers to manage and interact with files programmatically. This includes uploading files, extracting content from them, listing files, and deleting files that are no longer needed. These capabilities are particularly useful when you want to incorporate file content into AI-generated responses or when managing a large number of documents.

## Quick Start

To get started with the File Operations API, you will need to interact with the following endpoints:

- **Upload File**: `POST https://api.moonshot.cn/v1/files`
- **List Files**: `GET https://api.moonshot.cn/v1/files`
- **Delete File**: `DELETE https://api.moonshot.cn/v1/files/{file_id}`
- **Get File Information**: `GET https://api.moonshot.cn/v1/files/{file_id}`
- **Get File Content**: `GET https://api.moonshot.cn/v1/files/{file_id}/content`

### Python Example

```python
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key="MOONSHOT_API_KEY",
    base_url="https://api.moonshot.cn/v1", 
)

# Upload a file
file_object = client.files.create(file=Path("xlnet.pdf"), purpose="file-extract")

# Get the content of the uploaded file
file_content = client.files.content(file_id=file_object.id).text

# Use the file content in a chat completion request
messages = [
    {
        "role": "system",
        "content": "You are Kimi, an AI assistant provided by Moonshot AI. You specialize in Chinese and English conversations and provide safe, helpful, and accurate answers. You refuse to answer any questions involving terrorism, racial discrimination, or explicit violence. Moonshot AI is a proprietary name and cannot be translated into other languages.",
    },
    {
        "role": "system",
        "content": file_content,
    },
    {"role": "user", "content": "Please briefly introduce what xlnet.pdf is about."},
]

completion = client.chat.completions.create(
    model="moonshot-v1-32k",
    messages=messages,
    temperature=0.3,
)

print(completion.choices[0].message)
```

## UI Integration

Here's an example of how you might integrate the File Operations API into a user interface using the gradio library:

```python
import gradio as gr

def upload_file(uploaded_file, file_output):
    # Your code to handle file upload goes here
    pass

def file_extract(file_id_input, file_extract_content):
    # Your code to handle file extraction goes here
    pass

def file_list():
    # Your code to handle listing files goes here
    pass

def delete_file(file_id_delete):
    # Your code to handle file deletion goes here
    pass

with gr.Tab("File Operations"):
    with gr.Row():
        gr.Markdown("# Moonshot Files API Demo")
    with gr.Row():
        with gr.Column(scale=3): 
            with gr.Row(): gr.Markdown("## Upload File")
            with gr.Row():
                with gr.Column(scale=2): 
                    file_output = gr.Textbox(label="File ID", interactive=False)
                with gr.Column(scale=1): 
                    copy_button = gr.Button("Send ID to Right")
            with gr.Row():
                upload_button = gr.UploadButton("Click to Upload a File", file_types=["text"], file_count="single")
                upload_button.upload(upload_file, upload_button, file_output)
    with gr.Column(scale=5): 
        with gr.Row(): gr.Markdown("## Get Content")
        with gr.Row():
            with gr.Column(scale=1): 
                file_id_input = gr.Textbox(label="File ID")
                copy_button.click(copy_file_id, file_output, file_id_input)
            with gr.Column(scale=2): 
                file_extract_button = gr.Button("Extract")
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

# Launch the interface
iface = gr.Interface()
iface.launch()
```

## Official Documentation

For more detailed information on the File Operations API and its usage, please refer to the [official documentation](https://platform.moonshot.cn/docs/api-reference#%E6%96%87%E4%BB%B6%E5%86%85%E5%AE%B9%E6%8A%BD%E5%8F%96).
"""

TOKEN_CONTENT = """
# Moonshot AI Token Count API

## Overview

The Moonshot AI Token Count API is a service that allows you to estimate the number of tokens that a given input will be tokenized into. This is particularly useful when you need to ensure that your requests stay within the token limits for a specific model, such as `moonshot-v1-8k`, `moonshot-v1-32k`, or `moonshot-v1-128k`.

## Quick Start

To use the Token Count API, you will need to send a POST request to the following endpoint:

```
POST https://api.moonshot.cn/v1/tokenizers/estimate-token-count
```

The request body should follow the same structure as the chat completion request, with the `messages` field containing a list of dictionaries representing the conversation history and the `model` field specifying the model ID.

### Request Example

```json
{
    "model": "moonshot-v1-8k",
    "messages": [
        {
            "role": "system",
            "content": "You are Kimi, an AI assistant provided by Moonshot AI. You specialize in Chinese and English conversations and provide safe, helpful, and accurate answers. You refuse to answer any questions involving terrorism, racial discrimination, or explicit violence. Moonshot AI is a proprietary name and cannot be translated into other languages."
        },
        {
            "role": "user",
            "content": "Hello, my name is Li Lei, what is 1+1?"
        }
    ]
}
```

### Response Example

The response will contain a `data` field with the `total_tokens` calculated for the input:

```json
{
    "data": {
        "total_tokens": 80
    }
}
```

## UI Integration

Here's an example of how you can integrate the Token Count API into a user interface using the gradio library:

```python
import gradio as gr

def token_count(role, content):
    # Your code to calculate token count goes here
    pass

with gr.Tab("Token Count"):
    with gr.Row():
        gr.Markdown("# Moonshot Token Count Demo")
    with gr.Row():
        gr.Radio(["system", "user", "assistant"], value="system", label="Select Role", info="Choose the role of the message sender")
    with gr.Row():
        gr.Textbox("Enter message content", label="Content", placeholder="Type your message here...")
    with gr.Row():
        gr.Button("Calculate Token Count")
    with gr.Row():
        with gr.Column():
            gr.Markdown("结果显示在这里", label="result")
            gr.Button.click(token_count, ["role", "content"], "result")

# Launch the interface
iface = gr.Interface()
iface.launch()
```

## Official Documentation

For more detailed information on the Token Count API and its usage, please refer to the [official documentation](https://platform.moonshot.cn/docs/api-reference#%E8%AE%A1%E7%AE%97-token).
"""

TEMPLATE_CONTENT = """
# Development and Usage Guide for Tab Template 📚

## Development Process 🛠️

1. **Environment Preparation**: Ensure that your environment has the `gradio` library and `api` module installed. If not, use the corresponding package management tool to install them.

2. **Code Writing**: Follow these steps to write your Tab template code:

   - 📂 Import necessary modules, including `api`, `os`, `gradio`, and `config`.
   - 📝 Define Markdown content, which will be used to describe your Tab template.
   - 🔐 Use `config.api_key` as the API key, but remember not to expose the value of the key directly.
   - 💡 Define processing functions, such as `handle_button_click`, to handle user input and triggered events.
   - 🎨 Use `gradio`'s Tab and Row components to build the interface, including Markdown display, text input, buttons, and output display.

3. **Testing**: 🧪 Run your code in a local environment to ensure that all components work properly and the logic is correct.

4. **Deployment**: 🚀 Deploy your code to a server or cloud platform to ensure that users can access and use your Tab template.

## Integration into Main Application 🔄

To integrate the Tab template into your main application, you need to perform the following operations in the `app.py` file located in the root directory:

1. **Import Module**: 📦 Import the `app` from the `Plays.Tab_Template` module and refer to it as `template`.

   ```python
   from Plays.Tab_Template import app as template
   ```

2. **Create Gradio Interface**: 🌐 Use Gradio's `Blocks` component to create a dynamic interface and call the `template_tab()` function within it.

   ```python
   with gr.Blocks() as demo:
       # Other components and logic
       template.template_tab()
   ```

3. **Launch Application**: 🚀 Use the `queue()` and `launch()` methods to prepare and start the application.

   ```python
   demo.queue()
   demo.launch()
   ```

## Usage Process 📱

1. **Access the Application**: 🌐 Users can access the application by visiting the deployment address of your application to open the Tab template interface.

2. **Input Data**: 🔍 Users can enter data they wish to process in the text input box.

3. **Trigger Events**: 🎯 Users click the button component to trigger the corresponding processing function.

4. **View Results**: 📊 After the processing function is executed, the results will be displayed in the output component.

## Notes 📝

- **Security**: 🛡️ Ensure the security of your code when handling user input to avoid any operations that may lead to security vulnerabilities.
- **Performance**: 🏎️ Optimize the logic of your code to ensure the responsiveness and efficiency of the application.
- **User Experience**: 🎮 Design an intuitive and easy-to-use interface so that users can easily understand and operate.
- **Maintenance and Updates**: 🧩 Regularly maintain and update the code to fix any potential issues and add new features.
- **Compliance with Laws and Regulations**: 📜 Always comply with relevant laws and regulations, and respect user privacy during development and usage.

By following the above development, integration, and usage processes, you can create a secure and efficient Tab template to provide users with a quality service experience. Also, continue to learn and improve to adapt to the ever-changing technological environment and user needs. 🌟
"""

ICHING_CONTENT = """
# README for IChing Tab Application 🌟

## Overview 📊

The IChing Tab Application is a cutting-edge tool that seamlessly merges the profound insights of the IChing with the latest advancements in technology. This application, built with the user-friendly Gradio framework and the powerful OpenAI API, offers a unique, interactive platform for seeking guidance and wisdom from the IChing, a revered system of divination that has stood the test of time.

## Features 🚀

- **Dynamic Hexagram Generation**: The app generates a hexagram randomly, ensuring an unbiased and fresh perspective with each use.
- **In-Depth IChing Insights**: By harnessing the `ichingshifa` module, the app delivers comprehensive interpretations of the hexagrams cast.
- **User-Centric Design**: The intuitive Gradio interface ensures that users can easily pose their questions and obtain insights at the click of a button.
- **Seamless AI Integration**: The app integrates with the OpenAI API to provide detailed, expert-level analysis of the IChing, tailored to the user's query.
- **Customizable Prompts**: The AI is guided by a thoughtfully designed system prompt to ensure clear, decisive answers that address the user's question directly.

## How to Use 🤖

1. **Launch the App**: Open the application in your web browser to access the IChing Tab.
2. **Pose Your Question**: Input your question or concern into the designated text box.
3. **Cast Your Hexagram**: Click the "起卦" (Cast Hexagram) button to generate a hexagram and initiate the divination process.
4. **Receive Wisdom**: The app will present a detailed analysis, connecting the generated hexagram to your question and offering guidance rooted in the ancient wisdom of the IChing.

## Technical Specifications 🔧

- The `ichingshifa` module is utilized for the generation and interpretation of hexagrams.
- The `api` module facilitates communication with the OpenAI API, using `config.api_key` for secure access.
- The `gradio` library is employed to craft a dynamic and responsive web interface.
- Random hexagram generation is achieved through the `random` module.
- Configuration settings, such as the API key, are managed through the `config` module.

## Contribution and Support 🤝

Your feedback, suggestions, and potential contributions are highly valued. Please get in touch with us if you have any ideas on how to enhance the application or if you encounter any issues. We are dedicated to refining the user experience and ensuring that the IChing Tab Application remains a valuable resource for those seeking wisdom and guidance.

## License 📜

This project is licensed under the DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE (WTFPL). This permissive license allows you to do whatever you want with this software, including running, studying, sharing, and modifying it without any restrictions. For more information, please see the LICENSE file included in the project.

Enjoy exploring the depths of the IChing and discovering timeless wisdom with the IChing Tab Application. 🧘‍♂️🔮
"""
CHAT_CONTENT = """
            这是一个基于 Gradio 的聊天机器人应用程序,它利用了 OpenAI 的 API。
        
            该应用程序允许用户与聊天机器人进行对话,并自定义模型参数。
        
            这个应用程序的主要功能包括:

            1. **模型选择**: 用户可以选择使用 `moonshot-v1-8k`、`moonshot-v1-32k` 或 `moonshot-v1-128k` 三种不同的模型。这些模型的主要区别在于上下文长度不同,可以根据需求进行选择。
            2. **参数配置**: 用户可以调整以下参数:
               - **最大令牌数**: 设置生成文本的最大长度,可选范围为 100 到 8000 个令牌。
               - **温度**: 控制生成文本的随机性,取值范围为 0.0 到 1.0。温度越高,生成的文本越随机。
               - **流式传输**: 用户可以选择是否开启流式传输模式。在流式传输模式下,聊天机器人的响应会分段显示,而非一次性返回完整的响应。
            3. **聊天界面**: 应用程序提供了一个聊天界面,允许用户输入消息并查看聊天历史。聊天机器人的响应会根据用户的输入和配置的参数进行生成。
"""




MODEL_LIST_CONTENT = """
            # Moonshot AI 模型列表

            本页面提供了 Moonshot AI 可用模型的实时列表。通过连接到 Moonshot AI 的 API，您可以查看和选择不同的模型来定制您的聊天体验。

            ## 功能

            - **模型获取**: 点击下方的按钮以获取当前可用的 Moonshot AI 模型列表。
            - **模型显示**: 获取的模型列表将在下方文本框中显示，供您选择和使用。

            ## 调用示例

            ### Python 调用

            要使用Python获取模型列表，您可以使用以下代码：

            ```python
            import os
            from openai import OpenAI

            # 创建 OpenAI 客户端实例
            client = OpenAI(
                api_key=os.getenv("MOONSHOT_API_KEY"),  # 从环境变量获取 API 密钥
                base_url="https://api.moonshot.cn/v1",  # Moonshot AI 的 API 基础 URL
            )

            # 获取模型列表
            model_list = client.models.list()
            model_data = model_list.data

            # 打印每个模型的 ID
            for i, model in enumerate(model_data):
                print(f"model[{i}]: {model.id}")
            ```

            ### CURL 调用

            要使用CURL获取模型列表，您可以在命令行中运行以下命令：

            ```bash
            curl https://api.moonshot.cn/v1/models \
            -H "Authorization: Bearer $MOONSHOT_API_KEY"
            ```

            请确保替换 `$MOONSHOT_API_KEY` 为您从 Moonshot AI 平台获取的实际API密钥。

            ## 请查看可用的模型，并选择最适合您需求的模型进行聊天。
"""
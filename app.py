# app.py (根目录)
import os
import importlib

# 定义一个函数来运行 Moonshot_API_Demo 的 app.run() 函数
def launch_all_demo():
    # 动态导入 Moonshot_API_Demo 应用的 app 模块
    app_module = importlib.import_module("Plays.Moonshot_API_Demo.app")
    # 调用 app 模块中的 run 函数来启动 Gradio 应用
    app_module.run()

# 检查是否直接运行了此脚本
if __name__ == "__main__":
    # 如果是直接运行此脚本，则启动 Moonshot_API_Demo 应用
    launch_all_demo()
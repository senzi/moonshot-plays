import gradio as gr
from config import Config
import importlib

# 创建一个简单的 Gradio 界面
def launch_play(play_name):
    # 动态构建导入路径
    module_path = f'Plays.{play_name}.app'
    
    # 使用 importlib 动态导入模块
    try:
        play_module = importlib.import_module(module_path)
        # 假设每个 app.py 都有一个 run 函数用于启动 Gradio 应用
        play_module.run()
    except ModuleNotFoundError as e:
        print(f"Error: {e}")

with gr.Blocks() as demo:
    play_name = gr.Radio(["Moonshot_API_Demo", "Moonshot_Iching_Demo"], value="Moonshot_API_demo", label="选择要启动的Demo")
    get_models_button = gr.Button("launch!")
    get_models_button.click(launch_play, inputs=play_name, outputs=None)


demo.queue()
demo.launch()


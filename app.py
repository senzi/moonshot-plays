# app.py

from config import Config
import importlib

def main():
    # 获取PLAY_NAME的值
    play_name = Config.PLAY_NAME
    print(f"The selected play is: {play_name}")

    # 动态构建导入路径
    # 假设play_name是'Moonshot_API_Demo'，我们需要将其转换为'Plays.Moonshot_API_Demo.app'
    module_path = f'Plays.{play_name}.app'
    
    # 使用importlib.import_module动态导入模块
    try:
        play_module = importlib.import_module(module_path)
        play_module.run()  # 假设app模块中有一个run函数用于启动应用
    except ModuleNotFoundError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
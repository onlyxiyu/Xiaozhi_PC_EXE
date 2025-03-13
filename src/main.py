import sys
import os
from PyQt6.QtWidgets import QApplication
from voice_interaction import VoiceInteraction
from network_client import AINetworkClient
from ui_main_window import MainWindow
from config_manager import ConfigManager

def main():
    # 获取程序运行路径
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        base_path = sys._MEIPASS
    else:
        # 开发时的路径
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Vosk 模型路径
    MODEL_PATH = os.path.join(base_path, "vosk-model-cn-kaldi-multicn-0.15")
    
    # 初始化配置管理器
    config_manager = ConfigManager()
    
    # 初始化模块
    voice_module = VoiceInteraction(MODEL_PATH, config_manager)
    network_client = AINetworkClient()
    
    # 设置已保存的 API Key
    network_client.set_api_key(config_manager.get_api_key())
    
    # 创建应用
    app = QApplication(sys.argv)
    window = MainWindow(voice_module, network_client, config_manager)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 
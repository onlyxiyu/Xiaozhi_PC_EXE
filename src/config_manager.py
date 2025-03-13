import json
import os
import sys

class ConfigManager:
    def __init__(self):
        # 获取程序所在目录
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        self.config_file = os.path.join(self.base_dir, "config.json")
        self.default_config = {
            "api_key": "",
            "voice": {
                "rate": "+2%",      # 语速
                "volume": "+5%"      # 音量
            },
            "tts_engine": "edge-tts"  # 默认使用 edge-tts
        }
        self.config = self.load_config()

    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 确保所有默认配置项都存在
                    return {**self.default_config, **config}
            except:
                return self.default_config
        return self.default_config

    def save_config(self, config):
        """保存配置文件"""
        self.config.update(config)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def get_api_key(self):
        """获取 API Key"""
        return self.config.get("api_key", "")

    def get_voice_settings(self):
        """获取语音设置"""
        return self.config.get("voice", self.default_config["voice"])

    def save_voice_settings(self, rate, volume):
        """保存语音设置"""
        self.config["voice"]["rate"] = rate
        self.config["voice"]["volume"] = volume
        self.save_config(self.config)

    def get_tts_engine(self):
        """获取当前使用的 TTS 引擎"""
        return self.config.get("tts_engine", self.default_config["tts_engine"])

    def set_tts_engine(self, engine):
        """设置 TTS 引擎"""
        self.config["tts_engine"] = engine
        self.save_config(self.config) 
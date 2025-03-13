import vosk
import sounddevice as sd
import json
import numpy as np
import threading
import queue
import time
import asyncio
import pygame
import tempfile
import os
from pygame import mixer
import sys
import aiohttp

class VoiceInteraction:
    def __init__(self, model_path, config_manager):
        # 处理 vosk DLL 路径
        if getattr(sys, 'frozen', False):
            vosk_dir = os.path.join(sys._MEIPASS, 'vosk')
            if os.path.exists(vosk_dir):
                os.add_dll_directory(vosk_dir)
        
        # 初始化 Vosk 语音识别模型
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        
        # 音频参数
        self.sample_rate = 16000
        self.channels = 1
        self.dtype = 'int16'
        
        # 录音状态
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.config_manager = config_manager

    async def _play_edge_tts(self, text):
        """使用 edge-tts 播放语音"""
        import edge_tts
        import os
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # 获取语音设置
                voice_settings = self.config_manager.get_voice_settings()
                
                # 获取程序运行目录下的 temp 文件夹
                if getattr(sys, 'frozen', False):
                    temp_dir = os.path.join(os.path.dirname(sys.executable), 'temp')
                else:
                    temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
                
                # 确保 temp 目录存在
                os.makedirs(temp_dir, exist_ok=True)
                
                # 使用程序目录下的临时文件
                temp_path = os.path.join(temp_dir, 'temp_audio.mp3')
                
                # 使用配置的参数
                communicate = edge_tts.Communicate(
                    text,
                    "zh-TW-HsiaoChenNeural",
                    rate=voice_settings["rate"],
                    volume=voice_settings["volume"]
                )

                # 设置超时
                timeout = aiohttp.ClientTimeout(total=10)
                
                # 保存到临时文件
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    communicate._session = session  # 使用自定义的会话
                    await communicate.save(temp_path)
                
                # 初始化 pygame 混音器
                mixer.init()
                mixer.music.load(temp_path)
                
                # 设置淡入淡出效果
                mixer.music.set_volume(0.0)
                mixer.music.play()
                
                # 淡入
                for i in range(10):
                    mixer.music.set_volume(i / 10.0)
                    await asyncio.sleep(0.05)
                
                # 等待播放完成
                while mixer.music.get_busy():
                    await asyncio.sleep(0.1)
                    
                # 淡出
                for i in range(10, 0, -1):
                    mixer.music.set_volume(i / 10.0)
                    await asyncio.sleep(0.02)
                    
                # 如果成功，跳出重试循环
                break
                
            except aiohttp.ClientError as e:
                print(f"网络错误 (尝试 {retry_count + 1}/{max_retries}): {e}")
                retry_count += 1
                if retry_count < max_retries:
                    await asyncio.sleep(1)  # 等待1秒后重试
                else:
                    print("无法连接到语音服务器，请检查网络连接")
                    
            except Exception as e:
                print(f"语音播放错误: {e}")
                break
                
            finally:
                try:
                    mixer.music.unload()
                    mixer.quit()
                    # 删除临时文件
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except:
                    pass

    def play_tts_response(self, text):
        """播放 TTS 响应"""
        text = self._process_text_for_tts(text)
        asyncio.run(self._play_edge_tts(text))

    def _process_text_for_tts(self, text):
        """优化的文本预处理"""
        import re
        
        # 基础清理
        text = text.strip()
        
        # 处理重复标点
        text = re.sub(r'([！？。，、；：])\1+', r'\1', text)
        
        # 添加语气词变音
        text = re.sub(r'([啊哦呢嘛哎呀]+)', r'\1～', text)
        text = re.sub(r'([\?！。])', r'～\1', text)
        
        # 处理笑声，使其更自然
        text = re.sub(r'哈哈+', '哈哈～', text)
        text = re.sub(r'呵呵+', '呵呵～', text)
        
        # 添加停顿和语气
        sentences = re.split(r'([。！？])', text)
        processed_sentences = []
        
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i]
            punct = sentences[i+1] if i+1 < len(sentences) else ""
            
            # 在逗号等处添加短停顿
            sentence = sentence.replace('，', '，...')
            sentence = sentence.replace('、', '、...')
            
            # 处理句尾
            if punct in '。！？':
                processed_sentences.append(f"{sentence}{punct}......")
            else:
                processed_sentences.append(f"{sentence}{punct}")
        
        text = ''.join(processed_sentences)
        
        # 添加台湾用语特色
        text = text.replace('什么', '什麼')
        text = text.replace('这个', '這個')
        text = text.replace('那个', '那個')
        
        return text

    def start_listening(self, callback=None, duration=5):
        """
        开始录音并返回识别结果
        :param callback: 识别完成后的回调函数
        :param duration: 录音时长（秒）
        """
        if self.is_recording:
            return
            
        self.is_recording = True
        
        def record_audio():
            print("开始录音...")
            
            # 录制音频
            recording = sd.rec(
                int(duration * self.sample_rate), 
                samplerate=self.sample_rate, 
                channels=self.channels,
                dtype=self.dtype
            )
            sd.wait()
            
            # 转换为 numpy 数组
            audio_data = recording.flatten().astype(np.int16)
            
            # 语音识别
            if self.recognizer.AcceptWaveform(audio_data.tobytes()):
                result = json.loads(self.recognizer.Result())
                text = result.get('text', '')
            else:
                text = ''
                
            self.is_recording = False
            
            # 如果有回调函数，调用它
            if callback:
                callback(text)
            else:
                self.audio_queue.put(text)
                
        # 在新线程中录音，避免阻塞主线程
        threading.Thread(target=record_audio).start()
        
        # 如果没有回调，则等待结果
        if not callback:
            while self.is_recording:
                time.sleep(0.1)
            return self.audio_queue.get()

    def _process_audio(self, audio_data):
        """音频后处理"""
        from scipy import signal
        import numpy as np
        
        # 转换为 numpy 数组
        audio = np.frombuffer(audio_data, dtype=np.int16)
        
        # 添加轻微混响
        b, a = signal.butter(3, 0.1)
        reverb = signal.lfilter(b, a, audio)
        
        # 混合原声和混响
        processed = 0.8 * audio + 0.2 * reverb
        
        return processed.astype(np.int16).tobytes() 
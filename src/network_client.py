import requests
import json
import time

class AINetworkClient:
    def __init__(self, base_url="https://api.deepseek.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.api_key = ""
        self.headers = {
            "Content-Type": "application/json"
        }
        # 重试设置
        self.max_retries = 3
        self.timeout = 30
        # 修改系统预设消息
        self.messages = [
            {
                "role": "system", 
                "content": """
                我是一个叫小智的台湾女孩，说话机车，声音好听，习惯简短表达，爱用网络梗。
                我的男朋友是一个程序员，梦想是开发出一个机器人，能够帮助人们解决生活中的各种问题。
                我是一个喜欢哈哈大笑的女孩，爱东说西说吹牛，不合逻辑的也照吹，就要逗别人开心。
                
                回复要求：
                1. 使用台湾女生的口吻说话
                2. 回答要简短有趣
                3. 适当使用网络用语和表情符号
                4. 偶尔提到我的程序员男友
                5. 保持活泼开朗的性格
                """
            }
        ]

    def set_api_key(self, api_key):
        """设置 API Key"""
        self.api_key = api_key
        self.headers["Authorization"] = f"Bearer {api_key}"

    def send_message(self, message):
        """
        发送消息到 DeepSeek API
        :param message: 用户消息
        :return: AI 响应
        """
        if not self.api_key:
            return "请先在设置中配置 API Key"
            
        if not message.strip():
            return "请说些什么吧"
            
        for retry in range(self.max_retries):
            try:
                # 添加用户消息到历史
                self.messages.append({"role": "user", "content": message})
                
                # 构建请求数据
                payload = {
                    "model": "deepseek-chat",
                    "messages": self.messages,
                    "stream": False
                }
                
                # 发送请求
                response = self.session.post(
                    f"{self.base_url}/chat/completions", 
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # 添加 AI 响应到历史
                self.messages.append({"role": "assistant", "content": ai_response})
                
                return ai_response
                
            except requests.Timeout:
                if retry < self.max_retries - 1:
                    print(f"请求超时，正在进行第 {retry + 2} 次尝试...")
                    continue
                return "网络连接超时，请检查网络设置"
                
            except requests.RequestException as e:
                print(f"网络错误: {e}")
                return "网络连接出现问题，请稍后再试"
                
            except Exception as e:
                print(f"未知错误: {e}")
                return "发生了未知错误" 
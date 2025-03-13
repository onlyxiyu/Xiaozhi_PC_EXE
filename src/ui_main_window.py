from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QPushButton, QWidget, QLabel,
    QStatusBar, QSplitter, QFrame, QLineEdit,
    QDialog, QDialogButtonBox, QGroupBox, QSlider
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QTextCursor

# 添加设置对话框类
class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("设置")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # API Key 设置
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("DeepSeek API Key:")
        self.api_key_input = QLineEdit(config_manager.config.get("api_key", ""))
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        layout.addLayout(api_key_layout)
        
        # 语音设置
        voice_group = QGroupBox("语音设置")
        voice_layout = QVBoxLayout()
        
        # 语速设置
        rate_layout = QHBoxLayout()
        rate_label = QLabel("语速调整:")
        self.rate_slider = QSlider(Qt.Orientation.Horizontal)
        self.rate_slider.setRange(-10, 10)
        self.rate_slider.setValue(self._parse_percentage(config_manager.config["voice"]["rate"]))
        self.rate_value = QLabel(f"{self.rate_slider.value()}%")
        self.rate_slider.valueChanged.connect(lambda v: self.rate_value.setText(f"{v}%"))
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(self.rate_slider)
        rate_layout.addWidget(self.rate_value)
        voice_layout.addLayout(rate_layout)
        
        # 音量设置
        volume_layout = QHBoxLayout()
        volume_label = QLabel("音量调整:")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(-10, 10)
        self.volume_slider.setValue(self._parse_percentage(config_manager.config["voice"]["volume"]))
        self.volume_value = QLabel(f"{self.volume_slider.value()}%")
        self.volume_slider.valueChanged.connect(lambda v: self.volume_value.setText(f"{v}%"))
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_value)
        voice_layout.addLayout(volume_layout)
        
        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _parse_percentage(self, value):
        """解析百分比字符串"""
        try:
            return int(value.strip('%').strip('+').strip('-'))
        except:
            return 0

    def get_settings(self):
        """获取设置值"""
        return {
            "api_key": self.api_key_input.text().strip(),
            "voice": {
                "rate": f"+{self.rate_slider.value()}%",
                "volume": f"+{self.volume_slider.value()}%"
            }
        }

class MainWindow(QMainWindow):
    def __init__(self, voice_module, network_client, config_manager):
        super().__init__()
        self.voice_module = voice_module
        self.network_client = network_client
        self.config_manager = config_manager
        
        # 设置窗口属性
        self.setWindowTitle("小智 AI 助手")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # 创建中心窗口和布局
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("小智 AI 助手")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(title_label)
        
        # 分割线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)
        
        # 聊天历史
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setFont(QFont("Arial", 12))
        self.chat_history.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.chat_history)
        
        # 底部按钮区域
        button_layout = QHBoxLayout()
        
        # 语音交互按钮
        self.talk_button = QPushButton("开始语音交互")
        self.talk_button.setFont(QFont("Arial", 12))
        self.talk_button.setMinimumHeight(50)
        self.talk_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.talk_button.clicked.connect(self.handle_voice_interaction)
        button_layout.addWidget(self.talk_button)
        
        # 设置按钮
        self.settings_button = QPushButton("设置")
        self.settings_button.setFont(QFont("Arial", 12))
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.settings_button.clicked.connect(self.show_settings)
        button_layout.addWidget(self.settings_button)
        
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        # 初始化聊天历史
        self.init_chat_history()

    def init_chat_history(self):
        """初始化聊天历史"""
        welcome_message = "欢迎使用小智 AI 助手！点击下方按钮开始语音交互。"
        self.chat_history.append(f"<p style='color:#4CAF50'><b>小智:</b> {welcome_message}</p>")

    def handle_voice_interaction(self):
        """处理语音交互"""
        # 更新按钮状态
        self.talk_button.setEnabled(False)
        self.talk_button.setText("正在录音...")
        self.statusBar.showMessage("正在录音，请说话...")
        
        def on_recognition_complete(text):
            # 恢复按钮状态
            self.talk_button.setEnabled(True)
            self.talk_button.setText("开始语音交互")
            
            if text:
                # 显示用户消息
                self.chat_history.append(f"<p style='color:#2196F3'><b>用户:</b> {text}</p>")
                self.statusBar.showMessage("正在处理您的请求...")
                
                # 发送到 AI 服务器
                ai_response = self.network_client.send_message(text)
                
                # 显示 AI 响应
                self.chat_history.append(f"<p style='color:#4CAF50'><b>小智:</b> {ai_response}</p>")
                
                # 滚动到底部
                self.chat_history.moveCursor(QTextCursor.MoveOperation.End)
                
                # 播放 AI 响应
                self.voice_module.play_tts_response(ai_response)
                self.statusBar.showMessage("就绪")
            else:
                self.statusBar.showMessage("未能识别您的语音，请重试")
        
        # 开始语音识别
        self.voice_module.start_listening(callback=on_recognition_complete)

    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(
            self.config_manager, 
            self
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            self.config_manager.save_config(settings)
            self.network_client.set_api_key(settings["api_key"])
            self.statusBar.showMessage("设置已保存", 3000) 
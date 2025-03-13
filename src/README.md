# 小智 AI 助手

一个基于语音交互的 AI 聊天助手，具有语音识别和语音合成功能。小智以台湾女生的形象与用户进行对话，提供自然、有趣的交互体验。

## 作者信息

- 作者：饩雨 (God_xiyu)
- 邮箱：mai_xiyu@vip.qq.com

## 功能特点

- **语音识别**：使用 Vosk 实现离线语音识别，支持中文普通话
- **语音合成**：使用 Edge TTS 实现自然语音播放，模拟台湾女生声音
- **AI 对话**：使用 DeepSeek API 实现智能对话，具有记忆功能
- **图形界面**：使用 PyQt6 实现现代化界面，简洁易用
- **配置管理**：支持保存 API Key 和语音设置

## 安装要求

- Python 3.8 或更高版本
- Windows 操作系统（其他系统未测试）
- 网络连接（用于 AI 对话和语音合成）
- 麦克风（用于语音输入）
- DeepSeek API Key（需要自行申请）

## 依赖包 

numpy==1.24.3
requests==2.30.0
edge-tts==6.1.9
pygame==2.5.2
pyinstaller==6.3.0
vosk==0.3.45
sounddevice==0.4.6
aiohttp==3.9.1
Pillow==10.1.0

## 安装步骤

1. 克隆或下载项目代码
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 下载 Vosk 中文语音模型，放在项目根目录：
   - 模型名称：vosk-model-cn-kaldi-multicn-0.15
   - 下载地址：https://alphacephei.com/vosk/models
   - 模型位置：项目根目录/vosk-model-cn-kaldi-multicn-0.15/

## 运行方式
 
### 开发环境运行
python main.py 

### 打包为可执行文件

```
python build.py
```

打包后的文件在 dist/XiaoZhi 目录下，直接运行 XiaoZhi.exe 即可。

## 使用说明

1. **首次使用配置**：
   - 点击界面右下角的"设置"按钮
   - 输入您的 DeepSeek API Key
   - 调整语音的语速和音量
   - 点击"确定"保存设置

2. **开始对话**：
   - 点击"开始语音交互"按钮
   - 对着麦克风说话（录音约5秒）
   - 等待 AI 回复并播放语音

3. **查看对话历史**：
   - 所有对话都会显示在主界面的文本区域
   - 用户消息和 AI 回复有不同的颜色标识

## 常见问题及解决方案

### 1. 语音播放错误

**错误信息**：
```
语音播放错误: Cannot connect to host speech.platform.bing.com:443
```

**解决方案**：
- 检查网络连接是否正常
- 确认防火墙未阻止程序访问网络
- 等待几秒后重试
- 如果问题持续，可能是 Microsoft 服务暂时不可用，请稍后再试

### 2. 找不到 Vosk 模型

**错误信息**：
```
FileNotFoundError: [WinError 2] 系统找不到指定的文件
```

**解决方案**：
- 确保 vosk-model-cn-kaldi-multicn-0.15 文件夹在正确位置
- 检查模型文件是否完整
- 重新下载并解压模型文件

### 3. API Key 相关错误

**错误信息**：
```
请先在设置中配置 API Key
```
或
```
网络错误: 401 Client Error
```

**解决方案**：
- 在设置中填入有效的 DeepSeek API Key
- 确保 API Key 格式正确
- 检查 API Key 是否已过期或超出使用限制

### 4. 语音识别问题

**问题**：语音识别不准确或无法识别

**解决方案**：
- 确保麦克风工作正常
- 减少环境噪音
- 靠近麦克风说话
- 说话速度适中，发音清晰

## 技术细节

- **语音识别**：使用 Vosk 进行离线语音识别，支持中文
- **语音合成**：使用 Microsoft Edge TTS 服务，选用台湾女声
- **AI 对话**：使用 DeepSeek API，支持上下文记忆
- **界面框架**：使用 PyQt6 构建现代化界面
- **配置管理**：使用 JSON 文件存储配置

## 项目结构

```
src/
├── main.py              # 主程序入口
├── voice_interaction.py # 语音交互模块
├── network_client.py    # 网络通信模块
├── ui_main_window.py    # 用户界面
├── config_manager.py    # 配置管理
├── build.py             # 打包脚本
├── create_icon.py       # 图标生成
└── resources/           # 资源文件
    └── icon.ico         # 程序图标
```

## 注意事项

1. 程序需要管理员权限运行
2. 需要稳定的网络连接
3. 配置文件保存在程序目录下的 config.json
4. 临时文件保存在 temp 目录
5. DeepSeek API 可能有使用限制和费用，请参考官方文档

## 隐私说明

- 所有语音数据仅用于识别和处理，不会保存
- 对话内容会发送到 DeepSeek 服务器进行处理
- 配置信息仅保存在本地，不会上传

## 许可证

MIT License

## 更新日志

### v1.0.0 (2025-03-13)
- 初始版本发布
- 实现基本的语音交互功能
- 支持 DeepSeek API 对话
- 添加语音参数设置

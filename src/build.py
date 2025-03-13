import PyInstaller.__main__
import os
import shutil
import site
import glob
import vosk  # 导入 vosk 来获取其路径

def build_exe():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    # 创建 dist 目录
    dist_dir = os.path.join(parent_dir, "dist")
    xiaozhi_dir = os.path.join(dist_dir, "XiaoZhi")
    
    # 清理旧的构建目录
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # 获取 vosk 目录
    vosk_dir = os.path.dirname(vosk.__file__)
    vosk_dll = glob.glob(os.path.join(vosk_dir, '*.dll'))
    
    print(f"Vosk directory: {vosk_dir}")  # 打印路径以便调试
    
    # PyInstaller 参数
    params = [
        'main.py',                          # 主程序文件
        '--name=XiaoZhi',                   # 可执行文件名
        '--noconsole',                      # 不显示控制台
        '--onedir',                         # 生成目录形式
        '--add-data=../vosk-model-cn-kaldi-multicn-0.15;vosk-model-cn-kaldi-multicn-0.15',  # 添加模型文件
        '--icon=resources/icon.ico',        # 图标
        '--clean',                          # 清理临时文件
        '--add-binary=../config.json;.',    # 添加配置文件
        f'--add-data={vosk_dir};vosk',     # 添加 vosk 目录
        '--hidden-import=edge_tts',         # 添加隐式导入
        '--hidden-import=vosk',
        '--hidden-import=sounddevice',
        '--hidden-import=numpy',
        '--hidden-import=pygame',
        '--collect-all=vosk',              # 收集所有 vosk 相关文件
        '-y',                              # 自动覆盖输出目录
    ]
    
    # 添加所有 vosk DLL 文件
    for dll in vosk_dll:
        if os.path.exists(dll):  # 确保文件存在
            print(f"Adding DLL: {dll}")  # 打印 DLL 路径以便调试
            params.append(f'--add-binary={dll};.')
    
    # 运行 PyInstaller
    PyInstaller.__main__.run(params)
    
    # 创建 temp 目录
    temp_dir = os.path.join(xiaozhi_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    print("打包完成！")

if __name__ == "__main__":
    build_exe() 
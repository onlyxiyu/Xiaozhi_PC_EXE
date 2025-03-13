from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 创建一个 256x256 的图像
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    circle_color = (76, 175, 80)  # 绿色
    draw.ellipse([10, 10, size-10, size-10], fill=circle_color)
    
    # 添加文字
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()
        
    text = "智"
    text_color = (255, 255, 255)  # 白色
    
    # 计算文字位置使其居中
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # 绘制文字
    draw.text((x, y), text, font=font, fill=text_color)
    
    # 确保目录存在
    os.makedirs('resources', exist_ok=True)
    
    # 保存为 ICO 文件
    image.save('resources/icon.ico', format='ICO', sizes=[(256, 256)])

if __name__ == "__main__":
    create_icon() 
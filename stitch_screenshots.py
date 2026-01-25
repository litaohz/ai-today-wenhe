"""
改进的拼接脚本 - 确保页脚二维码完整
使用更简单的逻辑：直接按scrollY位置paste对应内容
"""
from PIL import Image
import os

# 截图文件路径
screenshot_dir = r"C:\Users\98554\.gemini\antigravity\brain\e5c23aea-7e53-4d8a-8bab-cc80dfaf5a07"
output_path = r"C:\Users\98554\Downloads\ai-today-wenhe\archives-260119\ai_posts_summary_2026-01-19_fullpage.png"

# 按顺序列出分段截图文件
segment_files = [
    ("clean_seg_1_1768888213685.png", 0),         # scrollY = 0
    ("clean_seg_2_1768888227590.png", 800),       # scrollY = 800
    ("clean_seg_3_1768888243904.png", 1600),      # scrollY = 1600
    ("clean_seg_4_1768888260402.png", 2400),      # scrollY = 2400
    ("clean_seg_5_1768888280100.png", 3200),      # scrollY = 3200
    ("clean_seg_6_1768888298578.png", 4000),      # scrollY = 4000
    ("clean_seg_7_footer_1768888319627.png", -1), # 页面底部（特殊处理）
]

# 加载第一张获取viewport尺寸
first_img = Image.open(os.path.join(screenshot_dir, segment_files[0][0]))
width = first_img.width
viewport_height = first_img.height
print(f"Viewport: {width} x {viewport_height}")

# 加载所有截图
images = []
for f, scroll_y in segment_files:
    img_path = os.path.join(screenshot_dir, f)
    if os.path.exists(img_path):
        img = Image.open(img_path)
        images.append((img, scroll_y, f))
        print(f"Loaded: {f}, size: {img.size}, scrollY: {scroll_y}")
    else:
        print(f"Warning: {f} not found")

# 页面总高度 = 最后一个scrollY位置 + viewport高度
# 或者使用segment_6的位置计算: 4000 + viewport_height
# 但footer截图是滚动到底部，所以我们需要计算精确的高度
# 从之前的测量: page_height = 5332

page_height = 5332
scroll_step = 800

print(f"Page height: {page_height}")

# 创建最终图像
final_image = Image.new('RGB', (width, page_height), (255, 255, 255))

# 简单策略：每张截图直接paste到scrollY位置
# 后面的截图会覆盖前面重叠的部分（这是期望的）
for img, scroll_y, fname in images[:-1]:  # 除了最后一张
    final_image.paste(img, (0, scroll_y))
    print(f"{fname}: pasted at y={scroll_y}")

# 最后一张（footer）需要特殊处理
# scrollY = page_height - viewport_height
footer_img = images[-1][0]
footer_scroll_y = page_height - viewport_height
final_image.paste(footer_img, (0, footer_scroll_y))
print(f"Footer: pasted at y={footer_scroll_y}")

# 保存最终图像
final_image.save(output_path, 'PNG', optimize=True)
print(f"\nSaved to: {output_path}")
print(f"Final size: {final_image.size}")

# 验证页脚区域
footer_crop = final_image.crop((0, page_height - 600, width, page_height))
footer_crop.save(output_path.replace('.png', '_footer_verify.png'), 'PNG')
print("Footer verification saved")

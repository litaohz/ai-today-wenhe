"""
手动裁剪拼接的截图，移除紫色侧边栏
"""
from PIL import Image

input_path = r"C:\Users\98554\Downloads\ai-today-wenhe\archives-260119\ai_posts_summary_2026-01-19_fullpage.png"
output_path = r"C:\Users\98554\Downloads\ai-today-wenhe\archives-260119\ai_posts_summary_2026-01-19_fullpage_final.png"

# 打开图片
img = Image.open(input_path)
print(f"Original size: {img.size}")

width, height = img.size

# 检查一列像素的颜色
pixels = img.load()

# 打印第一行一些采样点的颜色
print("Sampling pixels at y=500:")
for x in [0, 50, 100, 150, 180, 200, 250, 300, 400, 600, 800, 1000, 1100]:
    if x < width:
        print(f"  x={x}: {pixels[x, 500][:3]}")

# 通过观察找到内容区域边界
# 基于之前的截图，内容宽度约800px，居中在1179px视窗中
# 左边距大约 (1179 - 800) / 2 = 189.5px
# 所以内容从约 x=190 开始，到 x=990 结束

# 但实际上看图片，紫色区域可能只是很淡的渐变
# 让我检查是否有明显的颜色变化

# 找到第一个不是紫色渐变背景的列
left_crop = 0
for x in range(width):
    # 检查多个高度位置
    samples = [pixels[x, 200], pixels[x, 500], pixels[x, 1000], pixels[x, 2000]]
    all_light_purple = True
    for p in samples:
        r, g, b = p[:3]
        # 渐变紫色的特征: R在220-250, G在210-240, B在245-255
        if not (r > 210 and g > 210 and b > 240 and b > r):
            all_light_purple = False
            break
    if not all_light_purple:
        left_crop = max(0, x - 2)
        break

# 从右边找
right_crop = width
for x in range(width - 1, -1, -1):
    samples = [pixels[x, 200], pixels[x, 500], pixels[x, 1000], pixels[x, 2000]]
    all_light_purple = True
    for p in samples:
        r, g, b = p[:3]
        if not (r > 210 and g > 210 and b > 240 and b > r):
            all_light_purple = False
            break
    if not all_light_purple:
        right_crop = min(width, x + 3)
        break

print(f"Detected content: x={left_crop} to x={right_crop}")

# 如果检测到的区域合理，裁剪
if right_crop - left_crop > 600:  # 至少600px宽
    cropped = img.crop((left_crop, 0, right_crop, height))
else:
    # 如果检测失败，使用整张图
    cropped = img
    print("Detection failed, using original")

print(f"Final size: {cropped.size}")
cropped.save(output_path, 'PNG', optimize=True)
print(f"Saved to: {output_path}")

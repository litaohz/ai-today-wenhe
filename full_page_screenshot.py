"""
全页面截图脚本
使用 Playwright 将 HTML 页面转换为一张完整的长图
"""
from playwright.sync_api import sync_playwright
import sys
from pathlib import Path

def capture_full_page_screenshot(url, output_path, viewport_width=800):
    """
    捕获完整页面截图
    
    Args:
        url: 要截图的 URL
        output_path: 输出图片路径
        viewport_width: 视口宽度（默认 800px）
    """
    with sync_playwright() as p:
        # 启动浏览器（使用 Chromium）
        browser = p.chromium.launch(headless=True)
        
        # 创建新页面，设置视口大小
        page = browser.new_page(
            viewport={'width': viewport_width, 'height': 1200}
        )
        
        print(f"正在打开页面: {url}")
        # 访问页面
        page.goto(url, wait_until='networkidle')
        
        # 等待图片加载完成
        print("等待所有图片加载...")
        page.wait_for_load_state('networkidle')
        
        # 额外等待以确保所有资源都已加载
        page.wait_for_timeout(3000)
        
        # 注入 CSS 移除焦点边框
        page.add_style_tag(content="""
            * {
                outline: none !important;
                box-shadow: none !important;
            }
        """)
        
        print("正在截取完整页面...")
        # 截取全页面（full_page=True 会自动滚动并捕获整个页面）
        page.screenshot(
            path=output_path,
            full_page=True
        )
        
        print(f"截图已保存到: {output_path}")
        
        # 关闭浏览器
        browser.close()
        
        return True

if __name__ == "__main__":
    # 默认配置
    url = "http://localhost:3000/archives-260119/ai_posts_summary_2026-01-19.html"
    output_path = "archives-260119/ai_posts_summary_2026-01-19_full_page.png"
    
    # 允许通过命令行参数自定义
    if len(sys.argv) > 1:
        url = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    # 确保输出目录存在
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # 执行截图
    try:
        capture_full_page_screenshot(url, output_path)
        print("✅ 截图成功完成！")
    except Exception as e:
        print(f"❌ 截图失败: {e}")
        sys.exit(1)

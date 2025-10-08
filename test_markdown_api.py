"""测试 Markdown API 端点"""
import requests
import json

def test_markdown_endpoint():
    """测试获取 Markdown 内容的端点"""
    
    # 测试日期
    test_date = "2025-10-07"
    
    # API 端点
    url = f"http://localhost:8000/api/v1/scheduler/markdown/{test_date}"
    
    print(f"测试 API: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data.get('success')}")
            print(f"日期: {data.get('date')}")
            print(f"内容长度: {len(data.get('content', ''))}")
            print(f"文件路径: {data.get('file_path')}")
            
            # 显示内容的前 200 个字符
            content = data.get('content', '')
            if content:
                print(f"\n内容预览:\n{content[:200]}...")
        else:
            print(f"错误: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到 API 服务器。请确保后端服务正在运行。")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_markdown_endpoint()

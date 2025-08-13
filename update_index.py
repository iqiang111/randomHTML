import os
import re
from datetime import datetime

# 生成map.html的脚本
# 该脚本扫描指定目录下的所有HTML文件和包含index.html的文件
# 配置信息 - 请根据你的服务器情况修改这些值
SERVER_ROOT = '/www/wwwroot/qinag.fun'  # Nginx服务器根目录
DOMAIN = 'https://qinag.fun'  # 你的域名
INDEX_FILE = os.path.join(SERVER_ROOT, 'map.html')  # 要更新的map.html路径
EXCLUDE_FILES = ['index.html','map.html']  # 要排除的文件

def get_html_title(file_path):
    """从HTML文件中提取<title>标签内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 使用正则表达式匹配title标签
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
            return os.path.basename(file_path)  # 如果没有title标签，使用文件名
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return os.path.basename(file_path)

def scan_files():
    """扫描服务器根目录，获取所有HTML文件和包含index.html的文件夹"""
    links = []
    
    # 遍历服务器根目录
    for item in os.listdir(SERVER_ROOT):
        item_path = os.path.join(SERVER_ROOT, item)
        
        # 跳过要排除的文件
        if item in EXCLUDE_FILES:
            continue
            
        # 处理HTML文件
        if os.path.isfile(item_path) and item.endswith('.html'):
            title = get_html_title(item_path)
            # uri = f"{DOMAIN}/{item}"
            # 删除 .html 后缀
            base_name = os.path.splitext(item)[0]
            uri = f"{DOMAIN}/{base_name}"
            links.append((title, uri))
            
        # 处理包含index.html的文件夹
        elif os.path.isdir(item_path):
            index_path = os.path.join(item_path, 'index.html')
            if os.path.exists(index_path):
                title = get_html_title(index_path)
                uri = f"{DOMAIN}/{item}/"
                links.append((title, uri))
    
    # 按标题排序链接
    return sorted(links, key=lambda x: x[0].lower())

def update_index(links):
    """更新index.html文件，添加所有链接"""
    # 生成HTML内容
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>网站内容索引</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📚</text></svg>">
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --background-color: #f5f6fa;
            --text-color: #2d3436;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
        }}

        h1 {{
            color: var(--primary-color);
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .link-list {{
            list-style: none;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }}

        .link-list li {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease-in-out;
        }}

        .link-list li:hover {{
            transform: translateY(-5px);
        }}

        .link-list a {{
            display: block;
            padding: 1.5rem;
            text-decoration: none;
            color: var(--secondary-color);
            font-weight: 500;
        }}

        .updated {{
            color: #6c757d;
            font-size: 0.9em;
            text-align: center;
            margin-top: 2rem;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <h1>📚 网站内容索引</h1>
    <ul class="link-list">
"""
    # 添加所有链接
    for title, uri in links:
        html_content += f'        <li><a href="{uri}">{title}</a></li>\n'
    
    # 添加更新时间并结束HTML
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content += f"""    </ul>
    <p class="updated">最后更新: {update_time}</p>
</body>
</html>
"""
    
    # 写入到index.html文件
    try:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"成功更新 {INDEX_FILE}，共添加 {len(links)} 个链接")
    except Exception as e:
        print(f"更新 {INDEX_FILE} 时出错: {e}")
        
def main():
    """主函数"""
    print("开始扫描文件...")
    links = scan_files()
    print(f"找到 {len(links)} 个有效链接")
    update_index(links)
    print("操作完成")

if __name__ == "__main__":
    main()

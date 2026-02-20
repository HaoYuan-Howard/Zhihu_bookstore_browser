import requests


def save_webpage_as_html(url, file_path, headers):
    """
    将指定URL的网页内容保存为.html文件。

    参数:
    - url: 网页的URL
    - file_path: 保存的文件路径，包含文件名，例如 "saved_page.html"
    """

    try:
        # 发送请求获取网页内容
        response = requests.get(url,headers=headers)

        # 检查请求是否成功
        if response.status_code == 200:
            # 将内容写入文件
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"网页内容已成功保存为 {file_path}")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误: {e}")




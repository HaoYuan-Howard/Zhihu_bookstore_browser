# code/main/html_2_md.py
"""
爬取书架中的小说
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(project_root)  # 将项目根目录添加到路径

from Spider_Zhihu_Novel.Spider_zhihu.url_2_html import save_webpage_as_html
from Spider_Zhihu_Novel.markdown_ddddocr.md_ddddocr_shujia import main
from Spider_Zhihu_Novel.Spider_zhihu.parse_html_2_ttf_shujia import extract_base64_font
from Spider_Zhihu_Novel.Spider_zhihu.parse_html_2_md import extract_paragraphs_to_md
from Novel_Process.truncate_md import truncate_md_after_keyword


def clean_cookie(cookie):
    """清理 Cookie 值中的无效字符"""
    return cookie.replace("\n", "").strip()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("用法: python script.py <cookie> <url> <zhihu_html> <zhihu_md>")
        sys.exit(1)

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    cookie = sys.argv[1]
    cookie = clean_cookie(cookie)
    url = sys.argv[2]
    # 抓包后的网址内容
    zhihu_html = sys.argv[3]
    zhihu_html = zhihu_html.replace("\\", "/")
    # Save novel as markdown
    zhihu_md = sys.argv[4]
    zhihu_md = zhihu_md.replace("\\", '/')

    headers = {
        "User-Agent": user_agent,
        "Cookie": cookie
    }

    # 抓包后的网址内容
    # Save ttf file
    zhihu_ttf = r"E:\practice_group\generate_novel\material\ttf\zhihu.ttf"
    # Temporarily store ttf rendered glyph images
    glyph_image_dir = r"E:\practice_group\generate_novel\material\ttf\glyph_image"
    # Save novel as markdown
    # 解决符号加密
    replace_dict = {
        "o": '。',
        "2": '？',
        "l": '!',
        "上": ']',
        "r": '',
        ";": "：",
        "厂": ""
    }

    save_webpage_as_html(url, zhihu_html, headers)

    extract_base64_font(zhihu_html, zhihu_ttf)  # extract ttf font from html with base64
    extract_paragraphs_to_md(zhihu_html, zhihu_md)  # extract novel from html with p tags
    # 最后运行结果
    main(zhihu_ttf, glyph_image_dir, zhihu_md, replace_dict=replace_dict)
    truncate_md_after_keyword(zhihu_md)

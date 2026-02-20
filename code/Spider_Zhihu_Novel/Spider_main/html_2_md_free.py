"""
爬取书架中的小说
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir,os.pardir))
sys.path.append(project_root) # 将项目根目录添加到路径

from Novel_Process.truncate_md import truncate_md_after_keyword
from Spider_Zhihu_Novel.Spider_zhihu.parse_html_2_md import extract_paragraphs_to_md


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python script.py <zhihu_html> <zhihu_md>")
        sys.exit(1)

    zhihu_html = sys.argv[1]  # Captured HTML file
    zhihu_html = zhihu_html.replace("\\", "/")

    # Save novel as markdown
    zhihu_md = sys.argv[2]
    zhihu_md = zhihu_md.replace("\\", '/')

    extract_paragraphs_to_md(zhihu_html, zhihu_md) # extract novel from html with p tags
    truncate_md_after_keyword(zhihu_md)

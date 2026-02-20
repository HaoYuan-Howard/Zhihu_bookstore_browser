# code/main/html_2_md.py

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir,os.pardir))
sys.path.append(project_root) # 将项目根目录添加到路径

from Spider_Zhihu_Novel.markdown_ddddocr.md_ddddocr import main
from Spider_Zhihu_Novel.Spider_zhihu.parse_html_2_ttf import extract_base64_font
from Spider_Zhihu_Novel.Spider_zhihu.parse_html_2_md import extract_paragraphs_to_md
from Novel_Process.truncate_md import truncate_md_after_keyword


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python script.py <zhihu_html> <zhihu_md>r")
        sys.exit(1)

    zhihu_html = sys.argv[1] # Captured HTML file
    zhihu_html = zhihu_html.replace("\\", "/")
    zhihu_ttf = r"E:\practice_group\generate_novel\material\ttf\zhihu.ttf" # Save ttf file
    zhihu_md = sys.argv[2] # Save novel as markdown
    zhihu_md = zhihu_md.replace("\\", '/')
    extract_base64_font(zhihu_html, zhihu_ttf) # extract ttf font from html with base64
    extract_paragraphs_to_md(zhihu_html, zhihu_md) # extract novel from html with p tags

    glyph_image_dir = r"E:\practice_group\generate_novel\material\ttf\glyph_image" # Temporarily store ttf rendered glyph images
    main(zhihu_ttf,glyph_image_dir,zhihu_md)
    truncate_md_after_keyword(zhihu_md)
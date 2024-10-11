# code/main/html_2_md.py

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir,os.pardir))
sys.path.append(project_root) # 将项目根目录添加到路径

from markdown_ddddocr.md_ddddocr import main
from Spider_zhihu.parse_html_2_ttf import extract_base64_font
from Spider_zhihu.parse_html_2_md import extract_paragraphs_to_md


if __name__ == "__main__":
    html_path = r"E:\practice_group\generate_novel\material\html\zhihu.html" # Captured HTML file
    zhihu_ttf = r"E:\practice_group\generate_novel\material\ttf\zhihu.ttf" # Save ttf file
    zhihu_md = r"E:\practice_group\generate_novel\material\md_novel\zhihu.md" # Save novel as markdown
    extract_base64_font(html_path, zhihu_ttf) # extract ttf font from html with base64
    extract_paragraphs_to_md(html_path, zhihu_md) # extract novel from html with p tags

    glyph_image_dir = r"E:\practice_group\generate_novel\material\ttf\glyph_image" # Temporarily store ttf rendered glyph images
    main(zhihu_ttf,glyph_image_dir,zhihu_md)
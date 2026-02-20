import os
import re
from docx import Document
import sys


# 删除独立数字行
def remove_numbers_from_word(doc_path, output_path):
    doc = Document(doc_path)

    regex = re.compile(
        r'^\s*(\d+|\d+、|\d+.|\d+）|（\d+）|（[一二三四五六七八九十百千万亿]+）|[一二三四五六七八九十百千万亿]+)\s*$')

    for para in doc.paragraphs:
        # 使用正则表达式替换掉段落中的数字
        para.text = regex.sub('', para.text)

    doc.save(output_path)


# 删除多余空白行
def remove_extra_blank_lines(doc_path, output_path):
    doc = Document(doc_path)
    paragraphs_to_remove = []

    # 遍历文档中的段落，查找连续的三个空白行
    for i in range(len(doc.paragraphs) - 2):
        # 检查当前段落及接下来两个段落是否都是空白的
        if not doc.paragraphs[i].text.strip() and not doc.paragraphs[i+1].text.strip() and not doc.paragraphs[i+2].text.strip():
            # 如果是，标记后两个段落为删除
            paragraphs_to_remove.append(i+1)
            paragraphs_to_remove.append(i+2)
            # 跳过已经检查过的段落
            i += 2

    # 从后往前删除段落，避免索引变化导致的问题
    for i in sorted(set(paragraphs_to_remove), reverse=True):
        p = doc.paragraphs[i]._element
        p.getparent().remove(p)

    doc.save(output_path)


def remove_quotes_from_docx(input_path, output_path):

    doc = Document(input_path)
    new_doc = Document()
    for para in doc.paragraphs:
        # 去除每段中的空格
        text_without_whitespace = re.sub(r'\s+', '', para.text)

        # 使用正则表达式替换开头的「和结尾的」符号
        new_text = re.sub(r'^「', '', text_without_whitespace)  # 去除段落开头的「
        new_text = re.sub(r'」$', '', new_text)  # 去除段落结尾的」
        new_text = re.sub(r'：「', '：', new_text) # 去除段落开头的：「
        new_text = re.sub(r'。」', '。', new_text) # 去除段落结尾的：。」
        new_text = re.sub(r'，」', '，', new_text) # 去除段落结尾的：，」
        new_text = re.sub(r'！」', '！', new_text)
        new_text = re.sub(r'？」', '？', new_text)
        new_text = re.sub(r'……」', '……', new_text)
        new_text = re.sub(r'\n','1',new_text)
        new_text = re.sub(r'^【', '', new_text)  # 去除段落开头的「
        new_text = re.sub(r'】$', '', new_text)  # 去除段落结尾的」
        new_text = re.sub(r'：【', '：', new_text)  # 去除段落开头的：「
        new_text = re.sub(r'。】', '。', new_text)  # 去除段落结尾的：。」
        new_text = re.sub(r'，】', '，', new_text)  # 去除段落结尾的：，」
        new_text = re.sub(r'！】', '！', new_text)
        new_text = re.sub(r'？】', '？', new_text)
        new_text = re.sub(r'……】', '……', new_text)

        # 如果段落非空白，则将其添加到新文档
        if new_text.strip():
            new_para = new_doc.add_paragraph()
            new_para.add_run(new_text)

    # 保存修改后的文档
    new_doc.save(output_path)


def is_valid_docx(path):
    """检查文件是否为有效的 .docx 文件"""
    return os.path.isfile(path) and path.endswith('.docx')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python script.py <docx_file_path>")
        sys.exit(1)

    novel_docx_path = sys.argv[1]
    if novel_docx_path and is_valid_docx(novel_docx_path):
        # 调用处理函数
        remove_numbers_from_word(novel_docx_path, novel_docx_path)
        remove_extra_blank_lines(novel_docx_path, novel_docx_path)
        remove_quotes_from_docx(novel_docx_path, novel_docx_path)
        print(f"已删除标点符号和段落前数字")
    else:
        print("无效的文件路径或文件不是 .docx 格式")

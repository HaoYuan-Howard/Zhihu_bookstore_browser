import re
from docx import Document


# 删除独立数字行
def remove_numbers_from_word(doc_path, output_path):
    doc = Document(doc_path)

    regex = re.compile(r'^\s*(\d+|\d+、|（[一二三四五六七八九十百千万亿]+）|[一二三四五六七八九十百千万亿]+)\s*$')

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
    for para in doc.paragraphs:
        # 使用正则表达式替换开头的「和结尾的」符号
        new_text = re.sub(r'^「', '', para.text)  # 去除段落开头的「
        new_text = re.sub(r'」$', '', new_text)  # 去除段落结尾的」
        new_text = re.sub(r'：「', '：', new_text) # 去除段落开头的：「
        new_text = re.sub(r'。」', '。', new_text) # 去除段落结尾的：。」
        new_text = re.sub(r'，」', '，', new_text) # 去除段落结尾的：，」
        para.text = new_text  # 更新段落文本

    # 保存修改后的文档
    doc.save(output_path)

# 使用示例
doc_path = r'E:\practice_group\generate_novel\material\novel\喂.docx'
output_path = r'E:\practice_group\generate_novel\material\novel\喂.docx'
remove_numbers_from_word(doc_path, output_path)
remove_extra_blank_lines(output_path, output_path)
remove_quotes_from_docx(output_path,output_path)

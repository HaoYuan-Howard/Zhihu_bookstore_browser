def truncate_md_after_keyword(md_path, keyword="备案号:"):
    """
    打开一个 Markdown 文件，截断第一个匹配关键字后的内容，并覆盖保存原始文件。

    :param md_path: Markdown 文件的路径。
    :param keyword: 要匹配的关键字，默认为 "备案号:"。
    :return: None
    """
    try:
        # 读取 Markdown 文件内容
        with open(md_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 找到关键字的位置
        keyword_index = content.find(keyword)
        if keyword_index == -1:
            print(f"关键字 '{keyword}' 未在文件中找到，文件未做修改。")
            return

        # 截断关键字及其之前的内容
        truncated_content = content[:keyword_index + len(keyword)]

        # 覆盖保存原始文件
        with open(md_path, 'w', encoding='utf-8') as file:
            file.write(truncated_content)

        print(f"文件已成功截断并覆盖保存: {md_path}")

    except Exception as e:
        print(f"处理文件时出错: {e}")



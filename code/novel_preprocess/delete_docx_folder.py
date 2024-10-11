import os


def delete_docx_files(docx_folder):
    docx_files = [file for file in os.listdir(docx_folder) if file.endswith('.docx')]
    for file in docx_files:
        file_path = os.path.join(docx_folder, file)
        os.remove(file_path)
        print(f"已删除文件：{file_path}")


novel_type = ['恐怖', '文案', '末世', '沙雕', '治愈', '爽文', '甜文']
for n in novel_type:
    docx_folder = fr'E:\practice_group\generate_novel\material\novel\{n}'
    delete_docx_files(docx_folder)
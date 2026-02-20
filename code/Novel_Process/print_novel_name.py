import os


def print_novel_names(novel_folder):
    novel_files = [f for f in os.listdir(novel_folder) if f.endswith('.docx')]
    for i in novel_files:
        novel_name = os.path.splitext(i)[0]
        print(f"{novel_name}")


novel_folder = r"E:\practice_group\generate_novel\material\novel\末世"
print_novel_names(novel_folder)
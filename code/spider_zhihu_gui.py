import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import threading
import subprocess
import os
import json

# 定义四个Python脚本文件路径
scripts = {
    "知乎普通文章": "Spider_Zhihu_Novel/Spider_main/html_2_md_free.py",
    "知乎盐选文章": "Spider_Zhihu_Novel/Spider_main/html_2_md_yanxuan.py",
    "知乎书架文章": "Spider_Zhihu_Novel/Spider_main/html_2_md_shujia.py",
    "已有HTML文件": "Spider_Zhihu_Novel/Spider_main/html_2_md.py"
}

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
config_file = "config.json"  # JSON文件路径，用于存储上次输入的信息
novel_formation_scripts = "Novel_Process/delete_number_docx_novel.py"

# 页面历史堆栈
page_history = []

# 主窗口设置
root = tk.Tk()
root.title("知乎文章处理")
root.geometry("600x400")


def load_last_input():
    """ 从JSON文件加载上一次的输入信息 """
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"cookie": "", "url": "", "zhihu_html": "", "zhihu_md": ""}


def save_last_input(cookie, url, zhihu_html, zhihu_md):
    """ 将当前输入信息保存到JSON文件 """
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump({"cookie": cookie, "url": url, "zhihu_html": zhihu_html,"zhihu_md": zhihu_md}, file)
        
        
def clear_page():
    for widget in root.winfo_children():
        widget.destroy()


def go_back():
    """返回上一页"""
    if page_history:
        last_page, *args = page_history.pop()
        last_page(*args)  # 调用上一页的函数，并传入参数
    else:
        print("无可返回的页面")


def open_file(filepath):
    """ 打开本地系统中的文件"""
    if os.path.exists(filepath):
        os.startfile(filepath)
    else:
        messagebox.showerror("文件错误", "找不到指定的文件。")


def get_novel_page(script_name):
    """ 打开第二页 """
    # 保存当前页面到历史堆栈，包括参数
    page_history.append((main_page,))  # 返回时无参数

    clear_page()

    header_frame = tk.Frame(root)
    header_frame.pack(pady=10, fill=tk.X)

    back_button = tk.Button(header_frame, text="返回上一级", command=go_back, bg='lightblue', fg='black')
    back_button.pack(side=tk.LEFT, padx=10)

    tk.Label(header_frame, text=script_name, font=("Arial", 16)).pack(side=tk.TOP, pady=5)

    frame_left = tk.Frame(root, width=400, height=400)
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_right = tk.Frame(root, width=200, height=400)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    last_input = load_last_input()

    if script_name not in ["已有HTML文件", "知乎普通文章"]:
        tk.Label(frame_left, text="配置 Cookie:").pack(pady=5)
        cookie_entry = tk.Entry(frame_left, width=50)
        cookie_entry.insert(0, last_input.get("cookie", ""))
        cookie_entry.pack(pady=5)

        tk.Label(frame_left, text="配置 URL:").pack(pady=5)
        url_entry = tk.Entry(frame_left, width=50)
        url_entry.insert(0, last_input.get("url", ""))
        url_entry.pack(pady=5)
    else:
        cookie_entry = None
        url_entry = None
        
    tk.Label(frame_left, text="HTML文件路径:").pack(pady=5)
    html_path_entry = tk.Entry(frame_left, width=50)
    html_path_entry.insert(0, last_input.get("zhihu_html", ""))
    html_path_entry.pack(pady=5)

    tk.Label(frame_left, text="MD文件保存地址:").pack(pady=5)
    md_path_entry = tk.Entry(frame_left, width=50)
    md_path_entry.insert(0, last_input.get("zhihu_md", ""))
    md_path_entry.pack(pady=5)

    output_text = scrolledtext.ScrolledText(frame_right, wrap=tk.WORD, width=30, height=20)
    output_text.pack(pady=10, padx=10)

    def run_script():
        output_text.delete("1.0", tk.END)
        zhihu_html = html_path_entry.get()
        zhihu_md = md_path_entry.get()
        cookie = cookie_entry.get() if cookie_entry else ""
        url = url_entry.get() if url_entry else ""
        save_last_input(cookie, url, zhihu_html, zhihu_md)

        def execute_script():
            try:
                if script_name in ["已有HTML文件", "知乎普通文章"]:
                    command = ["python", scripts[script_name], zhihu_html, zhihu_md]
                else:
                    command = ["python", scripts[script_name], cookie, url, zhihu_html, zhihu_md]
                subprocess.run(command, encoding='utf-8', check=True)
                output_text.insert("end", f"小说源文件已保存到：{zhihu_md}\n")
                output_text.tag_config("link", foreground="red")
                output_text.tag_bind("link", "<Button-1>", lambda e: open_file(zhihu_md))
                output_text.insert("end", "点击打开MD文件\n", "link")

            except Exception as e:
                output_text.insert("end", f"执行过程中出错: {str(e)}")

        threading.Thread(target=execute_script).start()

    run_button = tk.Button(frame_left, text="生成 MD 文件", command=run_script, bg='lightblue')
    run_button.pack(pady=10)

    # 跳转到小说预处理页面
    preprocess_button = tk.Button(frame_left, text="格式化小说", command=lambda: novel_preprocess_page(script_name), bg='lightblue')
    preprocess_button.pack(pady=10)


def novel_preprocess_page(script_name):
    """ 第三页：小说预处理 """
    page_history.append((get_novel_page, script_name))

    clear_page()

    header_frame = tk.Frame(root)
    header_frame.pack(pady=10, fill=tk.X)

    back_button = tk.Button(header_frame, text="返回上一级", command=go_back, bg='lightblue', fg='black')
    back_button.pack(side=tk.LEFT, padx=10)

    tk.Label(header_frame, text="小说预处理", font=("Arial", 16)).pack(side=tk.TOP, pady=5)

    frame_left = tk.Frame(root, width=400, height=400)
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_right = tk.Frame(root, width=200, height=400)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def select_file():
        filepath = filedialog.askopenfilename(filetypes=[("Word 文件", "*.docx")])
        if filepath:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, filepath)

    tk.Label(frame_left, text="选择 DOCX 文件:").pack(pady=5)
    file_entry = tk.Entry(frame_left, width=50)
    file_entry.pack(pady=5)
    select_button = tk.Button(frame_left, text="浏览", command=select_file, bg='lightblue')
    select_button.pack(pady=5)

    def process_novel():
        def run_in_thread():
            docx_path = file_entry.get()
            if not os.path.exists(docx_path):
                messagebox.showerror("文件错误", "找不到指定的文件。")
                return
            try:
                command = ["python", novel_formation_scripts, docx_path]
                subprocess.run(command, check=True)
                output_text.insert("end", f"已成功格式化：{docx_path}\n")
                output_text.tag_config("link", foreground="red")
                output_text.tag_bind("link", "<Button-1>", lambda e: open_file(docx_path))
                output_text.insert("end", "点击打开Word文件\n", "link")
            except Exception as e:
                output_text.insert("end", f"格式化失败：{str(e)}\n")

        threading.Thread(target=run_in_thread, daemon=True).start()

    format_button = tk.Button(frame_left, text="格式化小说", command=process_novel, bg='lightblue')
    format_button.pack(pady=10)

    output_text = scrolledtext.ScrolledText(frame_right, wrap=tk.WORD, width=30, height=20)
    output_text.pack(pady=10, padx=10)


def main_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="选择要处理的文章类型", font=("Arial", 16)).pack(pady=20)

    for name in scripts.keys():
        btn = tk.Button(root, text=name, command=lambda n=name: get_novel_page(n))
        btn.pack(pady=10, ipadx=20, ipady=10)


main_page()
root.mainloop()

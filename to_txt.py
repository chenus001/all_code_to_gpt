import os
import tkinter as tk
from tkinter import filedialog

def remove_python_comments(code):
    lines = code.splitlines()
    new_lines = []
    in_string = False
    string_char = ""
    for line in lines:
        new_line = ""
        i = 0
        while i < len(line):
            if line[i] in ("'", '"') and not in_string:
                in_string = True
                string_char = line[i]
                new_line += line[i]
            elif line[i] == string_char and in_string:
                if i > 0 and line[i-1] != '\\':  # Handle escaping quotes
                    in_string = False
                new_line += line[i]
            elif line[i] == '#' and not in_string:
                break
            else:
                new_line += line[i]
            i += 1
        if new_line.strip():
            new_lines.append(new_line)
    return '\n'.join(new_lines)

def remove_js_comments(code):
    lines = code.splitlines()
    new_lines = []
    in_single_comment = False
    in_multi_comment = False
    in_string = False
    string_char = ""
    for line in lines:
        new_line = ""
        i = 0
        while i < len(line):
            if line[i] in ("'", '"') and not in_string and not in_multi_comment and not in_single_comment:
                in_string = True
                string_char = line[i]
                new_line += line[i]
            elif line[i] == string_char and in_string:
                if i > 0 and line[i-1] != '\\':  # Handle escaping quotes
                    in_string = False
                new_line += line[i]
            elif i < len(line) - 1 and line[i:i+2] == '//' and not in_string and not in_multi_comment:
                break
            elif i < len(line) - 1 and line[i:i+2] == '/*' and not in_string and not in_single_comment:
                in_multi_comment = True
                i += 1
            elif i < len(line) - 1 and line[i:i+2] == '*/' and in_multi_comment:
                in_multi_comment = False
                i += 1
            elif not in_multi_comment and not in_single_comment:
                new_line += line[i]
            i += 1
        if new_line.strip() and not in_single_comment and not in_multi_comment:
            new_lines.append(new_line)
    return '\n'.join(new_lines)

def write_directory_structure(f, src_path):
    for root, dirs, files in os.walk(src_path):
        level = root.replace(src_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        f.write('{}{}/\n'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            f.write('{}{}\n'.format(subindent, file))
    f.write("\n\n")

def write_files_content(f, src_path):
    for root, dirs, files in os.walk(src_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1]
            f.write(f"File: {file_path}\n\n")
            with open(file_path, 'r', encoding='utf-8') as file_content:
                code = file_content.read()
                if file_extension in ['.py']:
                    cleaned_code = remove_python_comments(code)
                elif file_extension in ['.js', '.jsx', '.ts', '.tsx']:
                    cleaned_code = remove_js_comments(code)
                else:
                    cleaned_code = code  # 对于其他文件类型，不处理注释
                f.write(cleaned_code)
                f.write("\n\n")

def main(src_path, output_file):
    # 之前的主功能函数代码保持不变
    pass

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        src_path_entry.delete(0, tk.END)
        src_path_entry.insert(0, directory)

def select_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".txt")
    if output_file:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, output_file)

def execute_program():
    src_path = src_path_entry.get()
    output_file = output_file_entry.get()
    main(src_path, output_file)
    result_label.config(text="目录结构和代码已保存到 " + output_file)

# 创建主窗口
root = tk.Tk()
root.title("文件处理程序")

# 添加组件：输入源路径
tk.Label(root, text="源路径:").pack()
src_path_entry = tk.Entry(root, width=50)
src_path_entry.pack()
src_path_button = tk.Button(root, text="选择路径", command=select_directory)
src_path_button.pack()

# 添加组件：输入输出文件
tk.Label(root, text="输出文件名:").pack()
output_file_entry = tk.Entry(root, width=50)
output_file_entry.pack()
output_file_button = tk.Button(root, text="选择文件", command=select_output_file)
output_file_button.pack()

# 添加按钮执行程序
execute_button = tk.Button(root, text="执行程序", command=execute_program)
execute_button.pack()

# 显示执行结果
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
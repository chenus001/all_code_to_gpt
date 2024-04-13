import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

# Assuming the functions remove_python_comments and remove_js_comments are defined elsewhere in the code as you have shown before.
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
    # Define a list of image file extensions to ignore
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.ico']

    for root, dirs, files in os.walk(src_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()  # Use lower to handle case variations
            if file_extension in image_extensions:
                continue  # Skip the file if it's an image

            f.write(f"File: {file_path}\n\n")
            try:
                with open(file_path, 'r', encoding='utf-8') as file_content:
                    code = file_content.read()
                    if file_extension in ['.py']:
                        cleaned_code = remove_python_comments(code)
                    elif file_extension in ['.js', '.jsx', '.ts', '.tsx']:
                        cleaned_code = remove_js_comments(code)
                    else:
                        cleaned_code = code  # No comment removal for other file types
                    f.write(cleaned_code)
                    f.write("\n\n")
            except UnicodeDecodeError:
                messagebox.showerror("Encoding Error", f"Failed to read file {file_path} due to encoding issue.")
            except IOError as e:
                messagebox.showerror("File Error", f"Failed to read file {file_path}: {str(e)}")

def main_gui():
    def browse_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            src_path_entry.delete(0, tk.END)
            src_path_entry.insert(0, folder_selected)

    def save_file():
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("文本文件", "*.txt")])
        if file:
            output_file_entry.delete(0, tk.END)
            output_file_entry.insert(0, file)

    def run_processing():
        src_path = src_path_entry.get()
        output_file = output_file_entry.get()
        if not src_path or not output_file:
            messagebox.showerror("错误", "请指定源目录和输出文件。")
            return
        if not os.path.isdir(src_path):
            messagebox.showerror("错误", "指定的源目录不存在。")
            return
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                write_directory_structure(f, src_path)
                write_files_content(f, src_path)
            messagebox.showinfo("成功", "目录结构和代码已保存到 " + output_file)
            open_button.config(state=tk.NORMAL)  # 启用“打开输出目录”按钮
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def open_output_dir():
        output_file = output_file_entry.get()
        output_dir = os.path.dirname(output_file)
        webbrowser.open(output_dir)

    root = tk.Tk()
    root.title("目录结构和代码保存器")

    tk.Label(root, text="源目录：").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
    src_path_entry = tk.Entry(root, width=50)
    src_path_entry.grid(row=0, column=1, pady=2, padx=5)
    tk.Button(root, text="浏览...", command=browse_folder).grid(row=0, column=2, pady=2, padx=5)

    tk.Label(root, text="输出文件：").grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
    output_file_entry = tk.Entry(root, width=50)
    output_file_entry.grid(row=1, column=1, pady=2, padx=5)
    tk.Button(root, text="保存为...", command=save_file).grid(row=1, column=2, pady=2, padx=5)

    tk.Button(root, text="运行", command=run_processing).grid(row=2, column=1, pady=10, padx=5)

    # 添加一个打开输出目录的按钮
    open_button = tk.Button(root, text="打开输出目录", command=open_output_dir, state=tk.DISABLED)
    open_button.grid(row=3, column=1, pady=10, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main_gui()

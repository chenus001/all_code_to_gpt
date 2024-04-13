import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

# Assuming the functions to remove comments from Python and JavaScript are defined elsewhere in the code.
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
            src_path